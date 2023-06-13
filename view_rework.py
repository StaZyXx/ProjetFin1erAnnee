import pygame
from pip._internal import self_outdated_check
from pygame.locals import *

import utils
from case import CaseType, BarrierType
from game import Game


class View:
    def __init__(self):
        # Création des couleurs
        self.__WHITE = (255, 255, 255, 50)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (171, 242, 255, 50)
        self.__DARK_BLUE = (57, 73, 116, 200)
        self.__RED = (255, 0, 0)
        self.__GREEN = (0, 255, 0)

        pygame.init()
        pygame.display.set_caption("Quorridor")  # Nom de la fenêtre
        self.__screen = pygame.display.set_mode((1500, 850))  # Définit la taille de la fenetre
        self.__background = pygame.image.load("./assets/background.jpg").convert()  # Charge l'image

        # Création des tailles de polices
        self.__96_font = pygame.font.SysFont('./fonts/Carme.ttf', 96, bold=False)
        self.__64_font = pygame.font.SysFont('./fonts/Carme.ttf', 64, bold=False)
        self.__48_font = pygame.font.SysFont('./fonts/Carme.ttf', 48, bold=False)
        self.__32_font = pygame.font.SysFont('./fonts/Carme.ttf', 32, bold=False)

        self.__blue_image = pygame.Surface((1500, 850), pygame.SRCALPHA)

        self.__game = None

        self.boucle_home_page()

    def boucle_home_page(self):
        self.home_page()
        self.__running = True
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
                        print("multiplayer")
                        self.__running = False
                        self.__mode = "multiplayer"
                    elif self.__get_leave.collidepoint(self.__cursor_pos):
                        print("leave")
                        pygame.quit()

        if self.__mode == "solo":
            self.boucle_param("solo")
        if self.__mode == "multiplayer":
            self.boucle_choice_server_client()
        if self.__mode == "game":
            self.boucle_game()

    def home_page(self):
        self.__screen.blit(self.__background, (0, 0))

        pygame.draw.rect(self.__blue_image, self.__WHITE, (530, 100, 520, 100))
        self.__quorridor = self.__96_font.render('QUORRIDOR', False, (self.__BLACK))

        self.__rect_solo = pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 300, 650, 75))
        self.__solo = self.__64_font.render('Solo', False, (self.__WHITE))
        self.__get_solo = self.__solo.get_rect()
        self.__get_solo.topleft = (700, 300)

        pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 450, 650, 75))
        self.__multiplayer = self.__64_font.render('Multijoueur', False, (self.__WHITE))
        self.__get_multiplayer = self.__multiplayer.get_rect()
        self.__get_multiplayer.topleft = (700, 450)

        pygame.draw.rect(self.__blue_image, self.__BLUE, (460, 600, 650, 75))
        self.__leave = self.__64_font.render('Quitter', False, (self.__WHITE))
        self.__get_leave = self.__leave.get_rect()
        self.__get_leave.topleft = (700, 610)

        self.__screen.blit(self.__blue_image, (0, 0))
        self.__screen.blit(self.__quorridor, (590, 125))
        self.__screen.blit(self.__solo, (730, 315))
        self.__screen.blit(self.__multiplayer, (660, 460))
        self.__screen.blit(self.__leave, (700, 610))

        pygame.display.flip()  # Mettre a jour l'affichage

    def boucle_param(self, mode):
        self.__GREEN = pygame.Color(57, 116, 70, 255)
        self.couleur_2players, self.couleur_4players = self.__DARK_BLUE, self.__DARK_BLUE
        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE
        self.__nbr_joueur = None
        self.__board_size = None
        self.__nbr_barr = 20
        self.param_game(mode)
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    # choix nombre de joueur
                    if self.__get_back.collidepoint(self.__cursor_pos):
                        self.boucle_home_page()
                    if mode != "multiplayer":
                        if self.__get_nbr_player2.collidepoint(self.__cursor_pos):
                            self.couleur_2players = self.__GREEN
                            self.couleur_4players = self.__DARK_BLUE
                            self.__nbr_joueur = 2
                        elif self.__get_nbr_player4.collidepoint(self.__cursor_pos):
                            self.couleur_4players = self.__GREEN
                            self.couleur_2players = self.__DARK_BLUE
                            self.__nbr_joueur = 4
                    # choice size
                    if self.__get_size_5x5.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__GREEN, self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE
                        self.__board_size = 5
                    elif self.__get_size_7x7.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE, self.__DARK_BLUE
                        self.__board_size = 7
                    elif self.__get_size_9x9.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE
                        self.__board_size = 9
                    elif self.__get_size_11x11.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN
                        self.__board_size = 11
                    elif self.__get_less_barr.collidepoint(self.__cursor_pos):
                        if self.__nbr_barr > 4:
                            self.__nbr_barr -= 4
                    elif self.__get_more_barr.collidepoint(self.__cursor_pos):
                        if self.__nbr_barr < 40:
                            self.__nbr_barr += 4
                    elif self.__get_start_game.collidepoint(event.pos):
                        if mode == "solo":
                            self.__game = Game()
                            self.__game.start(self.__board_size, self.__nbr_joueur)
                        self.game_page()
                        self.__running = False
                        self.__mode = "game"

                    self.param_game(mode)

    def param_game(self, mode):
        self.nbr_joueur = 2
        pygame.init()

        self.__size = (1500, 850)
        self.__blue_image2 = pygame.Surface(self.__size, pygame.SRCALPHA)

        # carré pricipale
        pygame.draw.rect(self.__blue_image2, pygame.Color(64, 91, 67, 50), (250, 200, 1000, 500))

        pygame.draw.rect(self.__blue_image2, self.__DARK_BLUE, (100, 100, 100, 100))
        self.__back = self.__96_font.render('Retour', False, (self.__WHITE))
        self.__get_back = self.__back.get_rect()
        self.__get_back.topleft = (100, 100)

        # choix nombre de joueur
        if mode != "multiplayer":
            pygame.draw.rect(self.__blue_image2, self.couleur_2players, (425, 240, 209, 58))
            pygame.draw.rect(self.__blue_image2, self.couleur_4players, (875, 240, 209, 58))

            self.__nbr_player2 = self.__48_font.render('2 joueurs', False, (self.__WHITE))
            self.__get_nbr_player2 = self.__nbr_player2.get_rect()
            self.__get_nbr_player2.topleft = (450, 250)

            self.__nbr_player4 = self.__48_font.render('4 joueurs', False, (self.__WHITE))
            self.__get_nbr_player4 = self.__nbr_player4.get_rect()
            self.__get_nbr_player4.topleft = (900, 250)

        # choix taille tableau

        pygame.draw.rect(self.__blue_image2, self.__color_5x5, (365, 390, 120, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_7x7, (565, 390, 120, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_9x9, (820, 390, 120, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_11x11, (1020, 390, 150, 50))

        self.__size_5x5 = self.__48_font.render('5x5', False, (self.__WHITE))
        self.__get_size_5x5 = self.__size_5x5.get_rect()
        self.__get_size_5x5.topleft = (400, 400)

        self.__size_7x7 = self.__48_font.render('7x7', False, (self.__WHITE))
        self.__get_size_7x7 = self.__size_7x7.get_rect()
        self.__get_size_7x7.topleft = (600, 400)

        self.__size_9x9 = self.__48_font.render('9x9', False, (self.__WHITE))
        self.__get_size_9x9 = self.__size_9x9.get_rect()
        self.__get_size_9x9.topleft = (850, 400)

        self.__size_11x11 = self.__48_font.render('11x11', False, (self.__WHITE))
        self.__get_size_11x11 = self.__size_11x11.get_rect()
        self.__get_size_11x11.topleft = (1050, 400)

        # choix nombre barrière
        pygame.draw.rect(self.__blue_image2, self.__DARK_BLUE, (700, 500, 200, 50))

        self.__less_barr = self.__48_font.render('-', False, (self.__WHITE))
        self.__get_less_barr = self.__less_barr.get_rect()
        self.__get_less_barr.topleft = (700, 500)

        # nbr_barr = str(self.__nbr_barr)
        self.__show_nbr_barr = self.__48_font.render(str(self.__nbr_barr), False, (self.__WHITE))

        self.__more_barr = self.__48_font.render('+', False, (self.__WHITE))
        self.__get_more_barr = self.__more_barr.get_rect()
        self.__get_more_barr.topleft = (900, 500)

        pygame.draw.rect(self.__blue_image2, self.__DARK_BLUE, (600, 590, 350, 60))

        self.__start_game = self.__48_font.render('Lancer la partie', False, (self.__WHITE))

        self.__get_start_game = self.__start_game.get_rect()
        self.__get_start_game.topleft = (650, 600)

        # ordre d'affichage
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__blue_image2, (0, 0))

        # back
        self.__screen.blit(self.__back, (100, 100))

        # choice player
        if mode != "multiplayer":
            self.__screen.blit(self.__nbr_player2, (450, 250))
            self.__screen.blit(self.__nbr_player4, (900, 250))

        # choice size
        self.__screen.blit(self.__size_5x5, (400, 400))
        self.__screen.blit(self.__size_7x7, (600, 400))
        self.__screen.blit(self.__size_9x9, (850, 400))
        self.__screen.blit(self.__size_11x11, (1050, 400))

        # choice barr
        self.__screen.blit(self.__less_barr, (700, 500))
        self.__screen.blit(self.__show_nbr_barr, (800, 500))
        self.__screen.blit(self.__more_barr, (900, 500))
        self.__screen.blit(self.__start_game, (650, 600))
        pygame.display.flip()  # Mettre a jour l'affichage

    def boucle_choice_server_client(self):
        self.choice_server_client()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_server.collidepoint(self.__cursor_pos):
                        self.boucle_param("multiplayer")
                    elif self.__get_back.collidepoint(self.__cursor_pos):
                        self.boucle_home_page()
                    elif self.__get_client.collidepoint(self.__cursor_pos):
                        print("je suis con")
                        self.boucle_join_page()

    def choice_server_client(self):
        pygame.init()
        self.__blue_image3 = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__blue_image3, self.__BLUE, (50, 50, 1400, 750))
        pygame.draw.rect(self.__blue_image3, self.__DARK_BLUE, (200, 200, 1100, 150))
        pygame.draw.rect(self.__blue_image3, self.__DARK_BLUE, (200, 400, 1100, 150))

        self.__server = self.__96_font.render("Créer", False, (self.__WHITE))
        self.__get_server = self.__server.get_rect()
        self.__get_server.topleft = (700, 250)

        self.__client = self.__96_font.render("Rejoindre", False, (self.__WHITE))
        self.__get_client = self.__client.get_rect()
        self.__get_client.topleft = (650, 450)

        self.__back = pygame.image.load("./assets/fleche-retour.png").convert_alpha()
        self.__back = pygame.transform.scale(self.__back, (100, 100))
        self.__get_back = self.__back.get_rect()

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__blue_image3, (0, 0))
        self.__screen.blit(self.__back, (50, 50))
        self.__screen.blit(self.__server, (700, 250))
        self.__screen.blit(self.__client, (650, 450))

        pygame.display.flip()

    def boucle_join_page(self):
        self.__adress = ""
        self.join_page()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_1 or event.key == K_KP1:
                        self.__adress = self.__adress + "1"
                    elif event.key == K_2 or event.key == K_KP2:
                        self.__adress = self.__adress + "2"
                    elif event.key == K_3 or event.key == K_KP3:
                        self.__adress = self.__adress + "3"
                    elif event.key == K_4 or event.key == K_KP4:
                        self.__adress = self.__adress + "4"
                    elif event.key == K_5 or event.key == K_KP5:
                        self.__adress = self.__adress + "5"
                    elif event.key == K_6 or event.key == K_KP6:
                        self.__adress = self.__adress + "6"
                    elif event.key == K_7 or event.key == K_KP7:
                        self.__adress = self.__adress + "7"
                    elif event.key == K_8 or event.key == K_KP8:
                        self.__adress = self.__adress + "8"
                    elif event.key == K_9 or event.key == K_KP9:
                        self.__adress = self.__adress + "9"
                    elif event.key == K_0 or event.key == K_KP0:
                        self.__adress = self.__adress + "0"
                    elif event.key == K_KP_PERIOD or event.key == K_PERIOD:
                        self.__adress = self.__adress + "."
                    elif event.key == K_DELETE:
                        self.__adress = self.__adress[:1]
                        print(self.__adress)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_1.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "1"
                    elif self.__get_2.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "2"
                    elif self.__get_3.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "3"
                    elif self.__get_4.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "4"
                    elif self.__get_5.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "5"
                    elif self.__get_6.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "6"
                    elif self.__get_7.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "7"
                    elif self.__get_8.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "8"
                    elif self.__get_9.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "9"
                    elif self.__get_0.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "0"
                    elif self.__get_point.collidepoint(self.__cursor_pos):
                        self.__adress = self.__adress + "."

                self.join_page()

    def join_page(self):
        pygame.init()
        self.__blue_image4 = pygame.Surface((1500, 850), pygame.SRCALPHA)

        # carré
        pygame.draw.rect(self.__blue_image4, self.__BLUE, (50, 50, 1400, 750))

        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (100, 200, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (100, 300, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (100, 400, 50, 50))

        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (400, 200, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (400, 300, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (400, 400, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (400, 500, 50, 50))

        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (700, 200, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (700, 300, 50, 50))
        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (700, 400, 50, 50))

        # lettre
        self.__1 = self.__96_font.render("1", False, (self.__WHITE))
        self.__get_1 = self.__1.get_rect()
        self.__get_1.topleft = (100, 200)
        self.__4 = self.__96_font.render("4", False, (self.__WHITE))
        self.__get_4 = self.__4.get_rect()
        self.__get_4.topleft = (100, 300)
        self.__7 = self.__96_font.render("7", False, (self.__WHITE))
        self.__get_7 = self.__7.get_rect()
        self.__get_7.topleft = (100, 400)

        self.__2 = self.__96_font.render("2", False, (self.__WHITE))
        self.__get_2 = self.__2.get_rect()
        self.__get_2.topleft = (400, 200)
        self.__5 = self.__96_font.render("5", False, (self.__WHITE))
        self.__get_5 = self.__5.get_rect()
        self.__get_5.topleft = (400, 300)
        self.__8 = self.__96_font.render("8", False, (self.__WHITE))
        self.__get_8 = self.__8.get_rect()
        self.__get_8.topleft = (400, 400)
        self.__0 = self.__96_font.render("0", False, (self.__WHITE))
        self.__get_0 = self.__0.get_rect()
        self.__get_0.topleft = (400, 500)

        self.__3 = self.__96_font.render("3", False, (self.__WHITE))
        self.__get_3 = self.__3.get_rect()
        self.__get_3.topleft = (700, 200)
        self.__6 = self.__96_font.render("6", False, (self.__WHITE))
        self.__get_6 = self.__6.get_rect()
        self.__get_6.topleft = (700, 300)
        self.__9 = self.__96_font.render("9", False, (self.__WHITE))
        self.__get_9 = self.__9.get_rect()
        self.__get_9.topleft = (700, 400)
        self.__point = self.__96_font.render(".", False, (self.__WHITE))
        self.__get_point = self.__point.get_rect()
        self.__get_point.topleft = (700, 500)

        self.__adress_final1 = self.__96_font.render("Adresse de connexion :", False, (self.__WHITE))
        self.__adress_final2 = self.__96_font.render(self.__adress, False, (self.__WHITE))

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__blue_image4, (0, 0))

        self.__screen.blit(self.__1, (100, 200))
        self.__screen.blit(self.__4, (100, 300))
        self.__screen.blit(self.__7, (100, 400))

        self.__screen.blit(self.__2, (400, 200))
        self.__screen.blit(self.__5, (400, 300))
        self.__screen.blit(self.__8, (400, 400))
        self.__screen.blit(self.__0, (400, 500))

        self.__screen.blit(self.__3, (700, 200))
        self.__screen.blit(self.__6, (700, 300))
        self.__screen.blit(self.__9, (700, 400))
        self.__screen.blit(self.__point, (700, 500))

        self.__screen.blit(self.__adress_final1, (100, 700))
        self.__screen.blit(self.__adress_final2, (875, 700))

        pygame.display.flip()

    def game_page(self):
        pygame.init()
        cases_items = {}
        self.__blue_image4 = pygame.Surface((1500, 850), pygame.SRCALPHA)

        # use self.get_cases()
        cases = self.__game.get_cases()
        for i in range(len(cases)):
            for j in range(len(cases[i])):
                case = cases[j][i]
                rect = None

                if case.has_player():
                    rect = utils.HashableRect(
                        pygame.draw.rect(self.__blue_image4, self.__RED, (i * 50 + 1, j * 50 + 1, 38, 38)))
                elif case.get_case_type() == CaseType.DEFAULT:
                    rect = utils.HashableRect(
                        pygame.draw.rect(self.__blue_image4, self.__BLUE, (i * 50 + 1, j * 50 + 1, 38, 38)))
                elif case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                    rect = utils.HashableRect(
                        pygame.draw.line(self.__blue_image4, self.__DARK_BLUE, (i * 50, j * 50 + 20),
                                         (i * 50 + 40, j * 50 + 20), 10))
                elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                    rect = utils.HashableRect(
                        pygame.draw.rect(self.__blue_image4, self.__DARK_BLUE, (i * 50 + 20, j * 50, 10, 40)))
                elif case.get_case_type() == CaseType.BARRIER:
                    if case.get_barrier_type() == BarrierType.HORIZONTAL:
                        rect = utils.HashableRect(
                            pygame.draw.rect(self.__blue_image4, self.__RED, (i * 50, j * 50, 40, 10)))
                    elif case.get_barrier_type() == BarrierType.VERTICAL:
                        rect = utils.HashableRect(
                            pygame.draw.rect(self.__blue_image4, self.__RED, (i * 50, j * 50, 10, 40)))

                cases_items.update({rect: (j, i)})

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, (i, j) in cases_items.items():
                    if rect is not None and rect.collidepoint(event.pos):
                        case = self.__game.get_case(i, j)
                        print(i, j)

                        if case.get_case_type() == CaseType.BLANK:
                            pass

                        elif case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                            self.__game.place_barrier(i, j, BarrierType.HORIZONTAL)
                        elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                            self.__game.place_barrier(i, j, BarrierType.VERTICAL)
                        else:
                            self.__game.move_player(i, j)
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__blue_image4, (0, 0))
        pygame.display.flip()

    def boucle_game(self):
        self.__running = True
        pygame.display.update()
        while self.__running:
            self.game_page()


View()
