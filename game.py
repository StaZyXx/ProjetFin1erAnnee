from case import Case
from player import Player


class Game:

    def __init__(self):
        self.__player: list[Player] = []
        self.__board_size = 0

        self.__cases: list[list[Case]] = []

    def create_board(self):
        self.__cases = [[Case() for _ in range(self.__board_size)] for _ in range(self.__board_size)]
