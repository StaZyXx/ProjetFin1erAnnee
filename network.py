import socket
import time
import pickle

class Client :
    def __init__(self,adress_ip):
        self.__adress = adress_ip
        self.__host, self.__port = (self.__adress,4000)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self): #renvoie 1 si il a réussi à se co et 0 dans l'autre cas
        try : 
            self.__socket.connect((self.__host,self.__port))
            mess = self.__socket.recv(1024)
            mess = mess.decode("utf8")
            return 1
        except :
            return 0
            
    def receipt_message_client(self):
        data = b''
        chunk = self.__socket.recv(4096)
        data += chunk
        received_list = pickle.loads(data)
        return received_list
    
    
    def send_message_client(self,liste):
        serialized_list = pickle.dumps(liste)
        self.__socket.sendall(serialized_list)
        
    

class Server :
    def __init__(self,host,port_host):
        self.__host, self.__post = (host,port_host)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host,self.__post))

        
    def give_ip(self):
        return self.__adress_ip

    def listen(self):
        self.__socket.listen(5)
        return self.__socket.accept()
    
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

    

    
        
        
