import random
from typing import List

from case import Case, CaseType, BarrierType
from direction import Direction
from direction_wrapper.default import DefaultDirection
from direction_wrapper.east import East
from direction_wrapper.north import North
from direction_wrapper.north_east import NorthEast
from direction_wrapper.north_west import NorthWest
from direction_wrapper.south import South
from direction_wrapper.south_east import SouthEast
from direction_wrapper.south_west import SouthWest
from direction_wrapper.west import West
from player import Player


class Game:

    def __init__(self):
        self.__current_player = None
        self.__player: List[Player] = []
        self.__board_size = 0
        self.__cases = []
        self.__is_started = True
        self.__direction_wrapper = {
            Direction.EAST: East(self),
            Direction.NORTH: North(self),
            Direction.NORTH_EAST: NorthEast(self),
            Direction.NORTH_WEST: NorthWest(self),
            Direction.SOUTH: South(self),
            Direction.SOUTH_EAST: SouthEast(self),
            Direction.SOUTH_WEST: SouthWest(self),
            Direction.WEST: West(self),
            Direction.DEFAULT: DefaultDirection(self)
        }
        self.__amount = {
            5: 12,
            7: 16,
            9: 20,
            11: 24,
        }

        self.__winner = None

    def start(self, size: int, players: int, amount_barrier, is_each_turn: bool):
        self.__is_each_turn = is_each_turn
        self.__board_size = size
        self.__amount_players = players
        self.__amount_barrier = amount_barrier

        self.create_board()
        self.place_player(players, amount_barrier, is_each_turn)
        self.__is_started = True

    def get_is_each_turn(self):
        return self.__is_each_turn

    def is_started(self):
        return self.__is_started

    def change_is_started(self):
        self.__is_started = True

    def change_is_started_for_false(self):
        self.__is_started = False

    def set_started(self, is_started: bool):
        self.__is_started = is_started

    def has_case(self, x, y):
        return len(self.__cases) > x >= 0 and len(self.__cases[x]) > y >= 0

    def get_case(self, x, y) -> Case:
        return self.__cases[x][y]

    def get_players(self):
        return self.__player

    def get_player(self, index: int) -> Player:
        return self.__player[index - 1]

    def get_current_player(self):
        return self.__current_player

    def get_winner(self):
        return self.__winner

    def create_board(self):
        self.__cases = []
        size = self.__board_size * 2 - 1
        y = 2
        z = 2

        for _ in range(size):
            rows_cases = []
            if z % 2 == 0:
                for _ in range(size):
                    if y % 2 == 0:
                        rows_cases.append(Case(CaseType.DEFAULT))
                        y -= 1
                    else:
                        rows_cases.append(Case(CaseType.SLOT_BARRIER_VERTICAL))
                        y += 1
                z -= 1
            else:
                for _ in range(size):
                    if y % 2 == 0:
                        rows_cases.append(Case(CaseType.BLANK))
                        y -= 1
                    else:
                        rows_cases.append(Case(CaseType.SLOT_BARRIER_HORIZONTAL))
                        y += 1
                z -= 1
            self.__cases.append(rows_cases)

    def jump_player(self, player: Player, direction: Direction):
        self.__direction_wrapper[direction].jump(player)

    def place_barrier(self, x, y, barrier_type):
        if self.__current_player.get_amount_barrier() <= 0:
            return False
        direction = self.__direction_wrapper[Direction.DEFAULT]
        if direction.can_place_barrier(x, y, barrier_type):
            direction.place_barrier(x, y, barrier_type)
            if barrier_type == BarrierType.HORIZONTAL:
                self.get_case(x, y).set_who_place_barrier(self.__current_player.get_id())
                self.get_case(x, y + 2).set_who_place_barrier(self.__current_player.get_id())
            else:
                self.get_case(x, y).set_who_place_barrier(self.__current_player.get_id())
                self.get_case(x + 2, y).set_who_place_barrier(self.__current_player.get_id())
            if not self.check_all_path():
                self.remove_barrier(x, y, barrier_type)
                return False
        else:
            return False
        return True

    def remove_barrier(self, x, y, barrier_type):
        if barrier_type == BarrierType.HORIZONTAL:
            self.get_case(x, y).set_case_type(CaseType.SLOT_BARRIER_HORIZONTAL)
            self.get_case(x, y + 2).set_case_type(CaseType.SLOT_BARRIER_HORIZONTAL)
        else:
            self.get_case(x, y).set_case_type(CaseType.SLOT_BARRIER_VERTICAL)
            self.get_case(x + 2, y).set_case_type(CaseType.SLOT_BARRIER_VERTICAL)

    def determine_direction(self, y, x):
        playerY, playerX = self.__current_player.get_location()

        if self.__current_player.get_id() == 2:
            if playerX + 1 == x:
                return Direction.SOUTH
        if playerX == x:
            if playerY > y:
                return Direction.NORTH
            else:
                return Direction.SOUTH
        elif playerY == y:
            if playerX > x:
                return Direction.WEST
            else:
                return Direction.EAST
        elif playerX > x:
            if playerY > y:
                return Direction.NORTH_WEST
            else:
                return Direction.SOUTH_WEST
        elif playerX < x:
            if playerY > y:
                return Direction.NORTH_EAST
            else:
                return Direction.SOUTH_EAST

    def move_player(self, x, y):
        direction = self.determine_direction(x, y)
        return self.move_player_with_direction(direction)

    def move_player_with_direction(self, direction):
        dw = self.__direction_wrapper[direction]
        if dw.player_can_jump(self.__current_player):
            self.jump_player(self.__current_player, direction)
            winner = self.check_winner()
            if winner  is not None:
                self.__winner = winner
                self.stop_game()
                return False
            self.switch_player()
            return True

        if dw.player_can_move(self.__current_player):
            dw.move(self.__current_player)
            winner = self.check_winner()
            if self.check_winner() is not None:
                self.__winner = winner
                self.stop_game()
                return False
            self.switch_player()
            return True
        return False

    def get_cases_by_allowed_direction(self):
        cases = []
        for direction in self.__direction_wrapper:
            location = None
            if self.__direction_wrapper[direction].player_can_move(self.__current_player):
                location = self.__direction_wrapper[direction].adapt_for_move(self.__current_player.get_location())
            elif self.__direction_wrapper[direction].player_can_jump(self.__current_player):
                location = self.__direction_wrapper[direction].adapt_for_jump(self.__current_player.get_location()[0],
                                                                              self.__current_player.get_location()[1])
            if location is not None:
                cases.append(self.get_case(location[0], location[1]))
        return cases

    def is_case_allowed_by_location(self, x, y):
        for case in self.get_cases_by_allowed_direction():
            if case == self.get_case(x, y):
                return True
        return False

    def is_case_allowed(self, case_target):
        for case in self.get_cases_by_allowed_direction():
            if case == case_target:
                return True
        return False

    def place_player(self, amount: int, amount_barrier,
                     is_each_turn):  # A vérifier que les pions tombent bien au millieu du plateau
        player1 = Player(1)
        player1.set_amount_barrier(amount_barrier / amount)
        player2 = Player(2)
        player2.set_amount_barrier(amount_barrier / amount)
        if not is_each_turn:
            player2.set_bot()
        self.__player.append(player1)
        self.__player.append(player2)
        self.__current_player = player1

        player1.set_location(self.__board_size * 2 - 2, self.__board_size - 1)  # Ce pion est en bas au millieu
        player2.set_location(0, self.__board_size - 1)  # Ce joueur est en haut au millieu
        self.get_case(self.__board_size * 2 - 2, self.__board_size - 1).set_player(player1)
        self.get_case(0, self.__board_size - 1).set_player(player2)

        if amount == 4:
            player3 = Player(3)
            player3.set_amount_barrier(amount_barrier / amount)
            if not is_each_turn:
                player3.set_bot()
            player4 = Player(4)
            player4.set_amount_barrier(amount_barrier / amount)
            if not is_each_turn:
                player4.set_bot()
            self.__player.append(player3)
            self.__player.append(player4)
            player3.set_location(self.__board_size - 1, 0)  # Ce joueur est a gauche au millieu
            player4.set_location(self.__board_size - 1,
                                 self.__board_size * 2 - 2)  # Ce joueur est a droite au millieu
            self.get_case(self.__board_size - 1, 0).set_player(player3)
            self.get_case(self.__board_size - 1, self.__board_size * 2 - 2).set_player(player4)

    def check_all_path(self):
        has_win = [False] * len(self.__player)

        for i in range(len(self.__player)):
            self.check_path(self.__player[i], has_win, i)

        for win in has_win:
            if not win:
                return False
        return True

    def check_path(self, player: Player, has_win, index):
        currentLocation = player.get_location()
        locations_to_explore = [currentLocation]  # Liste des positions à explorer
        explored_locations = set()  # Ensemble des positions explorées

        for amount in range(self.__board_size * 2 - 1):
            new_locations = []  # Liste temporaire pour stocker les nouvelles positions à explorer
            for location in locations_to_explore:
                for direction in Direction:
                    x, y = self.get_relative_location(location, player.get_id(), direction)

                    if x == -1 or y == -1:
                        continue

                    if self.check_win_with_location(player, [x, y]):
                        # Un chemin a été trouvé pour ce joueur

                        has_win[index] = True
                        return

                    new_location = (x, y)
                    if new_location not in explored_locations:
                        new_locations.append(new_location)
                        explored_locations.add(new_location)

            locations_to_explore = new_locations

    def get_relative_location(self, location: [int, int], id, direction: Direction):
        if self.__direction_wrapper[direction].can_move(location, id):
            return self.__direction_wrapper[direction].adapt_for_move(location)
        elif self.__direction_wrapper[direction].can_adapt_for_jump(location[0], location[1], id):
            return self.__direction_wrapper[direction].adapt_for_jump(location[0], location[1])
        else:
            return -1, -1

    def check_win(self, player):
        return self.check_win_with_location(player, player.get_location())

    def check_win_with_location(self, player: Player, location: [int, int]):
        match (player.get_id()):
            case 1:
                if location[0] == 0:
                    return True
            case 2:
                if location[0] == self.__board_size * 2 - 2:
                    return True
            case 3:
                if location[1] == self.__board_size * 2 - 2:
                    return True
            case 4:
                if location[1] == 0:
                    return True
            case _:
                return False

    def check_winner(self):  # A tester
        if not self.__is_started:
            return None
        if self.check_win(self.get_player(1)):
            return self.get_player(1)
        if self.check_win(self.get_player(2)):
            return self.get_player(2)
        if len(self.__player) == 4:
            if self.check_win(self.get_player(3)):
                return self.get_player(3)
            if self.check_win(self.get_player(4)):
                return self.get_player(4)
        return None

    def switch_player(self):
        if len(self.__player) == 4:
            if self.__current_player == self.get_player(1):
                self.__current_player = self.get_player(2)
            elif self.__current_player == self.get_player(2):
                self.__current_player = self.get_player(3)
            elif self.__current_player == self.get_player(3):
                self.__current_player = self.get_player(4)
            else:
                self.__current_player = self.get_player(1)
        else:
            if self.__current_player == self.get_player(1):
                self.__current_player = self.get_player(2)
            else:
                self.__current_player = self.get_player(1)
        if self.__current_player.is_bot():
            self.move_bot()

    def move_bot(self):
        if not self.__is_started:
            return
        list_slot_barrier = []
        if random.randint(0, 100) < 29:
            if not self.place_intelligent_barrier():
                for i in range(len(self.get_cases())):
                    for j in range(len(self.get_cases()[i])):
                        if self.get_case(j, i).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                            list_slot_barrier.append((i, j, BarrierType.HORIZONTAL))
                        elif self.get_case(j, i).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                            list_slot_barrier.append((i, j, BarrierType.VERTICAL))

                has_place = False
                amount_try = 50
                while not has_place and amount_try > 0:
                    amount_try -= 1
                    barrier_index = random.randint(0, len(list_slot_barrier) - 1)
                    x, y, case_type = list_slot_barrier[barrier_index]
                    if self.place_barrier(y, x, case_type):
                        has_place = True
                        self.switch_player()
                if amount_try == 0:
                    is_moving = False
                    while not is_moving:
                        if not self.is_started():
                            return
                        direction = random.randint(0, len(self.__direction_wrapper) - 1)
                        is_moving = self.move_player_with_direction(list(self.__direction_wrapper.keys())[direction])
            else:
                self.get_current_player().decrease_amount_barrier()
                self.switch_player()
        else:
            if not self.move_intelligent():
                is_moving = False
                while not is_moving:
                    if not self.is_started():
                        return
                    direction = random.randint(0, len(self.__direction_wrapper) - 1)
                    is_moving = self.move_player_with_direction(list(self.__direction_wrapper.keys())[direction])

    def move_intelligent(self):
        can_move = True
        x, y = self.get_current_player().get_location()
        if self.get_current_player().get_id() == 2:
            for i in range(x + 1, self.__board_size * 2, 2):
                if self.has_case(i, y) and self.get_case(i, y).get_case_type() == CaseType.BARRIER:
                    can_move = False
            if can_move:
                self.move_player_with_direction(Direction.SOUTH)

        if self.get_current_player().get_id() == 3:
            for i in range(y + 1, self.__board_size * 2, 2):
                if self.has_case(x, i) and self.get_case(x, i).get_case_type() == CaseType.BARRIER:
                    can_move = False
            if can_move:
                self.move_player_with_direction(Direction.EAST)

        if self.get_current_player().get_id() == 4:
            for i in range(y - 1, 1, -2):
                if self.has_case(x, i) and self.get_case(x, i).get_case_type() == CaseType.BARRIER:
                    can_move = False
            if can_move:
                self.move_player_with_direction(Direction.WEST)

        return can_move

    def place_intelligent_barrier(self):
        if self.__current_player.get_id() == 2:
            target = self.get_player(1)
            x, y = target.get_location()
            if self.place_barrier(x - 1, y, BarrierType.HORIZONTAL):
                return True
            elif self.place_barrier(x, y + 1, BarrierType.VERTICAL):
                return True
            elif self.place_barrier(x, y - 1, BarrierType.VERTICAL):
                return True
        if self.__current_player.get_id() == 3:
            target = self.get_player(4)
            x, y = target.get_location()
            if self.place_barrier(x, y - 1, BarrierType.VERTICAL):
                return True
            elif self.place_barrier(x - 1, y, BarrierType.HORIZONTAL):
                return True
            elif self.place_barrier(x + 1, y, BarrierType.HORIZONTAL):
                return True
        if self.__current_player.get_id() == 4:
            target = self.get_player(3)
            x, y = target.get_location()
            if self.place_barrier(x, y + 1, BarrierType.VERTICAL):
                return True
            elif self.place_barrier(x - 1, y, BarrierType.HORIZONTAL):
                return True
            elif self.place_barrier(x + 1, y, BarrierType.HORIZONTAL):
                return True

    def stop_game(self):
        self.__is_started = False
        self.__player = []

    def restart(self):
        self.__is_started = True
        self.start(self.__board_size, self.__amount_players, self.__amount_barrier, self.__is_each_turn)

    def amount_barrier(self):
        return self.__amount[int(self.__board_size / 2 - 1)]

    def get_cases(self) -> [[Case]]:
        return self.__cases
