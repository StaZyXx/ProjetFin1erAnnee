from case import CaseType, BarrierType


class DirectionWrapper:

    def __init__(self, game):
        self.__game = game

    def get_game(self):
        return self.__game

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_adapt_for_jump(self, x, y):
        return True

    def can_move(self, player):
        return True

    def move(self, player):
        return

    def jump(self, player):
        return

    def can_place_barrier(self, x, y, barrier_type: BarrierType) -> bool:
        return True

    def place_barrier(self, x, y, barrier_type: BarrierType):
        return

    def check_path(self, initialPosition: [int, int]):
        return False
