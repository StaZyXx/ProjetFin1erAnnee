from typing import List

from case import Case, CaseType
from direction import Direction
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
        self.__player: List[Player] = []
        self.__board_size = 7
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
            Direction.WEST: West(self)
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
        location = self.__direction_wrapper[direction].adapt_for_jump(player)
        player.set_location(location[0], location[1])

    def can_place_barrier(self, x1, x2, y1, y2):
        return self.__cases[x1][y1].get_case_type() == CaseType.BARRIER_SLOT and \
            self.__cases[x2][y2].get_case_type() == CaseType.BARRIER_SLOT

    def place_barrier(self, x1, x2, y1, y2):
        self.__cases[x1][y1].set_case_type(CaseType.BARRIER)
        self.__cases[x2][y2].set_case_type(CaseType.BARRIER)
