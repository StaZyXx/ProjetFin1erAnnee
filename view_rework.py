import pygame
from pygame import *


class View:
    def __init__(self):
        pygame.init()
        self.__running = True
        pygame.display.set_caption("Quorridor")  # Nom de la fenêtre
        self.__screen = pygame.display.set_mode((1500, 850), RESIZABLE)  # Définit la taille de la fenetre

        self.__background = pygame.image.load("./assets/background.jpg").convert()  # Charge l'image
        self.__quorridor = pygame.image.load("./assets/QUORRIDOR.png").convert_alpha()

        self.__screen.blit(self.__background, (0, 0))  # la positionne
        self.__screen.blit(self.__quorridor, (400, 75))
        pygame.display.flip()

        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()


View()
