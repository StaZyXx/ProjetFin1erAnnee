import pickle
import socket


class Client:
    def __init__(self, address_ip):
        self.__address = address_ip
        print(self.__address)
        self.__host, self.__port = (self.__address, 4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__me_player = None

    def get_me_player(self):
        return self.__me_player

    def connect(self):  # renvoie 1 si il a réussi à se co et 0 dans l'autre cas
        try:
            self.__socket.connect((self.__host, self.__port))
            self.__me_player = int(self.receive_text_client())
            print(f"je suis palyer {self.__me_player}")
        except socket.error:
            return 0
        return self.__me_player

    def receipt_message_client(self):
        data = b''
        chunk = self.__socket.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        return received_list

    def send_message_client(self, message):
        serialized_list = pickle.dumps(message)
        self.__socket.sendall(serialized_list)

    def receive_text_client(self):
        data = self.__socket.recv(1024)
        data = data.decode("utf8")
        return data


def receipt_message_client(recipient):
    data = b''
    chunk = recipient.recv(4096)
    data += chunk
    received_list = pickle.loads(data)
    return received_list


def send_message_server(recipient, message):
    serialized_list = pickle.dumps(message)
    recipient.sendall(serialized_list)





class Server:
    def __init__(self):
        self.__host, self.__post = ('', 4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host, self.__post))
        self.__me_player = 0
        self.__player_had_join = None
        self.__client1, self.address1 = None, None
        self.__client2, self.address2 = None, None
        self.__client3, self.address3 = None, None

    def close_socket(self):
        self.__socket.close()
    def get_player_had_join(self):
        return self.__player_had_join
    def get_client1(self):
        return self.__client1

    def get_client2(self):
        return self.__client2

    def get_client3(self):
        return self.__client3
    def get_address_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return (s.getsockname()[0])

    def add_all_player(self, nbr_player):
        self.__player_had_join = 1
        self.listen(self.__player_had_join)
        self.__player_had_join += 1
        print("le client 1 est la")
        if nbr_player == 4:
            self.listen(self.__player_had_join)
            print("le client 2 est la")
            self.__player_had_join += 1
            self.listen(self.__player_had_join)
            print("le client 3 est la")
            self.__player_had_join += 1
        print("le jeu est pret")
        return "ok"

    def listen(self, player):
        self.__socket.listen(5)
        if player == 1:
            self.__client1, self.address1 = self.__socket.accept()
            self.__client1.send("1".encode())
            info_player = {"type": "player", "num_player": "1"}
            self.send_message_server_all_client(info_player, 1)
            print("j'ai envoyé 1")
        elif player == 2:
            self.__client2, self.address2 = self.__socket.accept()
            self.__client2.send("2".encode())
            info_player = {"type": "player", "num_player": "2"}
            self.send_message_server_all_client(info_player, 2)
            print("j'ai envoyé 2")
        elif player == 3:
            self.__client3, self.address3 = self.__socket.accept()
            self.__client3.send("3".encode())
            info_player = {"type": "player", "num_player": "3"}
            self.send_message_server_all_client(info_player, 3)
            print("j'ai envoyé 3")

    def send_message_server_all_client(self, message, player_acct):
        serialized_list = pickle.dumps(message)
        if player_acct != 1:
            self.__client1.send(serialized_list)
        if self.__client2 is not None and player_acct != 2:
            self.__client2.send(serialized_list)
        if self.__client3 is not None and player_acct != 3:
            self.__client3.send(serialized_list)

    def send_text_all_client(self, message):
        print("je send a tous :")
        self.__client1.send(message.encode())
        print("j'ai envoyé au 1")
        if self.__client2 is not None:
            self.__client2.send(message.encode())
            print("j'ai envoyé au 2")
            if self.__client3 is not None:
                self.__client3.send(message.encode())
                print("j'ai envoyé au 3")


