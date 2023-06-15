class Player:
    def __init__(self, id: int):
        self.__amount_barrier = 0
        self.__id = id
        self.__x = 0
        self.__y = 0
        self.__is_bot = False

    def get_amount_barrier(self) -> int:
        return self.__amount_barrier

    def set_amount_barrier(self, amount_barrier: int):
        self.__amount_barrier = amount_barrier

    def decrease_amount_barrier(self):
        self.__amount_barrier -= 1
    def set_bot(self):
        self.__is_bot = True
    def is_bot(self):
        return self.__is_bot
    def get_id(self) -> int:
        return self.__id

    def set_location(self, x, y):
        self.__x = x
        self.__y = y

    def get_location(self) -> [int, int]:
        return self.__x, self.__y
