import socket
import time
import pickle

class Client :
    def __init__(self):
        self.__adress = str(input("Renseignez l'ip de connexion : "))
        self.__host, self.__port = (self.__adress,4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conection(self):
        try :
            self.__socket.connect((self.__host,self.__port))
            mess = self.__socket.recv(1024)
            mess = mess.decode("utf8")
            print(mess)
        except :
            print("Connexion au serveur échouée !")
            
    def receipt_message_client(self):
        data = b''
        chunk = self.__socket.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        print(received_list)
        return received_list

class Server :
    def __init__(self):
        self.__nbr_joueur = 1
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
        
    def join(self):
        self.listen()
        if self.__nbr_joueur != 1 :
            self.listen()
            self.listen()

    def listen(self):
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
    
    def send_message_server(self,recipient,liste):
        serialized_list = pickle.dumps(liste)
        recipient.sendall(serialized_list)
        
    def send_message_server_all_client(self,liste):
        serialized_list = pickle.dumps(liste)
        self.player2.sendall(serialized_list)
        if self.__nbr_joueur != 1 :
            self.player3.sendall(serialized_list)
            self.player4.sendall(serialized_list)
        
retour = str(input("0 pour etre client et 1 pour etre serveur : "))
if retour == "1":
    mon_dict = {"nom": "Gayerie", "prenom": "David"}           
    test = Server()
    test.join()
    time.sleep(0.2)
    test.send_message_server_all_client(mon_dict)
if retour == "0":      
    pas = Client()  
    pas.conection()
    L = pas.receipt_message_client()
     
while True :
    pass