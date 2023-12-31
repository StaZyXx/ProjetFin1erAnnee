from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class West(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x, y - 4

    def can_move(self, location: [int, int], id) -> bool:
        x, y = location
        if self.get_game().has_case(x, y - 2):
            if self.get_game().get_case(x, y - 1).get_case_type() == CaseType.BARRIER:
                return False
            return self.get_game().get_case(x, y - 2).get_case_type() == CaseType.DEFAULT and not \
                self.get_game().get_case(x, y - 2).check_has_player_without_same_player(id)
        return False

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return location[0], location[1] - 2

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x, y - 2).set_player(player)
        player.set_location(x, y - 2)
        self.get_game().get_case(x, y).set_player(0)

    def jump(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x, y - 4).set_player(player)
        player.set_location(x, y - 4)
        self.get_game().get_case(x, y).set_player(0)

    def can_adapt_for_jump(self, x, y, id):
        if not self.get_game().has_case(x, y - 2): return False
        if not self.get_game().get_case(x, y - 2).check_has_player_without_same_player(id): return False
        if not self.get_game().has_case(x, y - 1): return False
        if self.get_game().get_case(x, y - 1).get_case_type() == CaseType.BARRIER: return False
        if not self.get_game().has_case(x, y - 3): return False
        if self.get_game().get_case(x, y - 3).get_case_type() == CaseType.BARRIER: return False
        return self.get_game().has_case(x, y - 4) and self.get_game().get_case(x, y - 4).get_case_type() == \
            CaseType.DEFAULT and not self.get_game().get_case(x, y - 4).check_has_player_without_same_player(id)
