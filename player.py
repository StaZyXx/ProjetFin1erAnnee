class Player:
    def __init__(self):
        self.__amount_barrier = 0
        self.__x = 0
        self.__y = 0

    def set_location(self, x, y):
        self.__x = x
        self.__y = y

    def get_location(self) -> [int, int]:
        return self.__x, self.__y
