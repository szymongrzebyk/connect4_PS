
from board import *
from control import *
from player import *

clear_console()
board_width = 7
board_height = 6
board = GameBoard(board_width, board_height)
player1 = Player('O')
player2 = Player('X')
board.print()
while True:
    try:
        player1.make_move(board)
        player2.make_move(board)
    except GameWon:
        print("Game won! Congratulations!")
        break
