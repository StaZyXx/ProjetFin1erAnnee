from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class SouthEast(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x, y - 4

    def can_move(self, location: [int, int]) -> bool:
        if not self.get_game().has_case(location[0] + 2, location[1] + 2):
            return False
        if self.get_game().get_case(location[0] + 2, location[1] + 2).has_player():
            return False
        if not self.get_game().has_case(location[0] + 2, location[1] + 1):
            return False
        if self.get_game().get_case(location[0] + 2,
                                    location[1] + 1).get_case_type() != CaseType.SLOT_BARRIER_VERTICAL:
            return False

        if not self.get_game().has_case(location[0] + 2, location[1]):
            return False

        return self.get_game().get_case(location[0] + 2, location[1]).has_player()

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return location[0] + 2, location[1] + 2

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x + 2, y + 2).set_player(player)
        player.set_location(x + 2, y + 2)
        self.get_game().get_case(x, y).set_player(0)

    def can_adapt_for_jump(self, x, y):
        return False
