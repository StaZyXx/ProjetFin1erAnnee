from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class NorthEast(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return 0, 0

    def can_move(self, location: [int, int], id) -> bool:
        if not self.get_game().has_case(location[0] - 2, location[1] + 2) or \
                self.get_game().get_case(location[0] - 2, location[1] + 2).check_has_player_without_same_player(id):
            return False
        if self.get_game().has_case(location[0], location[1] + 2) and \
                self.get_game().get_case(location[0], location[1] + 2).check_has_player_without_same_player(id) and \
                self.get_game().has_case(location[0], location[1] + 3) and \
                self.get_game().get_case(location[0], location[1] + 3).get_case_type() == CaseType.BARRIER and \
                self.get_game().get_case(location[0], location[1] + 1).get_case_type() != CaseType.BARRIER and \
                self.get_game().get_case(location[0] - 1, location[1] + 2).get_case_type() != CaseType.BARRIER:
            return True
        if self.get_game().has_case(location[0] - 2, location[1]) and \
            self.get_game().get_case(location[0] - 2, location[1]).check_has_player_without_same_player(id) \
            and self.get_game().has_case(location[0] - 3, location[1]) \
            and self.get_game().get_case(location[0] - 3, location[1]) \
                .get_case_type() == CaseType.BARRIER and \
            self.get_game().get_case(location[0] - 1, location[1]).get_case_type() != CaseType.BARRIER and \
            self.get_game().get_case(location[0] - 2, location[1] + 1).get_case_type() != CaseType.BARRIER:
            return True
        return False

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return location[0] - 2, location[1] + 2

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x - 2, y + 2).set_player(player)
        player.set_location(x - 2, y + 2)
        self.get_game().get_case(x, y).set_player(0)
