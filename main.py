import logging
from pathlib import Path
from typing import Optional, List

from git import Repo
from langchain_community.retrievers import TFIDFRetriever
from langchain_core.documents import Document as LangChainDocument
from langchain_core.retrievers import BaseRetriever
from phi.assistant import Assistant
from phi.document import Document
from phi.knowledge import AssistantKnowledge
from phi.knowledge.langchain import LangChainKnowledgeBase
from phi.llm.ollama import Ollama
from phi.prompt import PromptTemplate


def init_cudeschin(update=True):
    """Download (and update) the Cudeschin aka the documents we want to RAG on."""
    cudeschin_path = Path("./cudeschin")

    if not cudeschin_path.exists():
        Repo.clone_from("https://github.com/scout-ch/cudeschin.git", cudeschin_path)
    elif update:
        Repo(cudeschin_path).remote("origin").pull()

    return cudeschin_path


class LessPickyLangChainKnowledgeBase(LangChainKnowledgeBase):
    def search(self, query: str, num_documents: Optional[int] = None) -> List[LangChainDocument]:
        if self.retriever is None:
            raise ValueError("must provide retriever")

        if not isinstance(self.retriever, BaseRetriever):  # no reason for VectorStoreRetriever
            raise ValueError(f"Retriever is not of type BaseRetriever: {self.retriever}")

        _num_documents = num_documents or self.num_documents
        # logger.debug(f"Getting {_num_documents} relevant documents for query: {query}")
        lc_documents: List[LangChainDocument] = self.retriever.invoke(input=query)
        documents = []
        for lc_doc in lc_documents:
            documents.append(
                Document(
                    content=lc_doc.page_content,
                    meta_data=lc_doc.metadata,
                )
            )

        return documents


def init_knowledge_base(cudeschin_path: Path, n_documents=3) -> AssistantKnowledge:
    """
    Set up and load the knowledge base. This is (arguably) the most important part of the whole application and defines
    the R in RAG. The most common way is to use a vector database and embed chunks of the documents for a semantic
    similarity search (akin to the traditional TF-IDF). Other options could include to do a (fuzzy) keyword search.
    """
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    from langchain_community.document_loaders import TextLoader
    from langchain_community.document_loaders import DirectoryLoader

    loader = DirectoryLoader(cudeschin_path / "content/de", glob="**/*.md",
                             loader_cls=TextLoader,
                             loader_kwargs=dict(encoding="utf-8"))

    # doesn't derive from TextSplitter -> no split_documents so manual aggregation necessary
    splitter = MarkdownHeaderTextSplitter(
        # cudeschin only contains these two header types
        headers_to_split_on=[("###", "Ueberschrift"), ("####", "Unterkapitel")], strip_headers=False)
    o_docs = loader.load()
    docs = []
    for o_doc in o_docs:
        chunks = splitter.split_text(o_doc.page_content)
        for chunk in chunks:
            chunk.metadata.update(o_doc.metadata)
        docs.extend(chunks)

    # splits on all headers and always keeps them. Derives from TextSplitter. Doesn't set is_separator_regex even though it should?
    # splitter = MarkdownTextSplitter(is_separator_regex=True)
    # docs = splitter.split_documents(loader.load())

    retriever = TFIDFRetriever.from_documents(docs, k=n_documents)

    # passing num_documents here literally only changes the log message
    return LessPickyLangChainKnowledgeBase(retriever=retriever, num_documents=n_documents)


def init_assistant(cudeschin: AssistantKnowledge):
    """
    Set up the actual assistant with its model, templates and prompts.
    """
    # Results are generally very sensitive to prompting, especially when working in a non-english language.
    # https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1/
    # Also, something to be careful about (or it can get confusing) is the pre-configured system prompt from Ollama.
    # Both phidata and Ollama have some opinions about system prompts and prompt templates in general so here's a short
    # breakdown:
    # - whenever Ollama is used, you are using the template in the modelfile, which defines how to pass messages
    #   or prompts to the model. In the case of llama3.1 it seems to format multiple messages plainly according to
    #   the specs above, but if you include any mention of tools, it will write an english prompt saying "you're able
    #   to use tools", which might not be what you want. Another thing that confuses me is that there is no
    #   <|begin_of_text|> tag despite the specs saying you need one AND there is an unconditional <|eot_id|> tag, even
    #   if there's no user message. It seems to work still but idk, I kinda suspect that's an error and the eot tag is
    #   just a workaround to get the model to generate anything after forgetting the begin_of_text? Must try with
    #   custom modelfile.
    # - when using phidata, it will use the ollama-python library, which will use the /api/chat endpoint
    #   (https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion). This endpoint accepts
    #   messages from a conversation where each message has a role (system, assistant, user, tool). These messages
    #   are then formatted according to the prompt template in the modelfile.
    # TODO try custom modelfile with potentially better template, will have to do some testing (then contribute?).
    # TODO you could also do one of these from scratch without PhiData but so far I like the level of abstraction.

    return Assistant(
        llm=Ollama(
            # TODO experiment with different model versions, quantizations and instruct vs chat.
            model="llama3.1:8b-instruct-q5_K_M",  # model version heavily influences prompting style
            options=dict(temperature=0.1),
        ),
        # TODO fiddle around with the prompts, I don't think I like things like DSPy.
        system_prompt=
        "Du bist ein Schweizer Pfadi-Coach und unterstützst die Leitpersonen beim Planen und Durchführen "
        "von Aktivitäten und Lagern indem du ihre Fragen zur Pfadi faktisch beantwortest und "
        "dafür mitgelieferte Informationen zur Pfadi und Jungend und Sport (J+S) verwendetst.\n"
        "<instructions>\n"
        "1. Beantworte die Fragen immer auf Deutsch.\n"
        "2. Beantworte die Fragen, indem du Inhalte aus der mitgelieferten knowledge_base zitierst oder umschreibst. "
        "Nutze dazu das Feld `content` der knowledge_base-Einträge.\n"
        "3. Gib jeweils an von welcher Datei die Informationen "
        "stammen (Feld `meta_data.source`). SCHREIBE NICHTS ÜBER DIE STRUKTUR DER KNOWLEDGE_BASE, VERWENDE SIE NUR!\n"
        # "3. Die mitgelieferten Informationen enthalten meistens Links zu weiterführenden Informationen, "
        # "erwähne diese jeweils am Ende der Antwort.\n"
        "4. Formatiere deine Antwort mithilfe von Markdown.\n"
        "</instructions>",
        user_prompt_template=PromptTemplate(template="Beantworte folgende Frage zur Pfadi mithilfe der Informationen "
                                                     "aus der strukturierten knowledge_base unterhalb: {message}\n\n"
                                                     "<knowledge_base>\n{references}\n</knowledge_base>"),
        knowledge_base=cudeschin,
        # TODO try a version where the model has to use function calls to query the knowledge base. I suspect
        # the results will be worse for small models but better for large models (that can write good queries).
        add_references_to_prompt=True,  # force references and always query the knowledge base
        # these are all False by default btw, I just want to be explicit about it with reasons why.
        add_chat_history_to_prompt=False,  # sends all the messages to the chat endpoint to simulate a continued
        # conversation, BUT it also adds an extra (english) prompt with all previous messages, there doesn't seem to
        # be a way to separate those but not sure, would have to dig deeper.
        markdown=False,  # avoid extra (english) prompt specifying to write in Markdown
        create_memories=False,  # no need to store history atm
        debug=True,
        save_output_to_file="./output.md",
    )


def clean_user_prompt(prompt: str) -> str:
    """
    Clean the user prompt before sending it further. Can be used for various things BUT THIS IS A HACK!
    I would generally advise against things like this and to instead focus on other parts but then again trying to
    get an LLM to do what you want is inherently hacky af.
    """
    return (prompt.replace("LS", "J+S Lagersport (LS)").
            replace("LA", "J+S Lageraktivität (LA)").
            replace("LP", "J+S Lagerprogramm (LP)"))


if __name__ == '__main__':
    logging.getLogger("phi").setLevel(logging.DEBUG)

    cudeschin_path = init_cudeschin(update=True)
    cudeschin = init_knowledge_base(cudeschin_path)
    assistant = init_assistant(cudeschin)

    question = clean_user_prompt("Auf was muss ich beim Planen eines LS-Blocks achten?")

    assistant.print_response(question)
