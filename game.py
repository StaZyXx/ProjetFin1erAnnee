from typing import List

from case import Case
from player import Player


class Game:

    def __init__(self):
        self.__player: List[Player] = []
        self.__board_size = 0

        self.__cases: List[List[Case]] = []
        self.__is_started = True

    def is_started(self):
        return self.__is_started

    def set_started(self, is_started: bool):
        self.__is_started = is_started
