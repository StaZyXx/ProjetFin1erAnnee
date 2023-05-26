import socket
import time
import pickle


class Client:
    def __init__(self, address_ip):
        self.__address = address_ip
        self.__host, self.__port = (self.__address, 4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):  # renvoie 1 si il a réussi à se co et 0 dans l'autre cas
        try:
            self.__socket.connect((self.__host, self.__port))
            return 1
        except socket.error:
            return 0

    def receipt_message_client(self):
        data = b''
        chunk = self.__socket.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        return received_list

    def send_message_client(self, message):
        serialized_list = pickle.dumps(message)
        self.__socket.sendall(serialized_list)


class Server:
    def __init__(self, host, port_host):
        self.__host, self.__post = (host, port_host)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host, self.__post))

    def listen(self):
        self.__socket.listen(5)
        return self.__socket.accept()

    def send_message_server(self, recipient, message):
        serialized_list = pickle.dumps(message)
        recipient.sendall(serialized_list)

    def send_message_server_all_client(self, message, players):
        serialized_list = pickle.dumps(message)
        for player in players:
            player.sendall(serialized_list)

    def receipt_message_client(self, recipient):
        data = b''
        chunk = recipient.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        return received_list
