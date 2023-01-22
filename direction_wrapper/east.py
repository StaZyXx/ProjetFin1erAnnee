from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper
from game import Game


class East(DirectionWrapper):

    def __init__(self, game: Game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x + 4, y

    def can_adapt_for_jump(self, x, y):

        if not self.get_game().has_case(x + 2, y): return False
        if not self.get_game().get_case(x + 2, y).has_player(): return False
        if not self.get_game().has_case(x + 1, y): return False
        if self.get_game().get_case(x + 1, y).get_case_type() != CaseType.BARRIER_SLOT: return False
        if not self.get_game().has_case(x + 3, y): return False
        if self.get_game().get_case(x + 3, y).get_case_type() != CaseType.BARRIER_SLOT: return False
        return self.get_game().has_case(x + 4, y) and self.get_game().get_case(x + 4, y).get_case_type() == \
            CaseType.DEFAULT and not self.get_game().get_case(x + 4, y).has_player()

    def can_place_barrier(self, x, y):
        return self.get_game().get_case(x, y).get_case_type() == CaseType.BARRIER_SLOT and \
            self.get_game().has_case(x + 1, y) and self.get_game().get_case(x + 1, y).get_case_type() \
            == CaseType.BARRIER_SLOT
