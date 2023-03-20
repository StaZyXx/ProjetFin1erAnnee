from typing import List

from case import Case, CaseType, BarrierType
from direction import Direction
from direction_wrapper.default import DefaultDirection
from direction_wrapper.east import East
from direction_wrapper.north import North
from direction_wrapper.north_east import NorthEast
from direction_wrapper.north_west import NorthWest
from direction_wrapper.south import South
from direction_wrapper.south_east import SouthEast
from direction_wrapper.south_west import SouthWest
from direction_wrapper.west import West
from player import Player


class Game:

    def __init__(self):
        self.__player1: Player = None
        self.__player2: Player = None
        self.__player3: Player = None
        self.__player4: Player = None
        self.__player: List[Player] = []
        self.__board_size = 9
        self.__cases = []
        self.create_board()
        self.__is_started = True
        self.__direction_wrapper = {
            Direction.EAST: East(self),
            Direction.NORTH: North(self),
            Direction.NORTH_EAST: NorthEast(self),
            Direction.NORTH_WEST: NorthWest(self),
            Direction.SOUTH: South(self),
            Direction.SOUTH_EAST: SouthEast(self),
            Direction.SOUTH_WEST: SouthWest(self),
            Direction.WEST: West(self),
            Direction.DEFAULT: DefaultDirection(self)
        }
        self.__amount = {
            5: 12,
            7: 16,
            9: 20,
            11: 24,
        }

    def is_started(self):
        return self.__is_started

    def set_started(self, is_started: bool):
        self.__is_started = is_started

    def has_case(self, x, y):
        return len(self.__cases) > x and len(self.__cases[x]) > y

    def get_case(self, x, y) -> Case:
        return self.__cases[x][y]

    def create_board(self):
        size = self.__board_size * 2 - 1
        y = 2
        z = 2

        for _ in range(size):
            rows_cases = []
            if z % 2 == 0:
                for _ in range(size):
                    if y % 2 == 0:
                        rows_cases.append(Case(CaseType.DEFAULT))
                        y -= 1
                    else:
                        rows_cases.append(Case(CaseType.BARRIER))
                        y += 1
                z -= 1
            else:
                for _ in range(size):
                    if y % 2 == 0:
                        rows_cases.append(Case(CaseType.BLANK))
                        y -= 1
                    else:
                        rows_cases.append(Case(CaseType.BARRIER))
                        y += 1
                z -= 1
            self.__cases.append(rows_cases)

    def jump_player(self, player: Player, direction: Direction):
        player_location = player.get_location()
        location = self.__direction_wrapper[direction].adapt_for_jump(player_location[0], player_location[1])
        player.set_location(location[0], location[1])

    def place_barrier(self, x, y, barrier_type):
        direction = self.__direction_wrapper[Direction.DEFAULT]
        if direction.can_place_barrier(x, y, barrier_type):
            direction.place_barrier(x, y, barrier_type)

    def place_player(self, amount: int):  # A vérifier que les pions tombent bien au millieu du plateau
        self.__player1 = Player(1)
        self.__player2 = Player(2)
        self.__player1.set_location(self.__board_size * 2 - 1, self.__board_size - 1)  # Ce pion est en bas au millieu
        self.__player2.set_location(0, self.__board_size - 1)  # Ce joueur est en haut au millieu
        self.get_case(self.__board_size * 2 - 1, self.__board_size - 1).set_player(self.__player1)
        self.get_case(0, self.__board_size - 1).set_player(self.__player2)

        if amount == 4:
            self.__player3 = Player(3)
            self.__player4 = Player(4)
            self.__player3.set_location(self.__board_size - 1, 0)  # Ce joueur est a gauche au millieu
            self.__player4.set_location(self.__board_size - 1,
                                        self.__board_size * 2 - 1)  # Ce joueur est a droite au millieu
            self.get_case(self.__board_size - 1, 0).set_player(self.__player3)
            self.get_case(self.__board_size - 1, self.__board_size * 2 - 1).set_player(self.__player4)

    def check_all_path(self):
        for player in self.__player:
            if self.check_path(player):
                return True
        return False

    def check_path(self, player: Player):
        while self.check_win(player, player.get_location()):
            for direction in self.__direction_wrapper:
                if self.__direction_wrapper[direction].check_path(player.get_location()):
                    return True

    def check_win(self, player: Player, location: [int, int]):
        match (player.get_id()):
            case 1:
                if location[0] == 0:
                    return True
            case 2:
                if location[0] == self.__board_size * 2 - 1:
                    return True
            case 3:
                if location[1] == self.__board_size * 2 - 1:
                    return True
            case 4:
                if location[1] == 0:
                    return True
            case _:
                return False

    def check_winner(self):  # A tester
        if self.check_win(self.__player1, self.__player1.get_location()):
            return self.__player1
        if self.check_win(self.__player2, self.__player2.get_location()):
            return self.__player2
        if self.check_win(self.__player3, self.__player3.get_location()):
            return self.__player3
        if self.check_win(self.__player4, self.__player4.get_location()):
            return self.__player4
        return None

    def stop_game(self):
        self.__is_started = False

    def amount_barrier(self):
        return self.__amount[int(self.__board_size / 2 - 1)]
