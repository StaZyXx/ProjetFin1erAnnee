import random
import threading
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

    def start(self, size: int, players: int, amount_barrier, is_each_turn: bool):
        self.__board_size = size

        self.create_board()
        self.place_player(players, amount_barrier, is_each_turn)
        self.__is_started = True

    def is_started(self):
        return self.__is_started

    def change_is_started(self):
        self.__is_started = True

    def set_started(self, is_started: bool):
        self.__is_started = is_started

    def has_case(self, x, y):
        return len(self.__cases) > x >= 0 and len(self.__cases[x]) > y >= 0

    def get_case(self, x, y) -> Case:
        return self.__cases[x][y]

    def get_player(self, index: int) -> Player:
        return self.__player[index - 1]

    def get_current_player(self):
        return self.__current_player

    def create_board(self):
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
            print("Barrier placed at " + str(x) + " " + str(y) + " " + str(barrier_type))
            direction.place_barrier(x, y, barrier_type)
            if not self.check_all_path():
                print("Barrier removed at " + str(x) + " " + str(y) + " " + str(barrier_type))
                if barrier_type == BarrierType.HORIZONTAL:
                    self.get_case(x, y).set_case_type(CaseType.SLOT_BARRIER_HORIZONTAL)
                    self.get_case(x, y + 2).set_case_type(CaseType.SLOT_BARRIER_HORIZONTAL)
                else:
                    self.get_case(x, y).set_case_type(CaseType.SLOT_BARRIER_VERTICAL)
                    self.get_case(x + 2, y).set_case_type(CaseType.SLOT_BARRIER_VERTICAL)
                return False
        else:
            return False
        self.__current_player.decrease_amount_barrier()
        return True

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
        if self.check_winner() is not None:
            self.stop_game()
            return False

        dw = self.__direction_wrapper[direction]
        if dw.can_adapt_for_jump(self.__current_player.get_location()[0], self.__current_player.get_location()[1]):
            self.jump_player(self.__current_player, direction)
            self.switch_player()
            return True

        if dw.player_can_move(self.__current_player):
            dw.move(self.__current_player)
            self.switch_player()
            return True
        return False

    def get_cases_by_allowed_direction(self):
        cases = []
        for direction in self.__direction_wrapper:
            location = None
            if self.__direction_wrapper[direction].player_can_move(self.__current_player):
                location = self.__direction_wrapper[direction].adapt_for_move(self.__current_player.get_location())
            elif self.__direction_wrapper[direction].can_adapt_for_jump(self.__current_player.get_location()[0],
                                                                        self.__current_player.get_location()[1]):
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

    def place_player(self, amount: int, amount_barrier, is_each_turn):  # A vérifier que les pions tombent bien au millieu du plateau
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

        for index, player in enumerate(self.__player):
            self.check_path(player, has_win, index)

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
                    x, y = self.get_relative_location(location, direction)

                    if x == -1 or y == -1:
                        continue

                    print("check", index, player.get_id(), [x, y])
                    if self.check_win_with_location(player, [x, y]):
                        # Un chemin a été trouvé pour ce joueur

                        has_win[index] = True
                        return

                    new_location = (x, y)
                    if new_location not in explored_locations:
                        new_locations.append(new_location)
                        explored_locations.add(new_location)

            locations_to_explore = new_locations

    def get_relative_location(self, location: [int, int], direction: Direction):
        if self.__direction_wrapper[direction].can_move(location):
            return self.__direction_wrapper[direction].adapt_for_move(location)
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
        list_slot_barrier = []
        if random.randint(0, 100) < 29:
            for i in range(len(self.get_cases())):
                for j in range(len(self.get_cases()[i])):
                    if self.get_case(j, i).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                        list_slot_barrier.append((i, j, BarrierType.HORIZONTAL))
                    elif self.get_case(j, i).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                        list_slot_barrier.append((i, j, BarrierType.VERTICAL))

            barrier_index = random.randint(0, len(list_slot_barrier) - 1)
            x, y, case_type = list_slot_barrier[barrier_index]
            if self.place_barrier(y, x, case_type):
                self.switch_player()
        else:
            is_moving = False
            while not is_moving:
                direction = random.randint(0, len(self.__direction_wrapper) - 1)
                is_moving = self.move_player_with_direction(list(self.__direction_wrapper.keys())[direction])

    def stop_game(self):
        self.__is_started = False

    def amount_barrier(self):
        return self.__amount[int(self.__board_size / 2 - 1)]

    def get_cases(self) -> [[Case]]:
        return self.__cases
