# Cudeschin RAG

Simple RAG (retrieval augmented generation) app to answer questions on scouts-stuff, mainly for planning. It is meant as a proof of concept and (as you'll read below) is barely more convenient than using a proper search tool IMO. While I agree that RAG systems can be really powerful if designed correctly, I am generally a bit sceptical and think that their wide-spread adoption for everything in the last few years borders on over- and misuse.

Features:

- [x] Correctly answer questions about planning and general basics of scouting.
- [x] Be considerably more accurate than the base model.
- [x] Add suitable and correct references to the original source, paraphrase where possible.
- [x] Should be lightweight, fully offline and self-hosted.
- [x] Offer simple user interaction with CLI.
- Might be interesting, but not sure if I want to invest the time (as I won't use the app)
  - [x] List all the used references clearly.
  - [ ] Force inclusion of the "see more" links at the end of every Cudeschin file, currently they are rarely retrieved.
  - [ ] Simple UI with Streamlit or Gradio.
  - [ ] Multi-turn conversaion for follow-up questions.
  - [ ] Multilingual support; Cudesch(in) exists in German, French and Italian.
  - [ ] Extensive tests with different prompt templates and models.
  - [ ] Using larger (potentially proprietary) models.
  - [ ] Entailment check (RTE, NLI) to assess whether the response answers the question. Could also be used to check whether the retrieved context is relevant to the question.
  - [ ] Secondary layer with deep search in the full Cudesch.
  - [ ] General refactoring; I wouldn't advice growing the codebase further before refactoring.

Currently, RAG applications are desired by many companies, but few realize that there are a lot of prerequisites before AI enters the frame. Collecting, organizing and cleaning the data are often the hardest and most time-consuming tasks. Then you need to decide on a good search strategy. The hot, trendy way is to chunk the documents up, embed them into a vector database and use semantic similarity to select the most relevant chunks. However, old school search methods (elasticsearch and friends) may be more performant and accurate, especially in big data scenarios. I'm glad some companies (e.g. [DeepJudge](https://www.deepjudge.ai/)) recognize that the most important part of RAG is the R and focus their engineering on optimizing retrieval (AFAIK). Whether you use this retrieval to look for documents to read yourself or to feed them to an LLM in hopes of getting a contextualized or simpler but still accurate response is secondary. As expected, the retrieval is also the component of this project that took the most time to get right **by far**. \
While RAG can be useful in some cases, I think it's important to highlight that the prerequisites needed for building such an application usually already yield a high benefit without needing to fiddle around with models and prompts. Additionally, I'm a big sceptic when it comes to using LLMs for anything reasoning-based; using RAG to tell the model what the rules are is easy, but making sure that the model can then correctly apply those rules to a specific scenario is basically impossible ([I'm with Yann on that one](https://lexfridman.com/yann-lecun-3-transcript)).

For this project, I wanted to avoid all the tiring and frankly not very interesting work of collecting and cleaning all the documents of [Cudesch](https://pfadi.swiss/de/cudesch/), so I used the condensed, cheatsheet-like version [Cudeschin](https://github.com/scout-ch/cudeschin). \
There is another project, named [cudesch-indexer](https://github.com/carlobeltrame/pfadi.ai), trying a similar thing on the entirety of Cudesch using LangChain and JavaScript instead of phidata and Python. I did not evaluate it to compare it with my project because it relies heavily on GPT-4, even for chunking, which I do not want to use. Switching to a local, less powerful model would not do it justice, I'm sure.

Btw. [phidata](https://github.com/phidatahq/phidata) has a ton of templates and advanced features, including simple ways to deploy projects like this to production. I wanted to keep it as simple as possible, so I avoided things like [phi workspaces](https://docs.phidata.com/templates/workspace/introduction) in favor of a self-contained CLI with a simple in-memory store at the cost of lower performance. \
As a takeaway, I think phidata has a nice level of abstraction when building simple applications like this and allows switching parts of the architecture very easily. They seem to excel in autonomous agents, so I'll be sure to use them again if that comes up. However, I think it's also fair to mention that they have a lot going on behind the scenes, which limits customizability. When an application needs a specific way of doing something (e.g. non-english), you might find that impossible to _just do_. LangChain seems better in that regard and also offers more tools because of its popularity.

## Some example answers (non-cherry-picked)

This was always run on my local setup with a quantized llama3.1-8b-instruct model. For such a small model, I'm very impressed by the quality of the answers.

NOTE: This first one is the one I always tested with, so the output is heavily biased. Note also that I injected J+S into the prompt behind the scenes because the LS to J+S association is of course missing in the embedding (could fine-tune theoretically), which prevented the retrieval of relevant information. The original input was "Auf was muss ich beim Planen eines LS-Blocks achten?".

Very happy with that answer.

```
╭──────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Message  │ Auf was muss ich beim Planen eines J+S Lagersport (LS)-Blocks achten?                                                                                                                 │
├──────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Response │ **Achtung beim Planen eines J+S Lagersport (LS)-Blocks**                                                                                                                              │
│ (5.6s)   │ =====================================================                                                                                                                                 │
│          │                                                                                                                                                                                       │
│          │ Beim Planen eines J+S Lagersport (LS)-Blocks sollten Sie folgende Punkte beachten:                                                                                                    │
│          │                                                                                                                                                                                       │
│          │ *   Die Aktivitäten sollten altersgerecht, vielfältig und abwechslungsreich sein.                                                                                                     │
│          │ *   Es sollte Freude an der Bewegung entstehen, insbesondere an vielfältigen Bewegungsgrundformen für Kinder.                                                                         │
│          │ *   Die Aktivitäten sollten oft in der Natur stattfinden.                                                                                                                             │
│          │ *   Sie können in den Bereichen Unterwegs sein (z.B. Wanderungen), Sport (z.B. Ballspiele) und Spiel (z.B. Geländespiele) liegen.                                                     │
│          │                                                                                                                                                                                       │
│          │ **Rahmenbedingungen**                                                                                                                                                                 │
│          │ -------------------                                                                                                                                                                   │
│          │                                                                                                                                                                                       │
│          │ Beachten Sie auch die Rahmenbedingungen für J+S-Aktivitäten:                                                                                                                          │
│          │                                                                                                                                                                                       │
│          │ *   Pro Lagertag sollten mindestens vier Stunden, maximal zwei Stunden davon als Lageraktivität, verteilt auf mindestens zwei Tageszeiten (Morgen, Mittag, Abend), eingeplant werden. │
│          │ *   Die Dauer jeder Aktivität sollte mindestens 30 Minuten betragen.                                                                                                                  │
│          │                                                                                                                                                                                       │
│          │ Quelle: cudeschin/content/de/03_Aktivitaet_LST.md                                                                                                                                     │
╰──────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Folgende Referenzen wurden verwendet (wenn diese unpassend sind, versuche die Frage umzuformulieren):
╭──────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Quelle                                                       │ Inhalt                                                                                                                                                 │
├──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md (Rahmenbedingungen für J+S-Aktivitäten) │ ### Rahmenbedingungen für J+S-Aktivitäten                                                                                                              │
│                                                              │ - pro Lagertag mindestens vier Stunden, maximal zwei Stunden davon als Lageraktivität                                                                  │
│                                                              │ - verteilt auf mindestens zwei Tageszeiten (Morgen, Mittag, Abend)                                                                                     │
│                                                              │ - Dauer mindestens 30 Minuten pro Aktivität (Block)                                                                                                    │
├──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md                                         │ ⛺ Aktivitäten im Lagersport/Trekking (J+S)                                                                                                            │
│                                                              │ -------------------------------------------                                                                                                            │
│                                                              │ In einem J+S Lager gibt es J+S-Aktivitäten und Verbandsaktivitäten, die J+S-Aktivitäten unterteilen sich in Lagersport (LS) und Lageraktivitäten (LA). │
├──────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md (Lagersport (LS))                       │ ### Lagersport (LS)                                                                                                                                    │
│                                                              │ **Ziel:** altersgerechte, vielfältige und abwechslungsreiche Spiel- und Sportaktivitäten                                                               │
│                                                              │ Dies bedeutet:                                                                                                                                         │
│                                                              │ - Freude an der vielfältigen Bewegung (Link Bewegungsgrundformen für Kinder)                                                                           │
│                                                              │ - Erlebnis in der Gruppe                                                                                                                               │
│                                                              │ - Oft mit einfachen Mitteln umgesetzt                                                                                                                  │
│                                                              │ - Finden typischerweise in der Natur statt                                                                                                             │
│                                                              │ Aktivitäten in den Bereichen:                                                                                                                          │
│                                                              │ - Unterwegs sein (Wanderungen, Schneeschuhtouren, Touren mit Velo, Bike, Inline-Skates, ...)                                                           │
│                                                              │ - Sport (Ballspiele, Trendsportarten, andere Sportarten wie Tanzen, Orientierungslauf, ...)                                                            │
│                                                              │ - Spiel (Spielturniere, Geländespiele, Spielfest, Freies Spiel, Kämpfen und Raufen, ...)                                                               │
╰──────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Changing LS to LA makes quite a big difference when planning, so let's see how it will do here. Note, I never tried this before this run, but there is a similar LA <-> J+S hack implemented.

I am happy with that answer as it contains only correct information. It missed two of the three general J+S requirements in favour of LA-specific ones. It correctly lists all the possible topic, but it is slightly incorrect in saying that these are examples. These really are the only possible ones and the TN also _must_ learn something, it's not optional as written. Still, all in all pretty impressive.

```
╭──────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Message  │ Auf was muss ich beim Planen eines J+S Lageraktivität (LA) Blocks achten?                                               │
├──────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Response │ **Achtung beim Planen eines J+S Lageraktivität (LA) Blocks**                                                            │
│ (4.4s)   │                                                                                                                         │
│          │ Beim Planen eines LA-Blocks solltest du folgende Aspekte beachten:                                                      │
│          │                                                                                                                         │
│          │ * Die Dauer der Aktivität sollte mindestens 30 Minuten betragen.                                                        │
│          │ * Die Aktivität sollte in der Gruppe stattfinden und alle Teilnehmenden sollten sich aktiv an der Aktivität beteiligen. │
│          │ * Alle Teilnehmenden sollten etwas lernen, was bedeutet, dass die Aktivität einen Ausbildungscharakter haben sollte.    │
│          │                                                                                                                         │
│          │ Es gibt verschiedene Bereiche, in denen LA-Blocke durchgeführt werden können, wie zum Beispiel:                         │
│          │                                                                                                                         │
│          │ * Outdoortechniken (z.B. Wanderplanung, Kartenlesen)                                                                    │
│          │ * Sicherheit (z.B. Unfallorganisation und Alarmierung, 1. Hilfe)                                                        │
│          │ * Natur und Umwelt (z.B. Tier- und Pflanzenwelt, Umweltschutz im Lager)                                                 │
│          │ * Pioniertechnik (z.B. Biwakbau, Material- und Ausrüstungskunde)                                                        │
│          │ * Lagerplatz/Lagerhaus/Umgebung (z.B. Einrichten, Abbau von Spielplätzeinrichtungen und Sportgeräten)                   │
│          │ * Prävention und Integration (z.B. Aktivitäten zur Förderung der Kompetenzen in diesem Bereich)                         │
│          │                                                                                                                         │
│          │ Quelle: (cudeschin/content/de/03_Aktivitaet_LST.md)                                                                     │
╰──────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Folgende Referenzen wurden verwendet (wenn diese unpassend sind, versuche die Frage umzuformulieren):
╭──────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Quelle                                                       │ Inhalt                                                                                                                                                                        │
├──────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md (Rahmenbedingungen für J+S-Aktivitäten) │ ### Rahmenbedingungen für J+S-Aktivitäten                                                                                                                                     │
│                                                              │ - pro Lagertag mindestens vier Stunden, maximal zwei Stunden davon als Lageraktivität                                                                                         │
│                                                              │ - verteilt auf mindestens zwei Tageszeiten (Morgen, Mittag, Abend)                                                                                                            │
│                                                              │ - Dauer mindestens 30 Minuten pro Aktivität (Block)                                                                                                                           │
├──────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md                                         │ ⛺ Aktivitäten im Lagersport/Trekking (J+S)                                                                                                                                   │
│                                                              │ -------------------------------------------                                                                                                                                   │
│                                                              │ In einem J+S Lager gibt es J+S-Aktivitäten und Verbandsaktivitäten, die J+S-Aktivitäten unterteilen sich in Lagersport (LS) und Lageraktivitäten (LA).                        │
├──────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 03_Aktivitaet_LST.md (Lageraktivität (LA))                   │ ### Lageraktivität (LA)                                                                                                                                                       │
│                                                              │ **Ziel:** möglichst praxisnahes und spielerisches Erlernen von Wissen und Fähigkeiten, die für Lagersport/Trekking notwendig sind                                             │
│                                                              │ Dies bedeutet:                                                                                                                                                                │
│                                                              │ - Alle Teilnehmende müssen etwas lernen (Ausbildungscharakter)                                                                                                                │
│                                                              │ - Alle Teilnehmende beteiligen sich aktiv an der Aktivität                                                                                                                    │
│                                                              │ - Lageraktivitäten müssen in der Gruppe stattfinden                                                                                                                           │
│                                                              │ Aktivitäten in den Bereichen:                                                                                                                                                 │
│                                                              │ - Outdoortechniken (Wanderplanung, Kartenlesen, Krokieren, Orientieren im Gelände, ...)                                                                                       │
│                                                              │ - Sicherheit (Sicherheit im Lager, Unfallorganisation und Alarmierung, 1. Hilfe, ...)                                                                                         │
│                                                              │ - Natur und Umwelt (Tier- und Pflanzenwelt, Umweltschutz im Lager, Wetter- und Sternenkunde, Ãbermittlungstechniken, Feuer machen, ...)                                       │
│                                                              │ - Pioniertechnik (Biwakbau, Material- und Ausrüstungskunde, Materialpflege, Erstellen und Abbau von Pionierbauten, Seil- und Knotenkunde, Seilbahnen, Seilbrücken, Abseilen,  │
│                                                              │ ...)                                                                                                                                                                          │
│                                                              │ - Lagerplatz/Lagerhaus/Umgebung (Einrichten, Abbau, Erstellen von Spielplatzeinrichtungen und Sportgeräten)                                                                   │
│                                                              │ - Prävention und Integration (Aktivitäten, welche der Prävention und der Integration dienen und die Kompetenzen der Teilnehmenden in diesem Bereich fördern)                  │
╰──────────────────────────────────────────────────────────────┴────────────────────────────────────────��──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

This one is also a first-timer, but I know the answer is contained in the Cudeschin.

I am also happy with that answer, it contains most of what I wanted to hear and doesn't include any incorrect information. It could be better if it told me where to find more information. Also, it's clear that the retrieval could still be improved because it fetched a tiny chunk with only a heading and no information as best match.

```
╭──────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Message  │ Wie muss ich in einem Notfall bei einer Aktivität vorgehen?                                                                                                                                    │
├──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Response │ **Notfallvorgehen bei einer Aktivität**                                                                                                                                                        │
│ (5.6s)   │ =====================================                                                                                                                                                          │
│          │                                                                                                                                                                                                │
│          │ Wenn in einer Aktivität ein Notfall auftritt, ist es wichtig, ruhig zu bleiben und einen klaren Überblick über die Situation zu gewinnen. Hier sind die Schritte, die du unternehmen solltest: │
│          │                                                                                                                                                                                                │
│          │ ### 1. **Schauen**                                                                                                                                                                             │
│          │                                                                                                                                                                                                │
│          │ * Bewahre Ruhe und beschaffe dich über die Situation.                                                                                                                                          │
│          │ * Frage dich:                                                                                                                                                                                  │
│          │         + Was ist geschehen?                                                                                                                                                                   │
│          │         + Wer ist beteiligt?                                                                                                                                                                   │
│          │         + Wer ist betroffen?                                                                                                                                                                   │
│          │                                                                                                                                                                                                │
│          │ ### 2. **Denken**                                                                                                                                                                              │
│          │                                                                                                                                                                                                │
│          │ * Überlege dir die möglichen Folgengefahren für:                                                                                                                                               │
│          │         + Unfallopfer                                                                                                                                                                          │
│          │         + Helfende                                                                                                                                                                             │
│          │         + Andere Personen                                                                                                                                                                      │
│          │                                                                                                                                                                                                │
│          │ ### 3. **Handeln**                                                                                                                                                                             │
│          │                                                                                                                                                                                                │
│          │ * Sorge für deinen Selbstschutz!                                                                                                                                                               │
│          │ * Alarmiere die Notfallnummern (z.B. 112) oder die Leitung des Teams.                                                                                                                          │
│          │ * Sichere die Unfallstelle, um weitere Unfälle zu vermeiden.                                                                                                                                   │
│          │ * Leiste Nothilfe, wenn möglich.                                                                                                                                                               │
│          │                                                                                                                                                                                                │
│          │ **Wichtig:** Ein Mitglied des Leitungsteams sollte die unbeteiligten Teilnehmer abseits der Unfallstelle betreuen.                                                                             │
│          │                                                                                                                                                                                                │
│          │ Quelle: (#)                                                                                                                                                                                    │
╰──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Folgende Referenzen wurden verwendet (wenn diese unpassend sind, versuche die Frage umzuformulieren):
╭────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Quelle                                                                     │ Inhalt                                                                                                   │
├────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 10_Handeln_im_notfall.md                                                   │ 🚦 Handeln im Notfall                                                                                    │
│                                                                            │ ---------------------                                                                                    │
├────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 10_Handeln_im_notfall.md (Notfall – was tun)                               │ ### Notfall – was tun                                                                                    │
│                                                                            │ **🔴 Schauen:**                                                                                          │
│                                                                            │ * Ruhe bewahren & Überblick beschaffen                                                                   │
│                                                                            │ * Was ist geschehen?                                                                                     │
│                                                                            │ * Wer ist beteiligt?                                                                                     │
│                                                                            │ * Wer ist betroffen?                                                                                     │
│                                                                            │ **🟠 Denken:**                                                                                           │
│                                                                            │ * Folgegefahren für Unfallopfer, Helfende und andere Personen?                                           │
│                                                                            │ **🟢 Handeln:**                                                                                          │
│                                                                            │ * Selbstschutz!                                                                                          │
│                                                                            │ * Alarmieren                                                                                             │
│                                                                            │ * Unfallstelle sichern/ für Sicherheit sorgen (weitere Unfälle vermeiden)                                │
│                                                                            │ * Nothilfe leisten                                                                                       │
│                                                                            │ **Wichtig:** Jemand aus dem Leitungsteam betreut die unbeteiligten Teilnehmenden abseits des Geschehens. │
├────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 08_Sicherheit.md (Sicherheitkonzept / Vorbereitung auf Notfallsituationen) │ #### Vorbereitung auf Notfallsituationen                                                                 │
│                                                                            │ [Und wenn doch etwas passiert? 🤔](/article/10)                                                          │
│                                                                            │ *   Ablauf und Verantwortlichkeiten im Notfall                                                           │
│                                                                            │ *   Notfallmaterial bereithalten (Apotheke, Mobiltelefon, Notfallnummern)                                │
│                                                                            │ *   Nächster Arzt, Spital, Notfalldienste, Apotheke kennen                                               │
╰────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

As a challenge, I also asked something that isn't in the Cudeschin. I fully expect it to fail, I just hope it doesn't make up too much misinformation. I already tried prompting it to say "I don't know" if it doesn't have enough information, but that significantly reduced the quality of previously good answers. Users would be able to tell that there is no information on this by the retrieved sources.

As expected, it didn't quite know how to answer that. Because the retrieval is set up to always fetch the three best matching document chunks, the model got context for planning other things, namely meetings and activities. Luckily, planning _anything_ will have some overlap, but it shows that the model wrongly incorporated this context in its answer (e.g. saying you need to prepare the agenda). It did correctly mention the files it got this information from (albeit with http), which already tells you there's something wrong, because none of them seem related to hiking. After that, the retrieved chunks are printed in full, so that a human intelligence can look at them and determine that the answer was misguided :)

```
╭──────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Message  │ Wie plane ich eine Wanderung und auf was muss ich achten?                                                                                              │
├──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Response │ **Planung einer Wanderung**                                                                                                                            │
│ (6.6s)   │                                                                                                                                                        │
│          │ Um eine Wanderung zu planen, sollten Sie zunächst die folgenden Punkte beachten:                                                                       │
│          │                                                                                                                                                        │
│          │ *   **Rahmenbedingungen klären**: Stellen Sie sicher, dass Sie alle notwendigen Informationen haben, bevor Sie mit der Planung beginnen. Dazu gehören: │
│          │     *   Der Ort und die Zeit der Wanderung                                                                                                             │
│          │     *   Die Anzahl und Alter der Teilnehmenden                                                                                                         │
│          │     *   Die erforderlichen Vorbereitungen (z.B. Ausrüstung, Verpflegung)                                                                               │
│          │     *   Die verfügbare Zeit und finanziellen Mittel                                                                                                    │
│          │ *   **Vorbereitung**: Stellen Sie sicher, dass alle notwendigen Unterlagen und Hilfsmittel vorbereitet sind.                                           │
│          │ *   **Traktanden / Themen sammeln und ordnen**: Sammeln Sie alle relevanten Informationen und ordnen Sie sie nach Bedarf an.                           │
│          │                                                                                                                                                        │
│          │ **Achtung bei der Planung**                                                                                                                            │
│          │                                                                                                                                                        │
│          │ Beachten Sie auch die folgenden Punkte:                                                                                                                │
│          │                                                                                                                                                        │
│          │ *   Die Dauer des Hockes (oder in diesem Fall der Wanderung) sollte bestimmt werden, um genügend Zeit für Pausen einzuplanen.                          │
│          │ *   Einladungen sollten frühzeitig versendet werden, damit alle Teilnehmenden sich auf die Veranstaltung vorbereiten können.                           │
│          │                                                                                                                                                        │
│          │ Quellen:                                                                                                                                               │
│          │                                                                                                                                                        │
│          │ *   (http://cudeschin/content/de/06_Hoeck.md)                                                                                                          │
│          │ *   (http://cudeschin/content/de/01_Aktivitaet_planen.md)                                                                                              │
╰──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Folgende Referenzen wurden verwendet (wenn diese unpassend sind, versuche die Frage umzuformulieren):
╭────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Quelle                                             │ Inhalt                                                                                                                                        │
├────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 06_Hoeck.md (Vorbereitung)                         │ #### Vorbereitung                                                                                                                             │
│                                                    │ *   Höckort (ruhig, genügend Platz, gut erreichbar)                                                                                           │
│                                                    │ *   Ziel des Höcks festlegen                                                                                                                  │
│                                                    │ *   Traktanden / Themen sammeln und ordnen: Information, diskutieren, entscheiden                                                             │
│                                                    │ *   Dauer des Höcks bestimmen, Pausen einplanen                                                                                               │
│                                                    │ *   Einladung frühzeitig versenden (Ort, Zeit, Traktanden, Unterlagen, Vorbereitung für Höckteilnehmende)                                     │
│                                                    │ *   Hilfsmittel und Unterlagen vorbereiten                                                                                                    │
├────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 01_Aktivitaet_planen.md                            │ 🏗️ Aktivität planen                                                                                                                            │
│                                                    │ -------------------                                                                                                                           │
│                                                    │ Bereits bei der [Quartalsplanung](/article/05) wurde die Aktivität grob geplant. Diese Unterlagen dienen als Grundlage für die Detailplanung. │
├────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 01_Aktivitaet_planen.md (Rahmenbedingungen klären) │ #### Rahmenbedingungen klären                                                                                                                 │
│                                                    │ *   Wo soll die Aktivität stattfinden?                                                                                                        │
│                                                    │ *   Was für eine Aktivität wird geplant?                                                                                                      │
│                                                    │ *   Wer sind die Teilnehmende (Anzahl, Alter, Wissen, Bedürfnisse, Interessen…)?                                                              │
│                                                    │ *   Wie viele Leitende?                                                                                                                       │
│                                                    │ *   Wie viel Zeit steht zur Verfügung?                                                                                                        │
│                                                    │ *   In welcher Jahreszeit / bei welchem Wetter findet die Aktivität statt?                                                                    │
│                                                    │ *   Welche finanziellen Mittel stehen zur Verfügung?                                                                                          │
│                                                    │ *   Welches Material steht zur Verfügung?                                                                                                     │
│                                                    │ *   Gibt es weitere Vorgaben oder Einschränkungen?                                                                                            │
╰────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## License

The Cudeschin PWA is licensed under AGPL and I couldn't find an exception/specification for the Markdown contents (which are derived from copyrighted material).
It probably won't matter for many, but I'll license this under AGPL as well just to be sure. Of course credit for the original Cudesch goes to the respective authors and copyright holders.
