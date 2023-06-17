from case import CaseType, BarrierType


class DirectionWrapper:

    def __init__(self, game):
        self.__game = game

    def get_game(self):
        return self.__game

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_adapt_for_jump(self, x, y, id):
        return False

    def can_move(self, location: [int, int], id) -> bool:
        return False

    def player_can_move(self, player):
        return self.can_move(player.get_location(), player.get_id())

    def player_can_jump(self, player):
        return self.can_adapt_for_jump(player.get_location()[0], player.get_location()[1], player.get_id())

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return

    def move(self, player):
        return

    def jump(self, player):
        return

    def can_place_barrier(self, x, y, barrier_type: BarrierType) -> bool:
        return False

    def place_barrier(self, x, y, barrier_type: BarrierType):
        return
