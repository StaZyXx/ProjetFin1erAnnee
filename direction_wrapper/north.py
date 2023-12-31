from case import CaseType
from direction_wrapper.direction_wrapper import DirectionWrapper


class North(DirectionWrapper):

    def __init__(self, game):
        super().__init__(game)

    def can_move(self, location: [int, int], id) -> bool:
        x, y = location
        if self.get_game().has_case(x - 2, y):
            if self.get_game().has_case(x - 1, y):
                if self.get_game().get_case(x - 1, y).get_case_type() == CaseType.BARRIER:
                    return False

            return self.get_game().get_case(x - 2, y).get_case_type() == CaseType.DEFAULT and not \
                self.get_game().get_case(x - 2, y).check_has_player_without_same_player(id)
        return False

    def adapt_for_move(self, location: [int, int]) -> [int, int]:
        return location[0] - 2, location[1]

    def move(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x - 2, y).set_player(player)
        player.set_location(x - 2, y)
        self.get_game().get_case(x, y).set_player(0)

    def adapt_for_jump(self, x, y) -> (int, int):
        return x - 4, y

    def jump(self, player):
        x, y = player.get_location()
        self.get_game().get_case(x - 4, y).set_player(player)
        player.set_location(x - 4, y)
        self.get_game().get_case(x, y).set_player(0)

    def can_adapt_for_jump(self, x, y, id):

        if not self.get_game().has_case(x - 2, y): return False
        if not self.get_game().get_case(x - 2, y).check_has_player_without_same_player(id): return False
        if not self.get_game().has_case(x - 1, y): return False
        if self.get_game().get_case(x - 1, y).get_case_type() == CaseType.BARRIER: return False
        if not self.get_game().has_case(x - 3, y): return False
        if self.get_game().get_case(x - 3, y).get_case_type() == CaseType.BARRIER: return False
        return self.get_game().has_case(x - 4, y) and self.get_game().get_case(x - 4, y).get_case_type() == \
            CaseType.DEFAULT and not self.get_game().get_case(x - 4, y).check_has_player_without_same_player(id)
