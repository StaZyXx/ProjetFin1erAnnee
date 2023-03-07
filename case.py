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
        self.__is_empty = True
        self.__player = None
        self.__case_type: CaseType = case_type

    def get_player(self):
        return self.__player

    def set_player(self, player):
        self.__player = player

    def has_player(self):
        return self.__player != 0

    def get_case_type(self) -> CaseType:
        return self.__case_type

    def set_case_type(self, case_type: CaseType):
        self.__case_type = case_type
