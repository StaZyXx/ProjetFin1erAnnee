import pygame
from pygame.locals import *

import time


class View:
    def __init__(self):
        # Création des couleurs
        self.__WHITE = (255, 255, 255, 50)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (171, 242, 255, 50)
        self.__DARK_BLUE = (57, 73, 116, 200)
        self.__GREEN = (0, 255, 0)

        self.home_page()

        self.__button1 = 1
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
                        self.__running = False
                        self.__mode = "solo"
                    elif self.__get_multiplayer.collidepoint(self.__cursor_pos):
                        if self.__button1 == 1:
                            print("multiplayer")
                    elif self.__get_leave.collidepoint(self.__cursor_pos):
                        if self.__button1 == 1:
                            print("leave")

        if self.__mode == "solo":
            self.boucle_param_solo()



    def boucle_param_solo(self):
        self.couleur_2players, self.couleur_4players = self.__DARK_BLUE, self.__DARK_BLUE
        self.__color_5x5,self.__color_7x7,self.__color_9x9,self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE,self.__DARK_BLUE, self.__DARK_BLUE
        self.nbr_joueur = None
        self.param_solo()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    #choix nombre de joueur
                    if self.__get_nbr_player2.collidepoint(self.__cursor_pos):
                        self.couleur_2players = self.__GREEN
                        self.couleur_4players = self.__DARK_BLUE
                        self.nbr_joueur = 2
                        print(self.nbr_joueur)
                        self.param_solo()
                    elif self.__get_nbr_player4.collidepoint(self.__cursor_pos):
                        self.couleur_4players = self.__GREEN
                        self.couleur_2players = self.__DARK_BLUE
                        self.nbr_joueur = 4
                        print(self.nbr_joueur)
                        self.param_solo()






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

        self.__rect_solo = pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 300, 650, 75))
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

    def param_solo(self):
        self.nbr_joueur = 2
        pygame.init()

        self.__size = (1500, 850)
        self.__blue_image = pygame.Surface(self.__size, pygame.SRCALPHA)

        #carré pricipale
        pygame.draw.rect(self.__blue_image, self.__BLUE, (250, 200, 1000, 500))

        #choix nombre de joueur
        pygame.draw.rect(self.__blue_image, self.couleur_2players, (450,250, 150, 100))
        pygame.draw.rect(self.__blue_image, self.couleur_4players, (900, 250, 150, 100))

        self.__nbr_player2 = self.__font.render('2 joueurs', False, (self.__WHITE))
        self.__get__nbr_player2 = self.__nbr_player2.get_rect()
        self.__get__nbr_player2.topleft = (450, 250)

        self.__nbr_player4 = self.__font.render('4 joueurs', False, (self.__WHITE))
        self.__get__nbr_player4 = self.__nbr_player4.get_rect()
        self.__get__nbr_player4.topleft = (900, 250)

        #choix taille tableau

        pygame.draw.rect(self.__blue_image, self.__color_5x5, (300, 400, 100, 50))
        pygame.draw.rect(self.__blue_image, self.__color_7x7, (500, 400, 100, 50))
        pygame.draw.rect(self.__blue_image, self.__color_9x9, (700,400, 100, 50))
        pygame.draw.rect(self.__blue_image, self.__color_11x11, (900, 400, 100, 50))

        self.__size_5x5 = self.__font.render('5x5', False, (self.__WHITE))
        self.__get_size_5x5 = self.__multiplayer.get_rect()
        self.__get_size_5x5.topleft = (450, 250)

        self.__nbr_player4 = self.__font.render('7x7', False, (self.__WHITE))
        self.__get__nbr_player4 = self.__multiplayer.get_rect()
        self.__get__nbr_player4.topleft = (900, 250)



        #ordre d'affichage
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__blue_image, (0, 0))
        self.__screen.blit(self.__nbr_player2, (450, 250))
        self.__screen.blit(self.__nbr_player4, (900, 250))



        pygame.display.flip()  # Mettre a jour l'affichage





View()