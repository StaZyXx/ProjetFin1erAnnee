from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class NorthEast(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_move(self, location: [int, int]) -> bool:
        return False
        #TODO CHECK CONSIGNE

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return location[0] + 1, location[1] - 2

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x + 1, y - 2).set_player(player)
        player.set_location(x + 1, y - 2)
        self.get_game().get_case(x, y).set_player(0)

    def can_adapt_for_jump(self, x, y):
        return False
