from datetime import datetime
from lib import *

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("_%Y-%m-%d-%H-%M-%S")

boards = getBoards()

# create boards
for board in boards:
    boardIdFrom = board['id']
    # create board
    createdBoard = createBoard(board['title']+dt_string, board['color'])
    boardIdTo = createdBoard['id']
    print('Created board', board['title'], dt_string)

    # create labels
    boardDetails = getBoardDetails(board['id'])
    labelsMap = {}
    for label in boardDetails['labels']:
        createdLabel = createLabel(label['title'], label['color'], boardIdTo)
        labelsMap[label['id']] = createdLabel['id']

    # copy stacks
    stacks = getStacks(boardIdFrom)
    stacksMap = {}
    for stack in stacks:
        createdStack = createStack(stack['title'], stack['order'], boardIdTo)
        stackIdTo = createdStack['id']
        stacksMap[stack['id']] = stackIdTo
        print('  Created stack', stack['title'])
        # copy cards
        if not 'cards' in stack:
            continue
        for card in stack['cards']:
            copyCard(card, boardIdTo, stackIdTo, labelsMap)
        print('    Created', len(stack['cards']), 'cards')

    # copy archived stacks
    stacks = getStacksArchived(boardIdFrom)
    for stack in stacks:
        # copy cards
        if not 'cards' in stack:
            continue
        print('  Stack', stack['title'])
        for card in stack['cards']:
            copyCard(card, boardIdTo, stacksMap[stack['id']], labelsMap)
        print('    Created', len(stack['cards']), 'archived cards')