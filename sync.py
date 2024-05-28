import argparse
import requests
import lib

# Argumente von der Kommandozeile einlesen
parser = argparse.ArgumentParser(description='Clone or sync a specific board from one Nextcloud instance to another.')
parser.add_argument('--board', type=str, required=True, help='The title of the board to clone or sync.')
args = parser.parse_args()

# Board-Titel, den wir klonen oder synchronisieren möchten
board_to_clone = args.board

# Hole alle Boards von der Quellinstanz
source_boards = lib.getBoards()

# Finde das gewünschte Board in der Quellinstanz
board_to_clone_data = next((board for board in source_boards if board['title'] == board_to_clone), None)

if not board_to_clone_data:
    print(f'Board "{board_to_clone}" nicht gefunden.')
    exit()

boardIdFrom = board_to_clone_data['id']

# Hole alle Boards von der Zielinstanz
target_boards = lib.getBoards('to')

# Überprüfen, ob das Board in der Zielinstanz existiert
target_board_data = next((board for board in target_boards if board['title'] == board_to_clone), None)

if target_board_data:
    boardIdTo = target_board_data['id']
    print(f'Board "{board_to_clone}" already exists. Syncing...')
else:
    # Erstelle das Board in der Zielinstanz
    createdBoard = lib.createBoard(board_to_clone_data['title'], board_to_clone_data['color'])
    boardIdTo = createdBoard['id']
    print(f'Created board "{board_to_clone}"')

# Kopiere oder synchronisiere die Labels des Boards
boardDetails = lib.getBoardDetails(boardIdFrom)
labelsMap = {}
target_board_details = lib.getBoardDetails(boardIdTo,'to')

# Existierende Labels in der Zielinstanz sammeln
existing_labels = {label['title']: label['id'] for label in target_board_details['labels']}

for label in boardDetails['labels']:
    if label['title'] in existing_labels:
        labelsMap[label['id']] = existing_labels[label['title']]
    else:
        createdLabel = lib.createLabel(label['title'], label['color'], boardIdTo)
        labelsMap[label['id']] = createdLabel['id']

# Kopiere oder synchronisiere die Stacks und Karten des Boards
stacks = lib.getStacks(boardIdFrom)
target_stacks = lib.getStacks(boardIdTo,'to')
stacksMap = {}

# Existierende Stacks in der Zielinstanz sammeln
existing_stacks = {stack['title']: stack['id'] for stack in target_stacks}

for stack in stacks:
    if stack['title'] in existing_stacks:
        stackIdTo = existing_stacks[stack['title']]
        stacksMap[stack['id']] = stackIdTo
        print(f'  Stack "{stack["title"]}" already exists. Syncing...')
    else:
        createdStack = lib.createStack(stack['title'], stack['order'], boardIdTo)
        stackIdTo = createdStack['id']
        stacksMap[stack['id']] = stackIdTo
        print(f'  Created stack "{stack["title"]}"')

    if 'cards' in stack:
        for card in stack['cards']:
            try:
                lib.copyCard(card, boardIdTo, stackIdTo, labelsMap)
            except requests.exceptions.HTTPError as e:
                print(f'    Failed to create card "{card["title"]}". Error: {e}')
                print(f'    Response: {e.response.text}')
        print(f'    Created {len(stack["cards"])} cards')

# Kopiere oder synchronisiere die archivierten Stacks und Karten des Boards
archived_stacks = lib.getStacksArchived(boardIdFrom)
target_archived_stacks = lib.getStacksArchived(boardIdTo,'to')

# Existierende archivierte Stacks in der Zielinstanz sammeln
existing_archived_stacks = {stack['title']: stack['id'] for stack in target_archived_stacks}

for stack in archived_stacks:
    if stack['title'] in existing_archived_stacks:
        stackIdTo = existing_archived_stacks[stack['title']]
        print(f'  Archived stack "{stack['title']}" already exists. Syncing...')
    else:
        createdStack = lib.createStack(stack['title'], stack['order'], boardIdTo)
        stackIdTo = createdStack['id']
        stacksMap[stack['id']] = stackIdTo
        print(f'  Created archived stack "{stack['title']}"')

    if 'cards' in stack:
        for card in stack['cards']:
            try:
                lib.copyCard(card, boardIdTo, stackIdTo, labelsMap)
            except requests.exceptions.HTTPError as e:
                print(f'    Failed to create archived card "{card["title"]}". Error: {e}')
                print(f'    Response: {e.response.text}')
        print(f'    Created {len(stack["cards"])} archived cards')
