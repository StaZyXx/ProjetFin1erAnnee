from enum import Enum


class Case:
    def __init__(self, case_type):
        self.__is_empty = True
        self.__player = 0
        self.__case_type: CaseType = case_type
    def get_case(self):
        return self.__case_type

class CaseType(Enum):
    DEFAULT = 1
    BARRIER = 2
    BLANK = 3
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

#Ratio