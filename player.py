from result_check import *


class Player:
    def __init__(self, mark):
        self.mark = mark

    def make_move(self, board):
        while True:
            try:
                chosen_column = int(input("In which column do you want to put your mark? (%s)\n" % self.mark))
                if chosen_column <= 0:
                    raise IndexError
                board.fill(chosen_column - 1, self.mark)
                check_result(board, self.mark)
                break
            except ValueError:
                board.print()
                print("There is no space.")
            except IndexError:
                board.print()
                print("No such a column, choose different number.")