# Nextcloud Deck importieren/exportieren

## Installation

1. git clone
2. Installiere Python, Pip
3. führe auf der Komandozeile aus:`pip install requests`
4. Kopiere die Datei "sample.config.py" nach "config.py" und trage dort die Daten zu deinen Nextcloudinstanzen ein


Um ein bestimmtes Deck auf eine andfere Nextcloud Instanz zu kopieren gibst du auf der Komandozeile an:

```python
python clone.py --"Name des Decks"
```
oder 
```python
python3 clone.py --"Name des Decks"
```

Um alle Decks zu kopieren, gibst du ein:

```python
python backup.py
```


Dank der großartigen Arbeit von @svbergerem:
https://gist.github.com/svbergerem/5914d7f87764901aefddba125af99938

### Funktionen des Skripts

1. **Daten von der Quellinstanz abrufen:**
   - `getBoards()`: Ruft die Liste aller Boards ab.
   - `getBoardDetails(boardId)`: Ruft Details eines spezifischen Boards ab.
   - `getStacks(boardId)`: Ruft die Stacks eines Boards ab.
   - `getStacksArchived(boardId)`: Ruft die archivierten Stacks eines Boards ab.
2. **Daten zur Zielinstanz übertragen:**
   - `createBoard(title, color)`: Erstellt ein Board.
   - `createLabel(title, color, boardId)`: Erstellt ein Label in einem Board.
   - `createStack(title, order, boardId)`: Erstellt einen Stack in einem Board.
   - `createCard(title, ctype, order, description, duedate, boardId, stackId)`: Erstellt eine Karte in einem Stack.
   - `assignLabel(labelId, cardId, boardId, stackId)`: Weist ein Label einer Karte zu.
   - `archiveCard(card, boardId, stackId)`: Archiviert eine Karte.
   - `copyCard(card, boardIdTo, stackIdTo, labelsMap)`: Kopiert eine Karte, einschließlich ihrer Labels und archiviertem Status.
