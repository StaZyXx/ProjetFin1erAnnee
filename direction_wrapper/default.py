from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper
from game import Game


class DefaultDirection(DirectionWrapper):


    def __init__(self, game: Game):
        super().__init__(game)

    def get_game(self) -> Game:
        return self.__game

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_adapt_for_jump(self, x, y):
        return True

    def can_place_barrier(self, x, y) -> bool:
        return self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL and \
            self.get_game().has_case(x + 1, y) and \
            self.get_game().get_case(x + 1, y).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL

    def check_path(self, initialPosition: [int, int]):
        return False