from control import *
from result_check import *
from player import *


class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[' ' for x in range(width)] for y in range(height)]

    def print(self):
        clear_console()
        for row in self.board:
            for elem in row:
                print('[%s]' % elem, end=' ')
            print("\b\n")
        for i in range(self.width):
            print(" %d _" % (i + 1), end='')
        print("\b\b\n")

    def fill(self, column, player):
        for row in range(1, self.height + 1):
            if self.board[-row][column] == ' ':
                self.board[-row][column] = player
                break
            elif row == self.width:
                raise ValueError
        self.print()