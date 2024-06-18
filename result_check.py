from control import *


def right(board, position):
    if position[1] + 1 >= board.width:
        return 1
    elif board.board[position[0]][position[1]] == board.board[position[0]][position[1] + 1]:
        return 1 + right(board, (position[0], position[1] + 1))
    else:
        return 1


def up(board, position):
    if position[0] - 1 < 0:
        return 1
    elif board.board[position[0]][position[1]] == board.board[position[0] - 1][position[1]]:
        return 1 + up(board, (position[0] - 1, position[1]))
    else:
        return 1


def up_right(board, position):
    if position[0] - 1 < 0 or position[1] + 1 >= board.width:
        return 1
    elif board.board[position[0]][position[1]] == board.board[position[0] - 1][position[1] + 1]:
        return 1 + up_right(board, (position[0] - 1, position[1] + 1))
    else:
        return 1


def up_left(board, position):
    if position[0] - 1 < 0 or position[1] - 1 < 0:
        return 1
    elif board.board[position[0]][position[1]] == board.board[position[0] - 1][position[1] - 1]:
        return 1 + up_left(board, (position[0] - 1, position[1] - 1))
    else:
        return 1


def find_streak(board, beginning):
    if right(board, beginning) >= 4:
        return True
    elif up(board, beginning) >= 4:
        return True
    elif up_right(board, beginning) >= 4:
        return True
    elif up_left(board, beginning) >= 4:
        return True
    else:
        return False


def check_result(board, player):
    for row in range(board.height):
        for elem in range(board.width):
            if board.board[row][elem] == player:
                if find_streak(board, (row, elem)):
                    raise GameWon