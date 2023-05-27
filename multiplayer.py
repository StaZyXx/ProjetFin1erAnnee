from game import Game
from network import Network, Client


class Multiplayer(Game):

    def __init__(self, network: Network):
        super().__init__()
        self.__network: Network = network
        while True:
            self.receive_message()

    #TODO : get the current client and send the message to all the other clients
    def move_player_with_direction(self, direction):
        super().move_player_with_direction(direction)
        self.__network.get_server().send_message_server_all_client({"type": "move", "direction": direction},
                                                                   self.__network.get_clients())

    def start(self, size: int, players: int):
        super().start(size, players)
        self.__network.get_server().send_message_server_all_client({"type": "start", "size": size, "players": players},
                                                                   self.__network.get_clients())

    def join_game(self, address_ip):
        self.__network.add_client(Client(address_ip))

    def receive_message(self):
        message = self.__network.get_initial_client().receipt_message_client()

        print(message)
