import threading

from game import Game
from network import Server, receipt_message_client, Client


class Multiplayer(Game):

    def __init__(self, is_server, nbr_player, client=None):
        self.__current_player_for_sends_and_receive = 0

        self.__if_had_play = False

        self.__nbr_player = nbr_player
        self.__is_server = is_server

        if is_server:
            self.__server = Server()
        else:
            self.__client = client
        super().__init__()

    def get_server(self):
        return self.__server

    def is_server(self):
        return self.__is_server

    def get_client(self) -> Client:
        return self.__client

    def get_have_play(self):
        return self.__if_had_play

    def change_have_play(self):
        self.__if_had_play = False

    def receive_move_player_with_direction_client(
            self):  # permet la réception des messages, et faire jouer le player. (coté client)
        move = self.__client.receipt_message_client()
        self.action_player(move)
        self.__if_had_play = True

    def receive_move_player_with_direction_server(
            self):  # permet la réception des messages, et faire jouer le player. (coté client)
        client = None
        if self.__current_player_for_sends_and_receive == 1:
            client = self.__server.get_client1()
        elif self.__current_player_for_sends_and_receive == 2:
            client = self.__server.get_client2()
        elif self.__current_player_for_sends_and_receive == 3:
            client = self.__server.get_client3()
        move = receipt_message_client(client)
        self.__server.send_message_server_all_client(move, self.__current_player_for_sends_and_receive)
        self.action_player(move)
        self.__if_had_play = True

    def action_player(self, move):
        if move["type"] == "move":
            direction = move["direction"]
            super().move_player_with_direction(direction)
        elif move["type"] == "barrier":
            x, y, barrier_type = move["x"], move["y"], move["barrier_type"]
            if super().place_barrier(x, y, barrier_type):
                self.switch_player()

    def place_barrier(self, x, y, barrier_type):
        if (self.__is_server and self.__current_player_for_sends_and_receive == 0) or (
                not self.__is_server and self.__current_player_for_sends_and_receive == self.__client.get_me_player()):
            can_place_bar = super().place_barrier(x, y, barrier_type)
            if can_place_bar:
                # permet l'envoie du dico avec les infos
                dico = {"type": "barrier", "x": x, "y": y, "barrier_type": barrier_type}
                if self.__is_server:
                    self.__server.send_message_server_all_client(dico, None)
                else:
                    self.__client.send_message_client(dico)
                self.switch_player()

    def move_player_with_direction(self, direction):
        if (self.__is_server and self.__current_player_for_sends_and_receive == 0) or (
                not self.__is_server and self.__current_player_for_sends_and_receive == self.__client.get_me_player()):
            result = super().move_player_with_direction(direction)
            dico = {"type": "move", "direction": direction}
            if result == 1:
                if self.__is_server:
                    self.__server.send_message_server_all_client(dico, None)
                else:
                    self.__client.send_message_client(dico)

    def switch_player(self):
        super().switch_player()
        if self.__current_player_for_sends_and_receive != self.__nbr_player - 1:
            self.__current_player_for_sends_and_receive += 1
        else:
            self.__current_player_for_sends_and_receive = 0

        #self.managements_sends()

        print(f"c'est au joueur {self.__current_player_for_sends_and_receive} !")

    def managements_sends(self):
        if (not self.__is_server or self.__current_player_for_sends_and_receive != 0) and (
                self.__is_server or self.__current_player_for_sends_and_receive != self.__client.get_me_player()):
            thread = threading.Thread(target=self.receive_movement)  # création du thread
            thread.start()

    def receive_movement(self):
        if self.__is_server:
            self.receive_move_player_with_direction_server()
        else:
            self.receive_move_player_with_direction_client()

    def wait_for_all_players(self):
        self.__server.add_all_player(self.__nbr_player)
