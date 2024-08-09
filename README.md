# Cudeschin RAG

Simple RAG (retrieval augmented generation) app to give infos on scouts-stuff, mainly for planning. It is generally a proof of concept and (as you'll read below) is barely more convenient than using a proper search tool.

Desired features:

- [ ] Answer questions about planning and general basics of scouting.
- [ ] Be considerably more accurate than the base model.
- [ ] Add suitable and correct references to the original source, paraphrase where possible.
- [ ] Should be fully offline and self-hosted.
- [ ] Simple UI with Streamlit or Gradio.
- Might be interesting, but not sure if I want to invest the time (I probably won't be using this app)
  - [ ] Multilingual support; Cudesch(in) exists in German, French and Italian.
  - [ ] Entailment check (RTE, NLI) to assess whether the response answers the question. Could also be used to check whether the retrieved context is relevant to the question.
  - [ ] Secondary layer with deep search in the full Cudesch.

Currently, RAG applications are desired by many companies, but few realize that there are a lot of prerequisites before AI enters the frame. Collecting, organizing and cleaning the data are often the hardest and most time-consuming tasks. Then you need to decide on a good search strategy. The hot, trendy way is to chunk the documents up, embed them into a vector database and use semantic similarity to select the most relevant chunks. However, old school search methods may often be more performant and accurate. I'm glad some companies (e.g. [DeepJudge](https://www.deepjudge.ai/)) recognize that the most important part of RAG is the R and focus their engineering on a search engine. Whether you use this search engine to look for documents to read or to feed them to an LLM in hopes of getting a contextualized or simpler but still accurate response is secondary. While RAG can be useful in some cases, I think it's important to highlight that the prerequisites needed for building such an application usually already yield a high benefit without needing to fiddle around with chunking, models, and prompts.

For this project, I wanted to avoid all the tiring and frankly not very interesting work of collecting and cleaning all the documents of [Cudesch](https://pfadi.swiss/de/cudesch/), so I used the condensed, cheatsheet-like version [Cudeschin](https://github.com/scout-ch/cudeschin). \
There is another project, named [cudesch-indexer](https://github.com/carlobeltrame/pfadi.ai), trying a similar thing on the entirety of Cudesch using LangChain instead of phidata. TODO compare.

Btw. [phidata](https://github.com/phidatahq/phidata) has a ton of templates and advanced features, including simple ways to deploy projects like this to production. I wanted to keep it as simple as possible, so I avoided things like [phi workspaces](https://docs.phidata.com/templates/workspace/introduction) in favor of a simple docker-compose for the vectordb.
