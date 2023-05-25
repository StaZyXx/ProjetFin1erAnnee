from game import Game


class Multiplayer(Game):

    def __init__(self, network):
        super().__init__()
        self.__network = network

    #TODO IMPLEMENTER LE RéSEAU ICI