import requests
import config
import base64

urlFrom = config.urlFrom
authFrom = config.authFrom

urlTo = config.urlTo
authTo = config.authTo

headers = {'OCS-APIRequest': 'true', 'Content-Type': 'application/json'}

def make_request(method, endpoint, from_to='from', json=None):
    if from_to == 'from':
        url = urlFrom
        auth = authFrom
    else:  # from_to == 'to'
        url = urlTo
        auth = authTo

    response = requests.request(method, f'{url}{endpoint}', auth=auth, headers=headers, json=json)
    response.raise_for_status()
    return response.json()

def getBoards(from_to='from'):
    boards = make_request('GET', '/index.php/apps/deck/api/v1.0/boards', from_to)
    return [board for board in boards if 0 == board['deletedAt']]

def getBoardDetails(boardId, from_to='from'):
    return make_request('GET', f'/index.php/apps/deck/api/v1.0/boards/{boardId}', from_to)

def getStacks(boardId, from_to='from'):
    return make_request('GET', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks', from_to)

def getStacksArchived(boardId, from_to='from'):
    return make_request('GET', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/archived', from_to)

def createBoard(title, color):
    board = make_request('POST', '/index.php/apps/deck/api/v1.0/boards', 'to', json={'title': title, 'color': color})
    boardId = board['id']
    # remove all default labels
    for label in board['labels']:
        labelId = label['id']
        make_request('DELETE', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/labels/{labelId}', 'to')
    return board

def createLabel(title, color, boardId):
    return make_request('POST', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/labels', 'to', json={'title': title, 'color': color})

def createStack(title, order, boardId):
    return make_request('POST', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks', 'to', json={'title': title, 'order': order})

def createCard(title, ctype, order, description, duedate, boardId, stackId):
    try:
        return make_request('POST', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards', 'to', 
                            json={'title': title, 'type': ctype, 'order': order, 'description': description, 'duedate': duedate})
    except requests.exceptions.HTTPError as e:
        print(f"Error creating card: {e}")
        print(f"Response: {e.response.text}")
        raise

def assignLabel(labelId, cardId, boardId, stackId):
    make_request('PUT', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{cardId}/assignLabel', 'to', json={'labelId': labelId})

def archiveCard(card, boardId, stackId):
    card['archived'] = True
    make_request('PUT', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{card["id"]}', 'to', json=card)

def copyCard(card, boardIdTo, stackIdTo, labelsMap):
    print(f"Copying card '{card['title']}' to board {boardIdTo}, stack {stackIdTo}")
    createdCard = createCard(
        card['title'],
        card['type'],
        card['order'],
        card['description'],
        card['duedate'],
        boardIdTo,
        stackIdTo
    )

    # copy card labels
    if card['labels']:
        for label in card['labels']:
            assignLabel(labelsMap[label['id']], createdCard['id'], boardIdTo, stackIdTo)

    if card['archived']:
        archiveCard(createdCard, boardIdTo, stackIdTo)

# Löschfunktionen auf der Zielinstanz
def deleteBoard(boardId):
    make_request('DELETE', f'/index.php/apps/deck/api/v1.0/boards/{boardId}', 'to')

def deleteStacks(boardId):
    stacks = getStacks(boardId, 'to')
    for stack in stacks:
        make_request('DELETE', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stack["id"]}', 'to')

def deleteLabels(boardId):
    boardDetails = getBoardDetails(boardId, 'to')
    for label in boardDetails['labels']:
        make_request('DELETE', f'/index.php/apps/deck/api/v1.0/boards/{boardId}/labels/{label["id"]}', 'to')
