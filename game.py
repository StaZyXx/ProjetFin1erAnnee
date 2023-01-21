from typing import List

from case import Case
from player import Player


class Game:

    def __init__(self):
        self.__player: List[Player] = []
        self.__board_size = 7
        self.__cases=[]
        self.__cases=self.create_board()
        
    def create_board(self):
        x=self.__board_size*2-1
        y=2
        z=2

        for _ in range (x):
            add = []
            if z%2==0:
                for _ in range (x):
                    if y%2==0:
                        add.append(Case(0))
                        y-=1
                    else:
                        add.append(Case(1))
                        y+=1
                z-=1
            else:
                for _ in range(x):
                    if y%2==0:
                        add.append(Case(2))
                        y-=1
                    else:
                        add.append(Case(1))
                        y+=1
                z-=1
            self.__cases.append(add)
        return self.__cases
    
