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

- Answers in German only
- Fast and fully offline
- Fairly deterministic and reliable despite small model
- Cites real links from retrieved context

### Problems

- Fetches irrelevant chunks (!!!)
- Answer includes irrelevant information based on wrongly retrieved chunks
- Does not answer the question with enough correct details

### Examples (non-cherry-picked)

Query:
```markdown
Auf was muss ich beim Planen eines LS-Blocks achten?
```

Answers:
```markdown
**Achtung beim Planen eines Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines LS-Blocks ist es wichtig, auf die Sicherheit und das Wohlbefinden der Teilnehmenden zu achten. Hier sind einige wichtige Punkte, die du beachten solltest:

*   **Sicherheitsaspekte**: Stelle sicher, dass alle notwendigen Sicherheitsmaßnahmen getroffen werden, wie z.B. die Einhaltung von Sicherheitsregeln und die Bereitstellung von geeigneten Ausrüstungen.
*   **Höck**: Wenn du einen Höck planst, solltest du dich an die Vorbereitungshinweise halten, um sicherzustellen, dass der Höck reibungslos verläuft. Dazu gehören unter anderem die Auswahl eines geeigneten Höckorts, die Festlegung von Zielen und Traktanden, sowie die Einladung der Teilnehmenden.
*   **Spiele**: Wenn du Spiele planst, solltest du sicherstellen, dass sie sich an die Sicherheitsanforderungen halten. Dazu gehören unter anderem die Auswahl von Spielen, die nicht zu gefährlich sind und die Bereitstellung von geeigneten Ausrüstungen.

Weitere Informationen findest du in der [J+S-Broschüre "LS/T - Spiel und Sport"](https://www.jugendundsport.ch/de/sportarten/lagersport-trekking-uebersicht/login-experten.html) oder im [Merkblatt LS-T 3x3 "Unterwegs sein"](https://www.jugendundsport.ch/content/jus-internet/de/sportarten/lagersport-trekking-uebersicht/_jcr_content/contentPar/tabs_copy_copy/items/dokumente/tabPar/downloadlist_copy/downloadItems/97_1494506483240.download/merkblatt_ls_t_3x3_unterwegs_sein_d.pdf).
```

```markdown
**Achtung beim Planen eines Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines LS-Blocks ist es wichtig, auf verschiedene Aspekte zu achten. Hier sind einige wichtige Punkte:

### Vorbereitung

*   **Höckort**: Wählen Sie einen ruhigen und gut erreichbaren Ort für den Höck.
*   **Ziel des Höcks**: Klären Sie das Ziel des Höcks und sammeln Sie Traktanden/Themen, um sie zu ordnen.
*   **Dauer des Höcks**: Bestimmen Sie die Dauer des Höcks und planen Sie Pausen ein.
*   **Einladung**: Versenden Sie eine frühzeitige Einladung mit allen wichtigen Informationen (Ort, Zeit, Traktanden, Unterlagen, Vorbereitung für Höckteilnehmende).
*   **Hilfsmittel und Unterlagen**: Bereiten Sie Hilfsmittel und Unterlagen vor.

### Ablauf

*   **Begrüßung & Einstimmung**: Beginnen Sie mit einer Begrüßung und Einstimmung.
*   **Ziel des Höcks**: Erklären Sie das Ziel des Höcks und geben Sie die Traktanden bekannt.
*   **Rollen verteilen**: Verteilen Sie Rollen wie Protokoll, Timekeeper usw.
*   **Ablauf entsprechend der Traktandenliste**: Führen Sie den Ablauf entsprechend der Traktandenliste durch.
*   **Aufgabenverteilung bis zum nächsten Höck**: Verteilen Sie Aufgaben bis zum nächsten Höck (Pendenzen).
*   **Zusammenfassung & Abschluss**: Fassen Sie das Ergebnis zusammen und schließen Sie den Höck ab.

### Regeln

*   **Pünktlich erscheinen**: Achten Sie darauf, dass alle pünktlich erscheinen.
*   **Beim Thema bleiben**: Bleiben Sie beim Thema und achten Sie auf die Zeit.
*   **Aktiv mitmachen**: Aktiv mitmachen und sich an der Diskussion beteiligen.
*   **Respektieren Sie die Meinungen anderer**: Respektieren Sie die Meinungen anderer und seien Sie offen für neue Ideen.

### Weitere Tipps

*   Beachten Sie auch die Sicherheitshinweise im [Merkblatt LS/T 3x3 "Unterwegs sein"](https://www.jugendundsport.ch/content/jus-internet/de/sportarten/lagersport-trekking-uebersicht/_jcr_content/contentPar/tabs_copy_copy/items/dokumente/tabPar/downloadlist_copy/downloadItems/97_1494506483240.download/merkblatt_ls_t_3x3_unterwegs_sein_d.pdf).
*   Überprüfen Sie auch die [J+S-Broschüre "LS/T - Spiel und Sport"](https://www.jugendundsport.ch/de/sportarten/lagersport-trekking-uebersicht/login-experten.html) für weitere Ideen und Tipps.
```