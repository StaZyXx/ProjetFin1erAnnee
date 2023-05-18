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
        self.player_act = 2

    def ecoute(self):
        while True :
            self.__socket.listen(5)
            if self.player_act == 2:
                self.player2,self.adress2 = self.__socket.accept()
                player = self.player2
            elif self.player_act == 3:
                self.player3,self.adress3 = self.__socket.accept()
                player = self.player3
            elif self.player_act == 4:
                self.player4,self.adress4 = self.__socket.accept()
                player = self.player4
            player.send(f"Vous êtes le joueur {self.player_act} !".encode())
            print(f"Le joueur {self.player_act} à rejoint la partie !")
            self.player_act += 1
            break

    def receipt_message_server(self):
        message = self.__socket.recv(1024)
        message = message.decode("utf8")
        return message

    def send_message_server(self,recipient,message,):
        recipient.send(message.encode())
        
class Client :
    def __init__(self):
        self.__adress = str(input("Renseignez l'ip de connexion : "))
        self.__host, self.__port = (self.__adress,4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connexion(self):
        try :
            self.__socket.connect((self.__host,self.__port))
            mess = self.__socket.recv(1024)
            mess = mess.decode("utf8")
            print(mess)
        except :
            print("Connexion au serveur échouée !")
    def receipt_message_client(self):
        message = self.__socket.recv(1024)
        message = message.decode("utf8")
        return message

    def send_message_client(self,message):
        self.__socket.send(message.encode())

choice = str(input("Quelle est le role server/client ? (s/c)"))
if choice == "s":
    server = Server()
    server.ecoute()
    server.ecoute()
    server.ecoute()
    server.send_message_server(server.player2,"Les joueurs sont tous la !")
    server.send_message_server(server.player3,"Les joueurs sont tous la !")
    server.send_message_server(server.player4,"Les joueurs sont tous la !")
elif choice == "c":
    client = Client()
    client.connexion()
    print(client.receipt_message_client())
    while(True):
        pass