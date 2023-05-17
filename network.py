import socket

class Server :
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__s.connect(("8.8.8.8", 80))
        self.__adress_ip = slef.__socket.getsockname()[0]
        self.__host, self.__post = ('',4000)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((host,post))

    def ecoute(self):
        while True :
            self.__socket.listen(5)

