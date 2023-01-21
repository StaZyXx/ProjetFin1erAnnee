from typing import List

from case import Case
from player import Player


class Game:

    def __init__(self):
        self.__player: List[Player] = []
        self.__board_size = 0

        self.__cases: List[List[Case]] = []
        
    def create_board(self):
        x=self.__board_size*2-1
        y,z=2,2
        board=[]

        for _ in range (x):
            add = []
            if z%2==0:
                for _ in range (x):
                    if y%2==0:
                        Case(0)
                        y-=1
                    else:
                        Case(1)
                        y+=1
                z-=1
            else:
                for _ in range(x):
                    if y%2==0:
                        Case(2)
                        y-=1
                    else:
                        Case(1)
                        y+=1
                z-=1
            board.append(add)
        return board
