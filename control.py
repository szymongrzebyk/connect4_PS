import os


def clear_console():
    command = "clear"
    os.system(command)


class GameWon(Exception):
    pass


class WrongPass(Exception):
    pass
