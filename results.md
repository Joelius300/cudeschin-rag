# Results (newer first)

This document contains some sample results of specific versions and is a way to track the performance
for doing adjustments later. Not all results, especially those in the beginning, were tracked.

## 73ae0992b9b4 (reverted)

### Changes since last version

- Switched from embedding-simliarity retrieval (vector store) to TF-IDF-similarity retrieval
- Retrieval performs significantly worse, so discard/revert it

### Examples

```markdown
Beim Planen eines J+S Lagersport (LS)-Blocks solltest du auf die folgenden Aspekte achten:

- Die Aktivitäten im LS-Block sind Teil der J+S-Aktivitäten, die sich in Lagersport (LS) und Lageraktivitäten (LA) unterteilen.
- Im Gegensatz zu den LA-Aktivitäten, die eher auf soziale Aspekte abzielen, konzentrieren sich LS-Aktivitäten auf sportliche und körperliche Herausforderungen.

Um einen erfolgreichen LS-Block zu planen, solltest du also sicherstellen, dass die Aktivitäten im Einklang mit den Zielen des J+S-Programms stehen und eine angemessene Balance zwischen Sport und Spaß bieten.
```

## 930819109e82

### Changes since last version

- Made sure to include "J+S" in the search prompt when querying about LA, LS or LP

### Works well

- Answers in German only
- Fast and fully offline
- Fairly deterministic and reliable despite small model
- Cites real links from retrieved context
- Retrieved chunks are relevant and sizable
- Answers correctly based on context
- Cites sources for retrieval

### Problems

- Links to local file sources with http
- Relies on hacky prompt tricks for specific questions
- Slow start-up because of in-memory vector store

### Examples

Query:
```markdown
Auf was muss ich beim Planen eines LS-Blocks achten?
```

```markdown
### Achtung beim Planen eines J+S Lagersport (LS)-Blocks
#### Rahmenbedingungen beachten
Beim Planen eines J+S Lagersport-Blocks müssen die folgenden Rahmenbedingungen berücksichtigt werden:
* Die Aktivität sollte mindestens 30 Minuten dauern.
* Sie sollte verteilt auf mindestens zwei Tageszeiten (Morgen, Mittag, Abend) sein.
* Insgesamt sollten pro Lagertag mindestens vier Stunden und maximal zwei Stunden als Lageraktivität veranschlagt werden.

#### Ziele des Lagersports
Der Lagersport soll altersgerechte, vielfältige und abwechslungsreiche Spiel- und Sportaktivitäten bieten. Dazu gehören:
* Freude an der vielfältigen Bewegung
* Erlebnis in der Gruppe
* Oft mit einfachen Mitteln umgesetzt
* Finden typischerweise in der Natur statt

#### Aktivitätsbereiche
Der Lagersport umfasst Aktivitäten in den Bereichen:
* Unterwegs sein (z.B. Wanderungen, Schneeschuhtouren)
* Sport (z.B. Ballspiele, Trendsportarten)
* Spiel (z.B. Spielturniere, Geländespiele)

Quelle: [cudeschin/content/de/03_Aktivitaet_LST.md](http://cudeschin/content/de/03_Aktivitaet_LST.md)
```

```markdown
**Achtung beim Planen eines J+S Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines J+S Lagersport (LS)-Blocks sollten Sie folgende Punkte beachten:

*   Die Aktivitäten sollten altersgerecht, vielfältig und abwechslungsreich sein.
*   Es sollte Freude an der Bewegung entstehen, insbesondere an vielfältigen Bewegungsgrundformen für Kinder.
*   Die Aktivitäten sollten oft in der Natur stattfinden.
*   Sie können in den Bereichen Unterwegs sein (z.B. Wanderungen), Sport (z.B. Ballspiele) und Spiel (z.B. Geländespiele) liegen.

**Rahmenbedingungen**
-------------------

Beachten Sie auch die Rahmenbedingungen für J+S-Aktivitäten:

*   Pro Lagertag sollten mindestens vier Stunden, maximal zwei Stunden davon als Lageraktivität, verteilt auf mindestens zwei Tageszeiten (Morgen, Mittag, Abend), verbleiben.
*   Die Dauer jeder Aktivität sollte mindestens 30 Minuten betragen.

Quelle: cudeschin/content/de/03_Aktivitaet_LST.md
```

```markdown
**Achtung beim Planen eines J+S Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines J+S Lagersport (LS)-Blocks sollten Sie folgende Punkte beachten:

*   Die Aktivität sollte mindestens 30 Minuten dauern.
*   Der Block sollte altersgerecht, vielfältig und abwechslungsreich sein und Freude an der Bewegung vermitteln.
*   Die Aktivität sollte oft in der Natur stattfinden und mit einfachen Mitteln umgesetzt werden.

Es ist auch wichtig zu beachten, dass Lagersport-Aktivitäten im Rahmen eines J+S-Lagers Teil einer größeren Struktur sind. Daher sollten Sie sicherstellen, dass die Aktivität gut in den Gesamtplan des Lagers passt und die erforderlichen Rahmenbedingungen erfüllt.

Quelle: [cudeschin/content/de/03_Aktivitaet_LST.md](cudeschin/content/de/03_Aktivitaet_LST.md)
```

## 94b0c680e3ec

- Model: llama3.1:8b-instruct-q5_K_M
- Temperature: 0.1
- Chunking: Markdown header based
- Retrieval: Semantic similarity with in-memory vector store
- Embedder: jina/jina-embeddings-v2-base-de

### Changes since last version

- Switched to LangChain retrieval, still using phidata for rest
- In-memory vector store instead of pgvector
- Different splitting method (markdown header based)

### Works well

- Answers in German only
- Fast and fully offline
- Fairly deterministic and reliable despite small model
- Cites real links from retrieved context
- Retrieved chunks are more relevant and sizable
- Answers correctly based on context
- Cites sources for retrieval

### Problems

- Still fetches some irrelevant chunks and misses some relevant ones
- Answer misses some details because of missing context
- Links to local file sources with http
- Slower than last version because of in-memory vector store

### Examples (non-cherry-picked)

Query:
```markdown
Auf was muss ich beim Planen eines LS-Blocks achten?
```

```markdown
**Achtung beim Planen eines Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines Lagersport-Blocks solltest du auf folgende Aspekte achten:

*   **Rahmenbedingungen klären**: Stelle sicher, dass alle notwendigen Informationen für die Planung vorliegen. Dazu gehören:
    *   Ort der Aktivität
    *   Art der Aktivität (z.B. Wanderung, Ballspiel)
    *   Teilnehmende (Anzahl, Alter, Wissen, Bedürfnisse, Interessen...)
    *   Anzahl und Qualifikation der Leitenden
    *   Zeitrahmen
    *   Jahreszeit/Wetterbedingungen
    *   Finanzielle Mittel
    *   Verfügbares Material
    *   Weitere Vorgaben oder Einschränkungen

Diese Informationen sind entscheidend, um sicherzustellen, dass die Aktivität altersgerecht und sicher durchgeführt werden kann.

**Ziel des Lagersports**
------------------------

Der Lagersport soll Freude an der Bewegung, Erlebnisse in der Gruppe und Abwechslung bieten. Dies kann mit einfachen Mitteln umgesetzt werden und findet oft in der Natur statt. Aktivitäten können im Bereich Unterwegs sein (z.B. Wanderungen), Sport (z.B. Ballspiele) oder Spiel (z.B. Geländespiele) liegen.

Quellen:

*   cudeschin/content/de/01_Aktivitaet_planen.md
*   cudeschin/content/de/03_Aktivitaet_LST.md
```

```markdown
**Achtung beim Planen eines Lagersport (LS)-Blocks**
=====================================================

Beim Planen eines Lagersport-Blocks solltest du auf folgende Aspekte achten:

*   **Rahmenbedingungen klären**: Stelle sicher, dass du alle notwendigen Informationen hast, bevor du mit der Planung beginnst. Dazu gehören:
    *   Der Ort, an dem die Aktivität stattfinden soll
    *   Die Art der Aktivität, die geplant wird
    *   Die Teilnehmenden (Anzahl, Alter, Wissen, Bedürfnisse, Interessen...)
    *   Die Anzahl der Leitenden
    *   Die verfügbare Zeit
    *   Die Jahreszeit oder das Wetter, in dem die Aktivität stattfinden soll
    *   Die finanziellen Mittel, die zur Verfügung stehen
    *   Das verfügbare Material
    *   Mögliche Vorgaben oder Einschränkungen

Diese Informationen sind wichtig, um sicherzustellen, dass deine Planung realistisch und sicher ist.

**Ziel des Lagersports**
------------------------

Der Lagersport soll altersgerechte, vielfältige und abwechslungsreiche Spiel- und Sportaktivitäten bieten. Dazu gehören:

*   Freude an der vielfältigen Bewegung
*   Erlebnis in der Gruppe
*   Oft mit einfachen Mitteln umgesetzt
*   Finden typischerweise in der Natur statt

Die Aktivitäten sollten in den Bereichen Unterwegs sein, Sport und Spiel stattfinden.

Quellen:

*   [cudeschin/content/de/03_Aktivitaet_LST.md](https://cudeschin/content/de/03_Aktivitaet_LST.md)
*   [cudeschin/content/de/01_Aktivitaet_planen.md](https://cudeschin/content/de/01_Aktivitaet_planen.md)
```

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

