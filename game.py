from typing import List

from case import Case, CaseType
from player import Player


class Game:

    def __init__(self):
        self.__player: List[Player] = []
        self.__board_size = 7
        self.__cases = []
        self.create_board()
        self.__is_started = True

    def is_started(self):
        return self.__is_started

    def set_started(self, is_started: bool):
        self.__is_started = is_started

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
    def place_barrier(self,pose_barrier1x,pose_barrier2x,pose_barrier1y,pose_barrier2y):
        self.__cases[pose_barrier1x][pose_barrier1y].set_case_type(CaseType.BARRIER)
        self.__cases[pose_barrier2x][pose_barrier2y].set_case_type(CaseType.BARRIER)
