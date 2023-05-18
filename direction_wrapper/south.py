from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class South(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def can_move(self, player):
        x, y = player.get_location()
        print(player.get_location())
        print(x, y, self.get_game().has_case(x + 2, y), self.get_game().get_case(x + 2, y).get_case_type())
        if self.get_game().has_case(x + 2, y):
            return self.get_game().get_case(x + 2, y).get_case_type() == CaseType.DEFAULT and not \
                self.get_game().get_case(x + 2, y).has_player()

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x + 2, y).set_player(player)
        player.set_location(x + 2, y)
        self.get_game().get_case(x, y).set_player(0)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x + 4, y

    def can_adapt_for_jump(self, x, y):
        if not self.get_game().has_case(x + 2, y): return False
        if not self.get_game().get_case(x + 2, y).has_player(): return False
        if not self.get_game().has_case(x + 1, y): return False
        if self.get_game().get_case(x + 1, y).get_case_type() != CaseType.SLOT_BARRIER_HORIZONTAL: return False
        if not self.get_game().has_case(x + 3, y): return False
        if self.get_game().get_case(x + 3, y).get_case_type() != CaseType.SLOT_BARRIER_HORIZONTAL: return False
        return self.get_game().has_case(x + 4, y) and self.get_game().get_case(x + 4, y).get_case_type() == \
            CaseType.DEFAULT and not self.get_game().get_case(x + 4, y).has_player()

    def can_place_barrier(self, x, y):
        return True
