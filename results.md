# Results (newer first)

This document contains some sample results of specific versions and is a way to track the performance
for doing adjustments later. Not all results, especially those in the beginning, were tracked.

## d3d837422899

- Model: llama3.1:8b-instruct-q5_K_M
- Temperature: 0.1
- Chunking: Vanilla size based
- Retrieval: Semantic similarity with vectordb
- Embedder: jina/jina-embeddings-v2-base-de

### Works well

- German only
- Fast and fully offline
- Fairly deterministic and reliable despite small model
- Cites real links

### Problems

- Fetches irrelevant chunks (!!!)
- Does not answer the question with enough correct details

### Examples

```markdown
**Achtung beim Planen eines Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines LS-Blocks ist es wichtig, auf die Sicherheit und das Wohlbefinden der Teilnehmenden zu achten. Hier sind einige wichtige Punkte, die du beachten solltest:

*   **Sicherheitsaspekte**: Stelle sicher, dass alle notwendigen Sicherheitsmaßnahmen getroffen werden, wie z.B. die Einhaltung von Sicherheitsregeln und die Bereitstellung von geeigneten Ausrüstungen.
*   **Höck**: Wenn du einen Höck planst, solltest du dich an die Vorbereitungshinweise halten, um sicherzustellen, dass der Höck reibungslos verläuft. Dazu gehören unter anderem die Auswahl eines geeigneten Höckorts, die Festlegung von Zielen und Traktanden, sowie die Einladung der Teilnehmenden.
*   **Spiele**: Wenn du Spiele planst, solltest du sicherstellen, dass sie sich an die Sicherheitsanforderungen halten. Dazu gehören unter anderem die Auswahl von Spielen, die nicht zu gefährlich sind und die Bereitstellung von geeigneten Ausrüstungen.

Weitere Informationen findest du in der [J+S-Broschüre "LS/T - Spiel und Sport"](https://www.jugendundsport.ch/de/sportarten/lagersport-trekking-uebersicht/login-experten.html) oder im [Merkblatt LS-T 3x3 "Unterwegs sein"](https://www.jugendundsport.ch/content/jus-internet/de/sportarten/lagersport-trekking-uebersicht/_jcr_content/contentPar/tabs_copy_copy/items/dokumente/tabPar/downloadlist_copy/downloadItems/97_1494506483240.download/merkblatt_ls_t_3x3_unterwegs_sein_d.pdf).
```