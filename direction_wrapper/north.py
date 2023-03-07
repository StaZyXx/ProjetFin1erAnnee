from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper
from game import Game


class North(DirectionWrapper):

    def __init__(self, game: Game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x, y - 4

    def can_adapt_for_jump(self, x, y):

        if not self.get_game().has_case(x, y - 2): return False
        if not self.get_game().get_case(x, y - 2).has_player(): return False
        if not self.get_game().has_case(x, y - 1): return False
        if self.get_game().get_case(x, y - 1).get_case_type() != CaseType.SLOT_BARRIER_HORIZONTAL: return False
        if not self.get_game().has_case(x, y - 3): return False
        if self.get_game().get_case(x, y - 3).get_case_type() != CaseType.SLOT_BARRIER_HORIZONTAL: return False
        return self.get_game().has_case(x, y - 4) and self.get_game().get_case(x, y - 4).get_case_type() == \
            CaseType.DEFAULT and not self.get_game().get_case(x, y - 4).has_player()

    def can_place_barrier(self, x, y):
        return self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL and \
            self.get_game().has_case(x, y - 1) and self.get_game().get_case(x, y -1).get_case_type() \
            == CaseType.SLOT_BARRIER_HORIZONTAL
