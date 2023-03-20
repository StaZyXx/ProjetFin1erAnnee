from case import CaseType, BarrierType
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

    def can_place_barrier(self, x, y, barrier_type: BarrierType) -> bool:
        if barrier_type == BarrierType.HORIZONTAL:
            return self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL and \
                self.get_game().has_case(x + 1, y) and \
                self.get_game().get_case(x + 1, y).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL

        return self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL and \
            self.get_game().has_case(x, y - 1) and \
            self.get_game().get_case(x, y - 1).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL

    def place_barrier(self, x, y, barrier_type: BarrierType):
        if barrier_type == BarrierType.HORIZONTAL:
            self.get_game().get_case(x, y) \
                .set_case_type(CaseType.BARRIER) \
                .set_barrier_type(BarrierType.HORIZONTAL)
            self.get_game().get_case(x + 1, y) \
                .set_case_type(CaseType.BARRIER) \
                .set_barrier_type(BarrierType.HORIZONTAL)
        else:
            self.get_game().get_case(x, y) \
                .set_case_type(CaseType.BARRIER) \
                .set_barrier_type(BarrierType.VERTICAL)
            self.get_game().get_case(x, y - 1) \
                .set_case_type(CaseType.BARRIER) \
                .set_barrier_type(BarrierType.VERTICAL)

    def check_path(self, initialPosition: [int, int]):
        return False
