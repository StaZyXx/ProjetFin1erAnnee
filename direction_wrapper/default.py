from case import CaseType, BarrierType
from direction_wrapper.direction_wrapper import DirectionWrapper


class DefaultDirection(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_place_barrier(self, x, y, barrier_type: BarrierType) -> bool:

        if barrier_type == BarrierType.HORIZONTAL:
            return self.get_game().has_case(x,y) and self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL and \
                self.get_game().has_case(x, y + 2) and \
                self.get_game().get_case(x, y + 2).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL

        return self.get_game().has_case(x,y) and  self.get_game().get_case(x, y).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL and \
            self.get_game().has_case(x + 2, y) and \
            self.get_game().get_case(x + 2, y).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL

    def place_barrier(self, x, y, barrier_type: BarrierType):
        if barrier_type == BarrierType.HORIZONTAL:
            case = self.get_game().get_case(x, y)
            case.set_case_type(CaseType.BARRIER)
            case.set_barrier_type(BarrierType.HORIZONTAL)
            case = self.get_game().get_case(x, y + 2)
            case.set_case_type(CaseType.BARRIER)
            case.set_barrier_type(BarrierType.HORIZONTAL)
        else:
            case = self.get_game().get_case(x, y)
            case.set_case_type(CaseType.BARRIER)
            case.set_barrier_type(BarrierType.VERTICAL)
            case = self.get_game().get_case(x + 2, y)
            case.set_case_type(CaseType.BARRIER)
            case.set_barrier_type(BarrierType.VERTICAL)
