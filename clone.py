import argparse
import lib

# Argumente von der Kommandozeile einlesen
parser = argparse.ArgumentParser(description='Klonen eines bestimmten Boards von einer Nextcloud-Instanz zu einer anderen.')
parser.add_argument('--board', type=str, required=True, help='Der Titel des zu klonenden Boards.')
args = parser.parse_args()

# Board-Titel, den wir klonen möchten
board_to_clone = args.board

# Hole alle Boards von der Quellinstanz
boards = lib.getBoards()

# Finde das gewünschte Board
board_to_clone_data = next((board for board in boards if board['title'] == board_to_clone), None)

if not board_to_clone_data:
    print(f'Board "{board_to_clone}" nicht gefunden.')
else:
    boardIdFrom = board_to_clone_data['id']
    # Erstelle das Board in der Zielinstanz
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
        print(f'  Stapel "{stack['title']}" erstellt')

        if 'cards' in stack:
            for card in stack['cards']:
                lib.copyCard(card, boardIdTo, stackIdTo, labelsMap)
            print(f'    {len(stack["cards"])} Karten erstellt')

    # Kopiere die archivierten Stacks und Karten des Boards
    stacks = lib.getStacksArchived(boardIdFrom)
    for stack in stacks:
        if 'cards' in stack:
            print(f'  Stack "{stack['title']}"')
            for card in stack['cards']:
                lib.copyCard(card, boardIdTo, stacksMap[stack['id']], labelsMap)
            print(f'    {len(stack["cards"])} archivierte Karten erstellt')
