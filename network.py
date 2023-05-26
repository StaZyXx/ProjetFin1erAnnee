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
    
    
    def send_message_client(self,liste):
        serialized_list = pickle.dumps(liste)
        self.__socket.sendall(serialized_list)
        
    

class Server :
    def __init__(self,nbr_joueur):
        self.__nbr_joueur = nbr_joueur
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
        
    def give_ip(self):
        return self.__adress_ip
        
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
        
    def receipt_message_client(self,recipient):
        data = b''
        chunk = recipient.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        print(received_list)
        return received_list 
    
rep = str(input("tu veux faire quoi ?"))
if rep == "0":
    serv = Server(1)
    serv.join()
    serv.receipt_message_client(serv.player2)
elif rep == "1":
    L = {'Nepal': 'Kathmandu', 'Italy': 'Rome', 'England': 'London'}
    clt = Client()
    clt.conection()
    time.sleep(1)
    clt.send_message_client(L)

    
    

    
        
        
