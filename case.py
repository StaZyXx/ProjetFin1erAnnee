from enum import Enum


class Case:
    def __init__(self,type):
        self.__is_empty = True
        self.__player = 0
        self.__type_case = type
    def get_case(self):
        return self.__type_case

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

#Ratio