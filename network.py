import socket

import time

class Server :
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__s.connect(("8.8.8.8", 80))
        self.__adress_ip = self.__s.getsockname()[0]
        print(self.__adress_ip)
        self.__host, self.__post = ('',4000)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host,self.__post))
#utilisation de la class player (le joueur serveur n'est donc pas compté)
        self.player2, self.adress2 = None, None
        self.player3, self.adress3 = None, None
        self.player4, self.adress4 = None, None

    def ecoute(self,player,adress,num_play):
        while True :
            self.__socket.listen(5)
            player,adress = self.__socket.accept()
            player.send(f"Vous êtes le joueur {num_play} !".encode())
            print(f"Le joueur {num_play} à rejoint la partie !")
            break
class Client :
    def __init__(self):
        self.__adress = str(input("Renseignez l'ip de connexion : "))
        self.__host, self.__port = (self.__adress,4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        self.__socket.connect((self.__host,self.__port))
        mess = self.__socket.recv(1024)
        mess = mess.decode("utf8")
        print(mess)

choice = str(input("Quelle est le role server/client ? (s/c)"))
if choice == "s":
    server = Server()
    server.ecoute(server.player2, server.adress2, 2)
    server.ecoute(server.player3, server.adress3, 3)
    server.ecoute(server.player4, server.adress4, 4)
elif choice == "c":
    client = Client()
    client.connexion()
    while(True):
        pass