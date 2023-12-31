from enum import Enum


class CaseType(Enum):
    DEFAULT = 0
    SLOT_BARRIER_HORIZONTAL = 1
    SLOT_BARRIER_VERTICAL = 2
    BARRIER = 3
    BLANK = 4


class BarrierType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Case:
    def __init__(self, case_type):
        self.__barrier_type = None
        self.__is_empty = True
        self.__player = 0
        self.__case_type: CaseType = case_type
        self.__who_place_barrier = None

    def get_player(self):
        return self.__player

    def set_player(self, player):
        self.__player = player

    def has_player(self):
        if self.__player is None:
            return False
        return self.__player != 0

    def check_has_player_without_same_player(self, player):
        if self.has_player():
            return self.__player.get_id() != player
        return False

    def get_case_type(self) -> CaseType:
        return self.__case_type

    def set_case_type(self, case_type: CaseType):
        self.__case_type = case_type

    def set_barrier_type(self, barrier_type: BarrierType):
        self.__barrier_type = barrier_type

    def get_barrier_type(self):
        return self.__barrier_type

    def set_who_place_barrier(self, player):
        self.__who_place_barrier = player

    def get_who_place_barrier(self):
        return self.__who_place_barrier
