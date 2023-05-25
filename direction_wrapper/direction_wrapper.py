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

    def can_move(self, location: [int, int]) -> bool:
        return True

    def player_can_move(self, player):
        return self.can_move(player.get_location())

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return
    def move(self, player):
        return

    def can_place_barrier(self, x, y, barrier_type: BarrierType) -> bool:
        return True

    def place_barrier(self, x, y, barrier_type: BarrierType):
        return
