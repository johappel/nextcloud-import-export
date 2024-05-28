# Nextcloud Deck importieren/exportieren

## Voraussetzung

[Python](https://www.python.org/downloads/) muss installiert sein. Du kannst diese [Anleitung](https://kinsta.com/de/wissensdatenbank/python-installieren/) nutzen.

## Optional: Git installieren

Installiere [Git](https://git-scm.com/book/de/v2/Erste-Schritte-Git-installieren): Das ermöglicht dir, die Skripte aktuell zu halten und dich an der Entwicklung zu beteiligen.

## Installation der Skripte

1. [Download](https://github.com/johappel/nextcloud-import-export/archive/refs/heads/main.zip) der Skripte oder mit Git 
   `git clone https://github.com/johappel/nextcloud-import-export.git`
2. Gehe in das Verzeichnis nextcloud-import-export (cd nextcloud-import-export)
3. Führe auf der Kommandozeile aus: `pip install requests`
4. Kopiere die Datei "sample.config.py" nach "config.py" und trage dort die Daten zu deinen Nextcloud-Instanzen ein.
5. Mit diesem Befehl auf der Kommandozeile holst du die neueste Version:
   `git pull`

## Anwendungsfälle

Um ein bestimmtes Deck auf eine andere Nextcloud-Instanz zu kopieren, gibst du auf der Kommandozeile einen der folgenden Befehle ein:

1. Um ein Deck zu kopieren:

```sh
python clone.py --board "Name des Decks"
```

2. Um ein bestehendes Deck auf der Zielinstanz zu löschen und zu ersetzen:

```sh
python sync.py --board "Name des Decks" --replace 
```

3. Um ein bestehendes Deck auf der Zielinstanz mit den Daten, Karten und Stacks der Originalinstanz synchron zu halten:

```sh
python sync.py --board "Name des Decks"
```

4. Um ein Backup aller Decks mit Datum des Backups im Titel auf der Zielinstanz zu sichern:

```sh
python backup.py
```

Dank der großartigen Arbeit von @svbergerem:
https://gist.github.com/svbergerem/5914d7f87764901aefddba125af99938

### Funktionen des Skripts

1. **Daten von der Quellinstanz abrufen:**
   Gib bei den folgenden Funktionen als Parameter 'from' oder 'to' ein, je nachdem, ob du die Daten von der Quellinstanz oder der Zielinstanz abfragst:
   - `getBoards(from_or_to)`: Ruft die Liste aller Boards ab.
   - `getBoardDetails(boardId, from_or_to)`: Ruft Details eines spezifischen Boards ab.
   - `getStacks(boardId, from_or_to)`: Ruft die Stacks eines Boards ab.
   - `getStacksArchived(boardId, from_or_to)`: Ruft die archivierten Stacks eines Boards ab.
2. **Daten zur Zielinstanz übertragen:**
   - `createBoard(title, color)`: Erstellt ein Board.
   - `createLabel(title, color, boardId)`: Erstellt ein Label in einem Board.
   - `createStack(title, order, boardId)`: Erstellt einen Stack in einem Board.
   - `createCard(title, ctype, order, description, duedate, boardId, stackId)`: Erstellt eine Karte in einem Stack.
   - `assignLabel(labelId, cardId, boardId, stackId)`: Weist einer Karte ein Label zu.
   - `archiveCard(card, boardId, stackId)`: Archiviert eine Karte.
   - `copyCard(card, boardIdTo, stackIdTo, labelsMap)`: Kopiert eine Karte, einschließlich ihrer Labels und des archivierten Status.
   - `deleteBoard(boardIdTo)`: Löscht ein Board.
   - `deleteStacks(boardIdTo)`: Löscht alle Listen eines Boards.
   - `deleteLabels(boardIdTo)`: Löscht alle Karten eines Boards.

# @todo:
   - Synchronisation verbessern (nur dezidierte Karten ersetzen)
   - Grafisches User Interface
