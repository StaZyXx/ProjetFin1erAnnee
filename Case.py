from enum import Enum
class Case:
    def __init__(self):
        self.__is_empty = True
        self.__player = 0
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    
#class Barrier:

