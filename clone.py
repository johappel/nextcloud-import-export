import argparse
import lib

# Argumente von der Kommandozeile einlesen
parser = argparse.ArgumentParser(description='Klonen eines bestimmten Boards von einer Nextcloud-Instanz zu einer anderen.')
parser.add_argument('--board', type=str, required=True, help='Der Titel des zu klonenden Boards.')
parser.add_argument('--replace', action='store_true', help='Ersetze das Board im Ziel, falls es bereits existiert.')
args = parser.parse_args()

# Board-Titel, den wir klonen möchten
board_to_clone = args.board

# Hole alle Boards von der Quellinstanz
boards_from = lib.getBoards()

# Finde das gewünschte Board
board_to_clone_data = next((board for board in boards_from if board['title'] == board_to_clone), None)

if not board_to_clone_data:
    print(f'Board "{board_to_clone}" nicht gefunden.')
else:
    boardIdFrom = board_to_clone_data['id']
    
    # Überprüfe, ob das Board im Ziel bereits existiert
    boards_to = lib.getBoards('to')
    existing_board_to = next((board for board in boards_to if board['title'] == board_to_clone and 0 == board['deletedAt']), None)
        
    # Löschen wenn der parameter --replace gesetzt wurde und das Board existiert
    if args.replace and existing_board_to:
        # Lösche das bestehende Board im Ziel
        print(f'Lösche Board: {existing_board_to["id"]}')
        lib.deleteBoard(existing_board_to['id'])
        print(f'Board "{board_to_clone}" im Ziel gelöscht')

    # Erstelle das Board in der Zielinstanz, wenn es nicht existiert oder ersetzt werden soll
    if not existing_board_to or args.replace:
        createdBoard = lib.createBoard(board_to_clone_data['title'], board_to_clone_data['color'])
        boardIdTo = createdBoard['id']
        print(f'Board "{board_to_clone}" erstellt')

        # Kopiere die Labels des Boards
        boardDetails = lib.getBoardDetails(boardIdFrom)
        labelsMap = {}
        for label in boardDetails['labels']:
            createdLabel = lib.createLabel(label['title'], label['color'], boardIdTo)
            labelsMap[label['id']] = createdLabel['id']

        # Kopiere die Stacks und Karten des Boards
        stacks = lib.getStacks(boardIdFrom)
        stacksMap = {}
        for stack in stacks:
            createdStack = lib.createStack(stack['title'], stack['order'], boardIdTo)
            stackIdTo = createdStack['id']
            stacksMap[stack['id']] = stackIdTo
            print(f'  Stapel "{stack["title"]}" erstellt')

            if 'cards' in stack:
                for card in stack['cards']:
                    lib.copyCard(card, boardIdTo, stackIdTo, labelsMap)
                print(f'    {len(stack["cards"])} Karten erstellt')

        # Kopiere die archivierten Stacks und Karten des Boards
        stacks = lib.getStacksArchived(boardIdFrom)
        for stack in stacks:
            if 'cards' in stack:
                print(f'  Stack "{stack["title"]}"')
                for card in stack['cards']:
                    lib.copyCard(card, boardIdTo, stacksMap[stack['id']], labelsMap)
                print(f'    {len(stack["cards"])} archivierte Karten erstellt')
    else:
        print(f'Board "{board_to_clone}" existiert bereits und wird nicht ersetzt (verwenden Sie --replace, um zu ersetzen).')
