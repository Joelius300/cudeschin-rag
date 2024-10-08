import json
import logging
from pathlib import Path

import fire
import rich
from git import Repo
from phi.assistant import Assistant
from phi.knowledge import AssistantKnowledge
from phi.llm.ollama import Ollama
from phi.prompt import PromptTemplate
from rich.box import ROUNDED
from rich.table import Table


def init_cudeschin(update=True):
    """Download (and update) the Cudeschin aka the documents we want to RAG on."""
    cudeschin_path = Path("./cudeschin")

    if not cudeschin_path.exists():
        Repo.clone_from("https://github.com/scout-ch/cudeschin.git", cudeschin_path)
    elif update:
        Repo(cudeschin_path).remote("origin").pull()

    return cudeschin_path


def init_knowledge_base(cudeschin_path: Path, n_documents=3) -> AssistantKnowledge:
    """
    Set up and load the knowledge base. This is (arguably) the most important part of the whole application and defines
    the R in RAG. The most common way is to use a vector database and embed chunks of the documents for a semantic
    similarity search (akin to the traditional TF-IDF). Other options could include a (fuzzy) keyword search.
    """
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    from langchain_community.document_loaders import TextLoader
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.document_loaders import DirectoryLoader
    from langchain_core.vectorstores import InMemoryVectorStore
    from phi.knowledge.langchain import LangChainKnowledgeBase

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

    embeddings = OllamaEmbeddings(model="jina/jina-embeddings-v2-base-de")  # make sure to use german embedding
    store = InMemoryVectorStore.from_documents(docs, embeddings)

    retriever = store.as_retriever(search_kwargs=dict(k=n_documents))

    # passing num_documents here literally only changes the log message
    return LangChainKnowledgeBase(retriever=retriever, num_documents=n_documents)


def init_assistant(cudeschin: AssistantKnowledge, temperature=0.1, debug=False):
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
    #   if there's no user message. This might be an error but after some testing, it seems to perform the same as
    #   formatting it according to the specs (see custom modelfile in file tree).
    # - when using phidata, it will use the ollama-python library, which will use the /api/chat endpoint
    #   (https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion). This endpoint accepts
    #   messages from a conversation where each message has a role (system, assistant, user, tool). These messages
    #   are then formatted according to the prompt template in the modelfile.

    # TODO you could also do one of these from scratch without PhiData but so far I like the level of abstraction.
    # Also, using LangChain all the way might also be interesting for more complex scenarios because it's a bit lower
    # level, but is still general unlike when directly building on top of the Ollama library for example.
    return Assistant(
        llm=Ollama(
            # TODO experiment with different model versions, quantizations and instruct vs chat.
            # model version heavily influences prompting style
            model="llama3.1:8b-instruct-q5_K_M",
            # model="llama3.1-instruct-custom",  # seemingly no difference in performance
            options=dict(temperature=temperature),  # TODO experiment with different temperature settings
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
        # NOTE: phidata formats the retrieved documents as JSON and inserts the JSON string into the prompt
        # at `references`. If you need a different format for the knowledge base, you need to pass a `reference_function`
        # to the assistant, which takes the assistant, query, num_documents and returns a string representation of the
        # retrieved documents. Also note that only the stringified references are added to memory, so if you want to
        # avoid decoding again from JSON, you'd need extra logic. Or just go with a lower level framework like LangChain.
        user_prompt_template=PromptTemplate(template="Beantworte folgende Frage zur Pfadi mithilfe der Informationen "
                                                     "aus der strukturierten knowledge_base unterhalb: {message}\n\n"
                                                     "<knowledge_base>\n{references}\n</knowledge_base>"),
        knowledge_base=cudeschin,
        # TODO try a version where the model has to use function calls to query the knowledge base (autonomous RAG).
        # I suspect the results will be worse for small models but better for large models (that can write good queries).
        add_references_to_prompt=True,  # force references and always query the knowledge base
        # these are all False by default btw, I just want to be explicit about it with reasons why.
        add_chat_history_to_prompt=False,  # sends all the messages to the chat endpoint to simulate a continued
        # conversation, BUT it also adds an extra (english) prompt with all previous messages, there doesn't seem to
        # be a way to separate those but not sure, would have to dig deeper.
        markdown=False,  # avoid extra (english) prompt specifying to write in Markdown
        create_memories=False,  # no need to store history atm
        debug=debug,
        save_output_to_file="./output.md",
    )


def improve_question(prompt: str) -> str:
    """
    Improve the user prompt for specific questions, where you know the model (or more likely the retrieval) struggles.
    I would generally advise against things like this and to instead focus on other parts but then again trying to
    get an LLM to do what you want is inherently hacky af.
    """
    return (prompt.replace("LS", "J+S Lagersport (LS)").
            replace("LA", "J+S Lageraktivität (LA)").
            replace("LP", "J+S Lagerprogramm (LP)"))


def cli(question: str, *, n_documents=3, temperature=0.1, debug=False, prompt_hacks=True):
    if debug:
        logging.getLogger("phi").setLevel(logging.DEBUG)

    cudeschin_path = init_cudeschin(update=True)
    cudeschin = init_knowledge_base(cudeschin_path, n_documents)
    assistant = init_assistant(cudeschin, temperature, debug)

    if prompt_hacks:
        question = improve_question(question)

    assistant.print_response(question)
    used_references = json.loads(assistant.memory.references[-1].references)
    rich.print("Folgende Referenzen wurden verwendet (wenn diese unpassend sind, versuche die Frage umzuformulieren):")
    table = Table(box=ROUNDED, border_style="blue", show_header=True, show_lines=True)
    table.add_column("Quelle")
    table.add_column("Inhalt")
    for ref in used_references:
        meta = ref["meta_data"]
        file = Path(meta["source"]).name
        headers = ""
        if "Ueberschrift" in meta:
            headers += meta["Ueberschrift"]
        if "Unterkapitel" in meta:
            if headers:
                headers += " / "
            headers += meta["Unterkapitel"]
        source = file + (f" ({headers})" if headers else "")
        table.add_row(source, ref["content"])
    rich.print(table)


if __name__ == '__main__':
    fire.Fire(cli)
