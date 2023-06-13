import pygame


class HashableRect(pygame.Rect):
    def __hash__(self):
        return hash(tuple(self))