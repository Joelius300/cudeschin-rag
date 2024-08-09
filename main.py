import logging
from pathlib import Path

from git import Repo
from phi.assistant import Assistant
from phi.embedder.ollama import OllamaEmbedder
from phi.knowledge import AssistantKnowledge
from phi.knowledge.text import TextKnowledgeBase
from phi.llm.ollama import Ollama
from phi.prompt import PromptTemplate
from phi.vectordb.pgvector import PgVector2


def init_cudeschin(update=True):
    cudeschin_path = Path("./cudeschin")

    if not cudeschin_path.exists():
        Repo.clone_from("https://github.com/scout-ch/cudeschin.git", cudeschin_path)
    elif update:
        Repo(cudeschin_path).remote("origin").pull()

    return cudeschin_path


def init_knowledge_base(cudeschin_path: Path):
    knowledge_base = TextKnowledgeBase(
        path=cudeschin_path / "content/de",
        formats=[".md"],
        num_documents=3,
        vector_db=PgVector2(
            collection="cudeschin",
            embedder=OllamaEmbedder(model="nomic-embed-text", dimensions=768),
            db_url="postgresql+psycopg://ai:asdf@localhost:5433/cudeschin",
        ),
    )

    knowledge_base.load(recreate=False)

    return knowledge_base


def init_assistant(cudeschin: AssistantKnowledge):
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
    # TODO custom modelfile with potentially better template, will have to see if it's actually true (then contribute).

    return Assistant(
        # TODO specify a low temperature, we don't want it to be creative at all.
        # TODO fiddle around with the prompt, I don't think I like things like DSPy.
        # TODO you could also do one of these from scratch without PhiData but so far I like the level of abstraction.
        llm=Ollama(model="llama3.1:8b-instruct-q5_K_M"),  # model version heavily influences prompting style
        system_prompt=
        "Du bist ein Schweizer Pfadi-Coach und unterstützst die Leitpersonen beim Planen und Durchführen"
        "von Aktivitäten und Lagern indem du ihre Fragen faktisch beantwortest und Informationen der"
        "J+S Brochuren verwendetst.\n"
        "<instructions>\n"
        "1. Antworte immer auf Deutsch.\n"
        "2. Verwende ausschliesslich Informationen aus dem Kontext, wenn möglich in Form von Zitaten. "
        "Referenziere genau, welche Informationen von wo verwendet wurden.\n"
        "3. Formatiere deine Antwort mithilfe von Markdown.\n"
        "</instructions>",
        # TODO tune user prompt to include references. also don't forget, it's an instruction model.
        user_prompt_template=PromptTemplate(template="Beantworte der Leitperson die folgende Frage"
                                                     "über die Pfadi mithilfe des Kontexts unterhalb: {message}"),
        knowledge_base=cudeschin,
        add_references_to_prompt=True,  # force references
        markdown=False,  # avoid extra (english) prompt specifying to write in Markdown
        debug=True,
    )


if __name__ == '__main__':
    logging.getLogger("phi").setLevel(logging.DEBUG)

    cudeschin_path = init_cudeschin(update=True)
    cudeschin = init_knowledge_base(cudeschin_path)
    assistant = init_assistant(cudeschin)

    assistant.print_response("Auf was muss ich beim Planen eines LS-Blocks achten?")
