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
from view import View


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

    def start(self, size: int, players: int):
        self.__board_size = size

        self.create_board()
        self.place_player(players)
        self.__is_started = True

    def is_started(self):
        return self.__is_started

    def set_started(self, is_started: bool):
        self.__is_started = is_started

    def has_case(self, x, y):
        return len(self.__cases) > x >= 0 and len(self.__cases[x]) > y >= 0

    def get_case(self, x, y) -> Case:
        return self.__cases[x][y]

    def get_player(self, index: int) -> Player:
        return self.__player[index - 1]

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
        self.move_player_with_direction(direction)

    def move_player_with_direction(self, direction):
        if self.check_winner() is not None:
            self.stop_game()
            return
        dw = self.__direction_wrapper[direction]
        if dw.can_adapt_for_jump(self.__current_player.get_location()[0], self.__current_player.get_location()[1]):
            self.jump_player(self.__current_player, direction)
            self.switch_player()
            return
        print("can move " + str(dw.player_can_move(self.__current_player)))
        if dw.player_can_move(self.__current_player):
            dw.move(self.__current_player)
            self.switch_player()

    def place_player(self, amount: int):  # A vérifier que les pions tombent bien au millieu du plateau
        player1 = Player(1)
        player2 = Player(2)
        self.__player.append(player1)
        self.__player.append(player2)
        self.__current_player = player1

        player1.set_location(self.__board_size * 2 - 2, self.__board_size - 1)  # Ce pion est en bas au millieu
        player2.set_location(0, self.__board_size - 1)  # Ce joueur est en haut au millieu
        self.get_case(self.__board_size * 2 - 2, self.__board_size - 1).set_player(player1)
        self.get_case(0, self.__board_size - 1).set_player(player2)

        if amount == 4:
            player3 = Player(3)
            player4 = Player(4)
            self.__player.append(player3)
            self.__player.append(player4)
            player3.set_location(self.__board_size - 1, 0)  # Ce joueur est a gauche au millieu
            player4.set_location(self.__board_size - 1,
                                 self.__board_size * 2 - 2)  # Ce joueur est a droite au millieu
            self.get_case(self.__board_size - 1, 0).set_player(player3)
            self.get_case(self.__board_size - 1, self.__board_size * 2 - 2).set_player(player4)

    def check_all_path(self):
        print(self.__player)
        for player in self.__player:
            if not self.check_path(player):
                return False
        return True

    def check_path(self, player: Player):
        currentLocation = player.get_location()
        dict = []
        dict.append(currentLocation)
        for amount in range(10):
            for i in range(len(dict)):
                location = dict[i]
                for direction in Direction:
                    x, y = self.get_relative_location(location, direction)
                    if x == -1 or y == -1:
                        continue
                    print("x " + str(x) + " y " + str(y))

                    dict.append([x, y])

                    if self.check_win_with_location(player, [x, y]):
                        return True
                dict.remove(location)

    def get_relative_location(self, location: [int, int], direction: Direction):
        if self.__direction_wrapper[direction].can_move(location):
            return self.__direction_wrapper[direction].adapt_for_move(location)
        elif self.__direction_wrapper[direction].can_adapt_for_jump(location[0], location[1]):
            return self.__direction_wrapper[direction].adapt_for_jump(location[0], location[1])
        else:
            return -1, -1

    def check_win(self, player):
        return self.check_win_with_location(player, player.get_location())

    def check_win_with_location(self, player: Player, location: [int, int]):
        print("Check win " + str(player.get_id()) + " " + str(location))
        match (player.get_id()):
            case 1:
                if location[0] == 0:
                    print("Win 1")
                    return True
            case 2:
                if location[0] == self.__board_size * 2 - 2:
                    print("Win 2")
                    return True
            case 3:
                if location[1] == self.__board_size * 2 - 1:
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

    def stop_game(self):
        self.__is_started = False

    def amount_barrier(self):
        return self.__amount[int(self.__board_size / 2 - 1)]

    def get_cases(self) -> [[Case]]:
        return self.__cases


jeu = Game()

# TODO REMOVE ARGUMENT FOR REPLACE WITH GAME SELECTION ON VIEW
View(jeu)
