from projet_final.Case import Case


class Game:
    def __init__(self):
        self.__player = []
        self.__board_size = 0

    def board(self):
        self.__cases = [[Case() for _ in range(self.__board_size)] for _ in range(self.__board_size)]

    def player_move(self):
        self.__cases[0][0]
