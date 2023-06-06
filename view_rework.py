import pygame
from pygame.locals import *


class View:
    def __init__(self):
        # Création des couleurs
        self.__WHITE = (255, 255, 255, 50)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (171, 242, 255, 50)

        self.home_page()

        # Boucle du jeu
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_solo.collidepoint(self.__cursor_pos):
                        print("solo")
                    elif self.__get_multiplayer.collidepoint(self.__cursor_pos):
                        print("multiplayer")
                    elif self.__get_leave.collidepoint(self.__cursor_pos):
                        print("leave")

    def home_page(self):
        pygame.init()
        self.__font = pygame.font.SysFont('./fonts/Carme.ttf', 80, bold=False)
        self.__running = True
        pygame.display.set_caption("Quorridor")  # Nom de la fenêtre
        self.__screen = pygame.display.set_mode((1500, 850))  # Définit la taille de la fenetre
        self.__background = pygame.image.load("./assets/background.jpg").convert()  # Charge l'image
        self.__screen.blit(self.__background, (0, 0))

        self.__size = (1500, 850)
        self.__blue_image = pygame.Surface(self.__size, pygame.SRCALPHA)
        pygame.draw.rect(self.__blue_image, self.__WHITE, (525, 100, 520, 100))
        self.__quorridor = self.__font.render('QUORRIDOR', False, (self.__BLACK))

        pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 300, 650, 75))
        self.__solo = self.__font.render('Solo', False, (self.__WHITE))
        self.__get_solo = self.__solo.get_rect()
        self.__get_solo.topleft = (700, 300)

        pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 450, 650, 75))
        self.__multiplayer = self.__font.render('Multijoueur', False, (self.__WHITE))
        self.__get_multiplayer = self.__multiplayer.get_rect()
        self.__get_multiplayer.topleft = (700, 450)

        pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 600, 650, 75))
        self.__leave = self.__font.render('Quitter', False, (self.__WHITE))
        self.__get_leave = self.__leave.get_rect()
        self.__get_leave.topleft = (1100, 500)

        self.__screen.blit(self.__blue_image, (0, 0))
        self.__screen.blit(self.__quorridor, (620, 125))
        self.__screen.blit(self.__solo, (730, 315))
        self.__screen.blit(self.__multiplayer, (660, 460))
        self.__screen.blit(self.__leave, (700, 610))

        pygame.display.flip()  # Mettre a jour l'affichage


View()