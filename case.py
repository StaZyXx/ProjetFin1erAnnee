from enum import Enum


class Case:
    def __init__(self, case_type):
        self.__is_empty = True
        self.__player = 0
        self.__case_type: CaseType = case_type
    def get_case_type(self):
        return self.__case_type

    def has_player(self):
        return self.__player != 0

class CaseType(Enum):
    DEFAULT = 0
    BARRIER_SLOT = 1
    BARRIER = 2
    BLANK = 3


#Ratio