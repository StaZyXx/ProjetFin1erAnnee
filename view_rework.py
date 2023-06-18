import threading
import time

import pygame
from pygame import mixer
from pygame.locals import *

import network
import utils
from case import CaseType, BarrierType
from game import Game
from multiplayer import Multiplayer
from network import Client


class View:
    def __init__(self):
        # Création des couleurs
        self.__WHITE = (255, 255, 255, 50)
        self.__BLACK = (0, 0, 0)
        self.__YELLOW = (246, 255, 51)
        self.__BLUE = (171, 242, 255, 50)
        self.__BLUE_PLAYER = (51, 110, 255)
        self.__DARK_BLUE = (57, 73, 116, 200)
        self.__RED = (255, 0, 0)
        self.__GREEN = (0, 255, 0)
        self.__BLUE_BORDER = (0, 47, 213)

        self.__is_mute = False

        pygame.init()
        pygame.display.set_caption("Quorridor")  # Nom de la fenêtre
        self.__screen = pygame.display.set_mode((1500, 850))  # Définit la taille de la fenetre
        self.__background = pygame.image.load("./assets/background.jpg").convert()  # Charge l'image

        pygame.mixer.set_num_channels(6)

        # Création des tailles de polices
        self.__96_font = pygame.font.SysFont('./fonts/Carme.ttf', 96, bold=False)
        self.__64_font = pygame.font.SysFont('./fonts/Carme.ttf', 64, bold=False)
        self.__48_font = pygame.font.SysFont('./fonts/Carme.ttf', 48, bold=False)
        self.__32_font = pygame.font.SysFont('./fonts/Carme.ttf', 32, bold=False)

        # load images players
        self.__img_red_player = pygame.image.load("./assets/red_player.png").convert_alpha()
        self.__img_blue_player = pygame.image.load("./assets/blue_player.png").convert_alpha()
        self.__img_yellow_player = pygame.image.load("./assets/yellow_player.png").convert_alpha()
        self.__img_green_player = pygame.image.load("./assets/green_player.png").convert_alpha()

        self.__img_game_board = pygame.image.load("./assets/plateau_de_jeu.png").convert_alpha()
        self.__logo = pygame.image.load("./assets/Brain_Games.png").convert_alpha()

        self.__red_barrier = pygame.image.load("./assets/Red_fence.png").convert_alpha()
        self.__blue_barrier = pygame.image.load("./assets/Blue_Fence.png").convert_alpha()
        self.__yellow_barrier = pygame.image.load("./assets/Yellow_Fence.png").convert_alpha()
        self.__green_barrier = pygame.image.load("./assets/Green_Fence.png").convert_alpha()

        self.__game = None

        mixer.init()

        self.before_loading_page()

    def before_loading_page(self):
        self.__player_leave = False
        self.__show_popup = False
        self.loading_page()
        time.sleep(0.5)
        self.loop_home_page()

    def loading_page(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__blue_image0 = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__blue_image0, self.__WHITE, (530, 310, 520, 90))
        self.__quorridor = self.__96_font.render('QUORRIDOR', False, self.__BLACK)

        self.__screen.blit(self.__blue_image0, (0, 0))
        self.__screen.blit(self.__logo, (450, 10))
        self.__screen.blit(self.__quorridor, (590, 325))
        self.__screen.blit(self.__img_game_board, (575, 420))

        pygame.display.flip()  # Mettre a jour l'affichage

    def loop_home_page(self):
        self.home_page()
        self.__running = True
        # Boucle du jeu
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_solo.collidepoint(self.__cursor_pos):

                        self.__running = False
                        self.__mode = "solo"
                    elif self.__get_multiplayer.collidepoint(self.__cursor_pos):
                        self.__running = False
                        self.__mode = "multiplayer"
                    elif self.__get_leave.collidepoint(self.__cursor_pos):
                        pygame.quit()

        if self.__mode == "solo":
            self.loop_game_type()
        if self.__mode == "multiplayer":
            self.loop_choice_server_client()
        if self.__mode == "game":
            self.loop_game()

    def home_page(self):
        self.__screen.blit(self.__background, (0, 0))

        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)
        pygame.draw.rect(self.__surface, self.__WHITE, (530, 100, 520, 100))
        self.__quorridor = self.__96_font.render('QUORIDOR', False, self.__BLACK)

        self.__rect_solo = pygame.draw.rect(self.__surface, self.__BLUE, (460, 300, 650, 75))
        self.__solo = self.__64_font.render('Solo', False, self.__WHITE)
        self.__get_solo = self.__solo.get_rect()
        self.__get_solo.topleft = (700, 300)

        pygame.draw.rect(self.__surface, self.__BLUE, (460, 450, 650, 75))
        self.__multiplayer = self.__64_font.render('Multijoueur', False, self.__WHITE)
        self.__get_multiplayer = self.__multiplayer.get_rect()
        self.__get_multiplayer.topleft = (700, 450)

        pygame.draw.rect(self.__surface, self.__BLUE, (460, 600, 650, 75))
        self.__leave = self.__64_font.render('Quitter', False, self.__WHITE)
        self.__get_leave = self.__leave.get_rect()
        self.__get_leave.topleft = (700, 610)
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__quorridor, (590, 125))
        self.__screen.blit(self.__solo, (730, 315))
        self.__screen.blit(self.__multiplayer, (660, 460))
        self.__screen.blit(self.__leave, (700, 610))

        if self.__player_leave:
            self.__player_leave = False
            self.__player_has_leave = self.__64_font.render("Un joueur a quitté la partie", False, self.__RED)
            self.__screen.blit(self.__player_has_leave, (480, 700))

        pygame.display.flip()  # Mettre a jour l'affichage

    def loop_parameters(self, mode, is_each_turn):
        self.__GREEN = pygame.Color(57, 116, 70, 255)
        self.__player2_color, self.__player4_color = self.__DARK_BLUE, self.__DARK_BLUE
        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE
        self.__amount_players = 0
        self.__board_size = 9
        self.__amount_barrier = 20
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
                        if mode == "multiplayer":
                            self.__game.get_server().close_socket()
                        self.__running = False
                        self.loop_home_page()
                    if mode != "multiplayer":
                        if self.__get_select_2_players_rect.collidepoint(self.__cursor_pos):
                            self.__player2_color = self.__GREEN
                            self.__player4_color = self.__DARK_BLUE
                            self.__amount_players = 2
                        elif self.__get_select_4_players_rect.collidepoint(self.__cursor_pos):
                            self.__player4_color = self.__GREEN
                            self.__player2_color = self.__DARK_BLUE
                            self.__amount_players = 4
                    # choice size
                    if self.__get_size_5x5.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__GREEN, self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE
                        self.__board_size = 5
                        self.__amount_barrier = 4
                    elif self.__get_size_7x7.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE, self.__DARK_BLUE
                        self.__board_size = 7
                        self.__amount_barrier = 12
                    elif self.__get_size_9x9.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE
                        self.__board_size = 9
                        self.__amount_barrier = 20
                    elif self.__get_size_11x11.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN
                        self.__board_size = 11
                        self.__amount_barrier = 32
                    elif self.__get_less_barr.collidepoint(self.__cursor_pos):
                        if self.__amount_barrier > 4:
                            self.__amount_barrier -= 4
                    elif self.__get_more_barr.collidepoint(self.__cursor_pos):
                        if self.__board_size == 5:
                            max_barr = 8
                        elif self.__board_size == 7:
                            max_barr = 16
                        elif self.__board_size == 9:
                            max_barr = 32
                        elif self.__board_size == 11:
                            max_barr = 40
                        if self.__amount_barrier < max_barr:
                            self.__amount_barrier += 4
                    elif self.__get_start_game.collidepoint(event.pos):
                        if mode == "multiplayer":
                            self.__amount_players = self.__required_players
                        if self.__amount_players != 0 and self.__board_size != None:
                            if mode == "solo":
                                self.__game = Game()
                                self.__game.start(self.__board_size, self.__amount_players,
                                                  self.__amount_barrier, is_each_turn)
                                self.game_page()
                                self.__running = False
                                self.__mode = "game"
                            elif mode == "multiplayer":
                                if self.__game.get_server().see_if_all_player_join(self.__amount_players):
                                    self.__game.start(self.__board_size, self.__required_players, self.__amount_barrier,
                                                      True)

                                    self.__game.get_server().send_message_server_all_client({"type": "parameter",
                                                                                             "size": self.__board_size,
                                                                                             "amount_player": self.__required_players,
                                                                                             "amount_barrier": self.__amount_barrier},
                                                                                            None)
                                    self.game_page()
                                    self.__running = False
                                    self.__mode = "game"

                    self.param_game(mode)

    def param_game(self, mode):
        pygame.init()

        self.__size = (1500, 850)
        self.__surface = pygame.Surface(self.__size, pygame.SRCALPHA)

        # carré pricipale
        pygame.draw.rect(self.__surface, pygame.Color(64, 91, 67, 50), (250, 200, 1000, 500))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (75, 75, 50, 50))

        # choix nombre de joueur
        if mode != "multiplayer":
            pygame.draw.rect(self.__surface, self.__player2_color, (425, 240, 209, 58))
            pygame.draw.rect(self.__surface, self.__player4_color, (875, 240, 209, 58))

            self.__select_2_players = self.__48_font.render('2 joueurs', False, (self.__WHITE))
            self.__get_select_2_players_rect = self.__select_2_players.get_rect()
            self.__get_select_2_players_rect.topleft = (450, 250)

            self.__select_4_players = self.__48_font.render('4 joueurs', False, (self.__WHITE))
            self.__get_select_4_players_rect = self.__select_4_players.get_rect()
            self.__get_select_4_players_rect.topleft = (900, 250)

        if mode == "multiplayer":
            address = self.__game.get_server().get_address_ip()
            self.__show_address = self.__48_font.render(f"Adresse de connexion : {address}", False, (self.__WHITE))

            self.__amount_players_connected = 1
            if self.__game.get_server().get_client1() is not None:
                self.__amount_players_connected = 2
            if self.__game.get_server().get_client2() is not None:
                self.__amount_players_connected = 3
            if self.__game.get_server().get_client3() is not None:
                self.__amount_players_connected = 4
            self.__show_nbr_player = self.__48_font.render(
                f"{self.__amount_players_connected} joueur(s) sont présents sur {self.__required_players}", False,
                (self.__WHITE))

        # choix taille tableau

        pygame.draw.rect(self.__surface, self.__color_5x5, (365, 390, 120, 50))
        pygame.draw.rect(self.__surface, self.__color_7x7, (565, 390, 120, 50))
        pygame.draw.rect(self.__surface, self.__color_9x9, (820, 390, 120, 50))
        pygame.draw.rect(self.__surface, self.__color_11x11, (1020, 390, 150, 50))

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
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (690, 500, 160, 50))

        self.__less_barr = self.__48_font.render('-', False, (self.__WHITE))
        self.__get_less_barr = self.__less_barr.get_rect()
        self.__get_less_barr.topleft = (700, 500)

        # nbr_barr = str(self.__nbr_barr)
        self.__show_nbr_barr = self.__48_font.render(str(self.__amount_barrier), False, (self.__WHITE))

        self.__more_barr = self.__48_font.render('+', False, (self.__WHITE))
        self.__get_more_barr = self.__more_barr.get_rect()
        self.__get_more_barr.topleft = (820, 500)

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (600, 590, 350, 60))

        self.__start_game = self.__48_font.render('Lancer la partie', False, (self.__WHITE))

        self.__get_start_game = self.__start_game.get_rect()
        self.__get_start_game.topleft = (650, 600)

        # ordre d'affichage
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))

        # back
        self.__back = pygame.image.load("./assets/fleche-retour.png").convert_alpha()
        self.__back = pygame.transform.scale(self.__back, (100, 100))
        self.__get_back = self.__back.get_rect()

        self.__screen.blit(self.__back, (50, 50))

        # choice player
        if mode != "multiplayer":
            self.__screen.blit(self.__select_2_players, (450, 250))
            self.__screen.blit(self.__select_4_players, (900, 250))

        if mode == "multiplayer":
            self.__screen.blit(self.__show_address, (450, 250))
            self.__screen.blit(self.__show_nbr_player, (450, 300))

        # choice size
        self.__screen.blit(self.__size_5x5, (400, 400))
        self.__screen.blit(self.__size_7x7, (600, 400))
        self.__screen.blit(self.__size_9x9, (850, 400))
        self.__screen.blit(self.__size_11x11, (1050, 400))

        # choice barr
        self.__screen.blit(self.__less_barr, (700, 505))
        self.__screen.blit(self.__show_nbr_barr, (750, 505))
        self.__screen.blit(self.__more_barr, (820, 505))
        self.__screen.blit(self.__start_game, (650, 600))
        pygame.display.flip()  # Mettre a jour l'affichage

    def loop_choice_server_client(self):
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
                        self.__running = False
                        self.loop_choice_nbr_player()
                    elif self.__get_back.collidepoint(self.__cursor_pos):
                        self.__running = False
                        self.loop_home_page()
                    elif self.__get_client.collidepoint(self.__cursor_pos):
                        self.__running = False
                        self.loop_join_page()

    def choice_server_client(self):
        pygame.init()
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (75, 75, 50, 50))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 200, 1100, 150))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 400, 1100, 150))

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
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__back, (50, 50))
        self.__screen.blit(self.__server, (700, 250))
        self.__screen.blit(self.__client, (650, 450))

        pygame.display.flip()

    def loop_choice_nbr_player(self):
        self.choice_nbr_player()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_2_players.collidepoint(self.__cursor_pos):
                        self.__required_players = 2
                        self.__amount_players = 2
                        self.__game = Multiplayer(True, 2)
                        self.__first_game_or_not = 1
                        self.__thread_add_player = threading.Thread(
                            target=self.starting_thread_listening_for_clients)  # création du thread
                        self.__thread_add_player.start()  # lancement du thread
                        self.loop_parameters("multiplayer", False)
                    elif self.__get_back.collidepoint(self.__cursor_pos):
                        self.loop_home_page()
                    elif self.__get_4_players.collidepoint(self.__cursor_pos):
                        self.__required_players = 4
                        self.__amount_players = 4
                        self.__game = Multiplayer(True, 4)
                        self.__first_game_or_not = 1
                        self.__thread_add_player = threading.Thread(
                            target=self.starting_thread_listening_for_clients)  # création du thread
                        self.__thread_add_player.start()  # lancement du thread
                        self.loop_parameters("multiplayer", False)

    def starting_thread_listening_for_clients(self):
        self.__stop_listen = True
        self.__current_player_for_listen = 1
        if self.__first_game_or_not == 1:
            self.__game.wait_for_all_players()
            self.__first_game_or_not += 1
        self.__listen_player_1 = threading.Thread(
            target=self.listen_new_player)
        self.__listen_player_1.start()
        self.__current_player_for_listen += 1
        if self.__required_players == 4:
            self.__listen_player_2 = threading.Thread(
                target=self.listen_new_player)
            self.__listen_player_2.start()
            self.__current_player_for_listen += 1
            self.__listen_player_3 = threading.Thread(
                target=self.listen_new_player)
            self.__listen_player_3.start()

    def loop_game_type(self):
        self.choice_game_type()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_versus_ia.collidepoint(self.__cursor_pos):
                        self.__is_each_turn = False
                        self.loop_parameters("solo", False)
                    elif self.__get_back.collidepoint(self.__cursor_pos):
                        self.loop_home_page()
                    elif self.__get_each_turn.collidepoint(self.__cursor_pos):
                        self.__is_each_turn = True
                        self.loop_parameters("solo", True)

    def choice_game_type(self):

        pygame.init()
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 200, 1100, 150))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 400, 1100, 150))

        self.__versus_ia = self.__96_font.render("Contre une IA", False, (self.__WHITE))
        self.__get_versus_ia = self.__versus_ia.get_rect()
        self.__get_versus_ia.topleft = (525, 250)

        self.__each_turn = self.__96_font.render("Chacun son tour", False, (self.__WHITE))
        self.__get_each_turn = self.__each_turn.get_rect()
        self.__get_each_turn.topleft = (475, 450)

        self.__back = pygame.image.load("./assets/fleche-retour.png").convert_alpha()
        self.__back = pygame.transform.scale(self.__back, (100, 100))
        self.__get_back = self.__back.get_rect()

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__back, (50, 50))
        self.__screen.blit(self.__versus_ia, (525, 250))
        self.__screen.blit(self.__each_turn, (475, 450))

        pygame.display.flip()

    def choice_nbr_player(self):
        pygame.init()
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 200, 1100, 150))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (200, 400, 1100, 150))

        self.__versus_ia = self.__96_font.render("2 joueurs", False, (self.__WHITE))
        self.__get_2_players = self.__versus_ia.get_rect()
        self.__get_2_players.topleft = (700, 250)

        self.__each_turn = self.__96_font.render("4 joueurs", False, (self.__WHITE))
        self.__get_4_players = self.__each_turn.get_rect()
        self.__get_4_players.topleft = (650, 450)

        self.__back = pygame.image.load("./assets/fleche-retour.png").convert_alpha()
        self.__back = pygame.transform.scale(self.__back, (100, 100))
        self.__get_back = self.__back.get_rect()

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__back, (50, 50))
        self.__screen.blit(self.__versus_ia, (650, 250))
        self.__screen.blit(self.__each_turn, (650, 450))

        pygame.display.flip()

    def loop_join_page(self):
        self.__address = ""
        self.__has_connection_error = False
        self.join_page()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()
                if self.__get_back.collidepoint(self.__cursor_pos):
                    self.loop_home_page()
                elif event.type == KEYDOWN:
                    if len(self.__address) < 15:
                        if event.key == K_1 or event.key == K_KP1:
                            self.__address = self.__address + "1"
                        elif event.key == K_2 or event.key == K_KP2:
                            self.__address = self.__address + "2"
                        elif event.key == K_3 or event.key == K_KP3:
                            self.__address = self.__address + "3"
                        elif event.key == K_4 or event.key == K_KP4:
                            self.__address = self.__address + "4"
                        elif event.key == K_5 or event.key == K_KP5:
                            self.__address = self.__address + "5"
                        elif event.key == K_6 or event.key == K_KP6:
                            self.__address = self.__address + "6"
                        elif event.key == K_7 or event.key == K_KP7:
                            self.__address = self.__address + "7"
                        elif event.key == K_8 or event.key == K_KP8:
                            self.__address = self.__address + "8"
                        elif event.key == K_9 or event.key == K_KP9:
                            self.__address = self.__address + "9"
                        elif event.key == K_0 or event.key == K_KP0:
                            self.__address = self.__address + "0"
                        elif event.key == K_KP_PERIOD or event.key == K_PERIOD:
                            self.__address = self.__address + "."

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if len(self.__address) < 15:
                        for i, j in self.__numbers.items():
                            if i.collidepoint(self.__cursor_pos):
                                self.__address = self.__address + str(j)
                        if self.__get_zero.collidepoint(self.__cursor_pos):
                            self.__address = self.__address + "0"
                        elif self.__get_point.collidepoint(self.__cursor_pos):
                            self.__address = self.__address + "."
                    if self.__get_supprimer.collidepoint(self.__cursor_pos):
                        self.__address = ""
                    elif self.__get_join.collidepoint(self.__cursor_pos):
                        client = Client(self.__address)
                        response = client.connect()
                        if response == 0:
                            self.__has_connection_error = True
                        else:
                            self.__game = Multiplayer(False, 2, client)
                            self.loop_lobby(response)
                self.join_page()

    def loop_lobby(self, num_client):
        self.__point = "."
        self.__running = True
        self.player_acctu = num_client + 1
        self.lobby()
        self.__stop_listen = True
        self.__thread_listen_player = threading.Thread(target=self.listen_new_player)  # création du thread
        self.__thread_listen_player.start()

        self.__thread_loading = threading.Thread(target=self.point_loading_change)  # création du thread
        self.__thread_loading.start()

        while self.__running:
            for event in pygame.event.get():  # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    self.__running = False
                    pygame.quit()

    def point_loading_change(self):
        self.if_play = True
        while self.if_play:
            time.sleep(1)
            if self.__point == ".":
                self.__point = ".."
            elif self.__point == "..":
                self.__point = "..."
            elif self.__point == "...":
                self.__point = "."
            self.lobby()

    def listen_new_player(self):
        num_client = 0

        if self.__game.is_server():
            num_client = self.__current_player_for_listen
            client_list = {
                1: self.__game.get_server().get_client1(),
                2: self.__game.get_server().get_client2(),
                3: self.__game.get_server().get_client3()
            }
        while self.__stop_listen:
            if num_client == 0:
                dico = self.__game.get_client().receipt_message_client()
            else:
                dico = network.receipt_message_client(client_list[num_client])
            if dico["type"] == "player":
                self.player_acctu += 1
                self.lobby()
            elif dico["type"] == "parameter":
                self.__board_size = dico["size"]
                self.__game.start(dico["size"], dico["amount_player"], dico["amount_barrier"], True)
                self.if_play = False
                self.__running = False
                self.__mode = "game"
                self.game_page()
            elif dico["type"] == "pause":
                if dico["state"] == "put":
                    self.__show_popup = True
                else:
                    self.__show_popup = False
            elif dico["type"] == "logout":
                if self.__game.is_server():
                    dico = {"type": "logout"}
                    self.__game.get_server().send_message_server_all_client(dico, num_client)

                self.__mode = "multiplayer"
                self.__player_leave = True
                self.__stop_listen = False
                self.__game.change_is_started_for_false()
                self.__game.stop_game()
                if self.__game.is_server():
                    self.__game.get_server().close_socket()
                else:
                    self.__game.get_client().close_socket()

            else:
                self.__game.action_player(dico)

    def lobby(self):
        pygame.init()
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        self.__loading_word = self.__64_font.render(f"En attente des joueurs {self.__point}", False, (self.__WHITE))
        self.__affichage_nbr_player = self.__64_font.render(f"{self.player_acctu} joueur(s) sont présents", False,
                                                            (self.__WHITE))

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__loading_word, (500, 450))
        self.__screen.blit(self.__affichage_nbr_player, (500, 500))
        pygame.display.flip()

    def join_page(self):
        pygame.init()
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (115, 100, 650, 35))
        self.__consigne = self.__48_font.render(f"Entrez l'adresse pour vous connectez !", False, (self.__WHITE))

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (100, 200, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (100, 300, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (100, 400, 65, 65))

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (400, 200, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (400, 300, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (400, 400, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (400, 500, 65, 65))

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 200, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 300, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 400, 65, 65))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 500, 65, 65))

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (1000, 500, 350, 75))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (1000, 600, 350, 75))

        self.__zero = self.__96_font.render("0", False, (self.__WHITE))
        self.__get_zero = self.__zero.get_rect()
        self.__get_zero.topleft = (415, 500)

        self.__point = self.__96_font.render(".", False, (self.__WHITE))
        self.__get_point = self.__point.get_rect()
        self.__get_point.topleft = (715, 500)

        self.__adress_final = self.__48_font.render(f"Adresse de connexion : {self.__address}", False, (self.__WHITE))

        if self.__has_connection_error:
            self.__erreur = self.__48_font.render("Connexion au serveur échoué !", False, (self.__RED))

        self.__supprimer = self.__96_font.render("Supprimer", False, (self.__RED))
        self.__get_supprimer = self.__supprimer.get_rect()
        self.__get_supprimer.topleft = (1000, 500)

        self.__join = self.__96_font.render("Rejoindre", False, (self.__GREEN))
        self.__get_join = self.__join.get_rect()
        self.__get_join.topleft = (1000, 600)

        self.__back = pygame.image.load("./assets/fleche-retour.png").convert_alpha()
        self.__back = pygame.transform.scale(self.__back, (100, 100))
        self.__get_back = self.__back.get_rect()

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))

        self.__numbers = {}
        nbr = 0
        y = 200
        for i in range(3):
            x = 115
            for j in range(3):
                nbr += 1
                self.__number = self.__96_font.render(str(nbr), False, (self.__WHITE))
                self.__get_number = self.__number.get_rect()
                self.__get_number.topleft = (x, y)
                self.__numbers.update({utils.HashableRect(self.__get_number): nbr})
                self.__screen.blit(self.__number, (x, y))
                x += 300
            y += 100

        self.__screen.blit(self.__back, (50, 50))

        self.__screen.blit(self.__consigne, (115, 100))

        self.__screen.blit(self.__zero, (415, 500))

        self.__screen.blit(self.__point, (715, 500))

        self.__screen.blit(self.__supprimer, (1000, 500))
        self.__screen.blit(self.__join, (1000, 600))

        self.__screen.blit(self.__adress_final, (100, 700))
        if self.__has_connection_error:
            self.__screen.blit(self.__erreur, (100, 750))

        pygame.display.flip()

    def game_page(self):
        if not self.__game.is_started():
            return

        pygame.init()
        self.__is_update = True
        self.__cases_items = {}
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)
        self.__game_current_player = self.__game.get_current_player().get_id()

        colors = {
            1: self.__RED,
            2: self.__BLUE_BORDER,
            3: self.__YELLOW,
            4: self.__GREEN
        }
        separator = 25
        borderSize = {
            5: 297,
            7: 409,
            9: 521,
            11: 633
        }

        border_seperator = separator - 2
        pygame.draw.line(self.__surface, self.__BLUE_BORDER, (border_seperator, border_seperator),
                         (border_seperator, borderSize[self.__board_size]), 2)
        pygame.draw.line(self.__surface, self.__BLUE_BORDER, (border_seperator, border_seperator),
                         (borderSize[self.__board_size], border_seperator), 2)
        pygame.draw.line(self.__surface, self.__BLUE_BORDER,
                         (borderSize[self.__board_size], borderSize[self.__board_size]),
                         (borderSize[self.__board_size], border_seperator), 2)
        pygame.draw.line(self.__surface, self.__BLUE_BORDER,
                         (borderSize[self.__board_size], borderSize[self.__board_size]),
                         (border_seperator, borderSize[self.__board_size]), 2)
        cases = self.__game.get_cases()
        if self.__is_update:
            self.__is_update = False
            for i in range(len(cases)):
                for j in range(len(cases[i])):
                    case = cases[j][i]
                    rect = None
                    if case.has_player():
                        if case.get_player().get_id() == 1:
                            img_red_player = pygame.transform.scale(self.__img_red_player, (48, 48))
                            self.__surface.blit(img_red_player, (separator + i * 28, separator + j * 28))
                        elif case.get_player().get_id() == 2:
                            img_blue_player = pygame.transform.scale(self.__img_blue_player, (48, 48))
                            self.__surface.blit(img_blue_player, (separator + i * 28, separator + j * 28))
                        elif case.get_player().get_id() == 3:
                            img_yellow_player = pygame.transform.scale(self.__img_yellow_player, (48, 48))
                            self.__surface.blit(img_yellow_player, (separator + i * 28, separator + j * 28))
                        elif case.get_player().get_id() == 4:
                            img_green_player = pygame.transform.scale(self.__img_green_player, (48, 48))
                            self.__surface.blit(img_green_player, (separator + i * 28, separator + j * 28))
                    elif case.get_case_type() == CaseType.DEFAULT:
                        if self.__game.is_case_allowed(case):
                            rect = utils.HashableRect(
                                pygame.draw.rect(self.__surface, self.__WHITE,
                                                 (separator + i * 28, separator + j * 28, 48, 48)))
                        else:
                            rect = utils.HashableRect(
                                pygame.draw.rect(self.__surface, self.__BLUE,
                                                 (separator + i * 28, separator + j * 28, 48, 48)))

                    elif case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                        rect = utils.HashableRect(
                            pygame.draw.rect(self.__surface, self.__BLACK,
                                             (separator + i * 28, separator + j * 28 + 20, 48, 10)))

                    elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                        rect = utils.HashableRect(
                            pygame.draw.rect(self.__surface, self.__BLACK,
                                             (separator + i * 28 + 20, separator + j * 28, 10, 48)))

                    elif case.get_case_type() == CaseType.BARRIER:
                        if case.get_barrier_type() == BarrierType.HORIZONTAL:
                            rect = utils.HashableRect(
                                pygame.draw.rect(self.__surface, colors[case.get_who_place_barrier()],
                                                 (separator + i * 28, separator + j * 28 + 20, 48, 10)))

                        elif case.get_barrier_type() == BarrierType.VERTICAL:
                            rect = utils.HashableRect(
                                pygame.draw.rect(self.__surface, colors[case.get_who_place_barrier()],
                                                 (separator + i * 28 + 20, separator + j * 28, 10, 48)))

                    self.__cases_items.update({rect: (j, i)})

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 75, 600, 75))
        self.__turn_player = self.__48_font.render(
            "Au tour du joueur " + str(self.__game_current_player), False, (colors[self.__game_current_player]))

        for rect, (j, i) in self.__cases_items.items():
            if rect is not None and rect.collidepoint(pygame.mouse.get_pos()):
                case = self.__game.get_case(i, j)
                if case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                    if self.__game.has_case(i, j + 2) and self.__game.get_case(i,
                                                                               j + 2).get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                        utils.HashableRect(
                            pygame.draw.rect(self.__surface, colors[self.__game_current_player],
                                             (separator + i * 28 + 20, separator + j * 28, 10, 48)))
                        utils.HashableRect(
                            pygame.draw.rect(self.__surface, colors[self.__game_current_player],
                                             (separator + i * 28 + 20, separator + (j + 2) * 28, 10, 48)))

                elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                    if self.__game.has_case(i + 2, j) and self.__game.get_case(i + 2,
                                                                               j).get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                        utils.HashableRect(
                            pygame.draw.rect(self.__surface, colors[self.__game_current_player],
                                             (separator + i * 28, separator + j * 28 + 20, 48, 10)))
                        utils.HashableRect(
                            pygame.draw.rect(self.__surface, colors[self.__game_current_player],
                                             (separator + (i + 2) * 28, separator + j * 28 + 20, 48, 10)))

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (700, 200, 600, 75))
        if len(self.__game.get_players()) == 2:
            pygame.draw.rect(self.__surface, self.__BLUE, (700, 300, 500, 75))
        else:
            pygame.draw.rect(self.__surface, self.__BLUE, (700, 300, 500, 250))

        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__turn_player, (730, 100))

        self.__red_barrier = pygame.transform.scale(self.__red_barrier, (75, 64))
        self.__blue_barrier = pygame.transform.scale(self.__blue_barrier, (75, 64))
        self.__yellow_barrier = pygame.transform.scale(self.__yellow_barrier, (75, 64))
        self.__green_barrier = pygame.transform.scale(self.__green_barrier, (75, 64))

        self.__burger_image = pygame.image.load("./assets/boutton_menu.png").convert()
        self.__burger_image = pygame.transform.scale(self.__burger_image, (75, 75))
        self.__screen.blit(self.__burger_image, (1400, 25))
        self.__burger_pos = self.__burger_image.get_rect()
        self.__burger_pos.topleft = (1400, 25)

        if self.__is_mute:
            self.__image1 = pygame.image.load("./assets/image1.png").convert_alpha()
            self.__image1 = pygame.transform.scale(self.__image1, (75, 64))
            self.__song_image_pos = self.__image1.get_rect()
            self.__song_image_pos.topleft = (1400, 750)
            if self.__song_image_pos.collidepoint(pygame.mouse.get_pos()):

                self.__image1 = pygame.image.load("./assets/image.png").convert_alpha()
                self.__image1 = pygame.transform.scale(self.__image1, (75, 64))
                self.__screen.blit(self.__image1, (1400, 750))
            else:
                self.__screen.blit(self.__image1, (1400, 750))
        else:
            self.__image1 = pygame.image.load("./assets/image3.png").convert_alpha()
            self.__image1 = pygame.transform.scale(self.__image1, (75, 64))
            self.__song_image_pos = self.__image1.get_rect()
            self.__song_image_pos.topleft = (1400, 750)
            if self.__song_image_pos.collidepoint(pygame.mouse.get_pos()):

                self.__image1 = pygame.image.load("./assets/image2.png").convert_alpha()
                self.__image1 = pygame.transform.scale(self.__image1, (75, 64))
                self.__screen.blit(self.__image1, (1400, 750))
            else:
                self.__screen.blit(self.__image1, (1400, 750))

        if not self.__game.is_started():
            return
        if type(self.__game) == Multiplayer:
            multiplayer: Multiplayer = self.__game
            if multiplayer.is_server():
                self.__player1 = self.__48_font.render(
                    f"Vous êtes le joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False,
                    self.__RED)
                self.__player2 = self.__48_font.render(
                    f"Joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                    self.__BLUE_PLAYER)
                self.__screen.blit(self.__player1, (710, 220))
                self.__screen.blit(self.__player2, (710, 320))
                self.__screen.blit(self.__red_barrier, (1200, 205))
                self.__screen.blit(self.__blue_barrier, (1100, 305))
                if len(self.__game.get_players()) == 4:
                    self.__player3 = self.__48_font.render(
                        f"Joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False, self.__YELLOW)
                    self.__player4 = self.__48_font.render(
                        f"Joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False, self.__GREEN)
                    self.__screen.blit(self.__player3, (710, 400))
                    self.__screen.blit(self.__player4, (710, 480))
                    self.__screen.blit(self.__yellow_barrier, (1100, 385))
                    self.__screen.blit(self.__green_barrier, (1100, 465))

            elif multiplayer.get_client().get_me_player() == 1:
                self.__player2 = self.__48_font.render(
                    f"Vous êtes le joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                    (self.__BLUE_PLAYER))
                self.__player1 = self.__48_font.render(
                    f"Joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False, (self.__RED))
                self.__screen.blit(self.__player2, (710, 220))
                self.__screen.blit(self.__player1, (710, 320))
                self.__screen.blit(self.__blue_barrier, (1200, 205))
                self.__screen.blit(self.__red_barrier, (1100, 305))
                if len(self.__game.get_players()) == 4:
                    self.__player4 = self.__48_font.render(
                        f"Joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False,
                        (self.__GREEN))
                    self.__player3 = self.__48_font.render(
                        f"Joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False,
                        (self.__YELLOW))
                    self.__screen.blit(self.__player3, (710, 400))
                    self.__screen.blit(self.__player4, (710, 480))
                    self.__screen.blit(self.__yellow_barrier, (1100, 405))
                    self.__screen.blit(self.__red_barrier, (1100, 485))

            if len(self.__game.get_players()) == 4:
                if not multiplayer.is_server() and multiplayer.get_client().get_me_player() == 2:
                    self.__player3 = self.__48_font.render(
                        f"Vous êtes le joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False,
                        (self.__YELLOW))
                    self.__player4 = self.__48_font.render(
                        f"Joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False,
                        (self.__GREEN))
                    self.__player2 = self.__48_font.render(
                        f"Joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                        (self.__BLUE_PLAYER))
                    self.__player1 = self.__48_font.render(
                        f"Joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False, (self.__RED))
                    self.__screen.blit(self.__player3, (710, 220))
                    self.__screen.blit(self.__player1, (710, 320))
                    self.__screen.blit(self.__player2, (710, 400))
                    self.__screen.blit(self.__player4, (710, 480))
                    self.__screen.blit(self.__yellow_barrier, (1200, 205))
                    self.__screen.blit(self.__green_barrier, (1100, 325))
                    self.__screen.blit(self.__blue_barrier, (1100, 405))
                    self.__screen.blit(self.__red_barrier, (1100, 485))
                elif not multiplayer.is_server() and multiplayer.get_client().get_me_player() == 3:
                    self.__player4 = self.__48_font.render(
                        f"Vous êtes le joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False,
                        (self.__GREEN))
                    self.__player3 = self.__48_font.render(
                        f"Joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False,
                        (self.__YELLOW))
                    self.__player2 = self.__48_font.render(
                        f"Joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                        (self.__BLUE_PLAYER))
                    self.__player1 = self.__48_font.render(
                        f"Joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False, (self.__RED))
                    self.__screen.blit(self.__player4, (710, 220))
                    self.__screen.blit(self.__player1, (710, 320))
                    self.__screen.blit(self.__player2, (710, 400))
                    self.__screen.blit(self.__player3, (710, 480))
                    self.__screen.blit(self.__green_barrier, (1200, 205))
                    self.__screen.blit(self.__yellow_barrier, (1100, 325))
                    self.__screen.blit(self.__blue_barrier, (1100, 405))
                    self.__screen.blit(self.__red_barrier, (1100, 485))
        else:
            if self.__game.get_is_each_turn():
                self.__player1 = self.__48_font.render(
                    f"Joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False, self.__RED)
                self.__player2 = self.__48_font.render(
                    f"Joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                    self.__BLUE_PLAYER)
                self.__screen.blit(self.__player1, (710, 220))
                self.__screen.blit(self.__player2, (710, 320))
                self.__screen.blit(self.__red_barrier, (1200, 205))
                self.__screen.blit(self.__blue_barrier, (1100, 305))
                if len(self.__game.get_players()) == 4:
                    self.__player3 = self.__48_font.render(
                        f"Joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False, self.__YELLOW)
                    self.__player4 = self.__48_font.render(
                        f"Joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False, self.__GREEN)
                    self.__screen.blit(self.__player3, (710, 400))
                    self.__screen.blit(self.__player4, (710, 480))
                    self.__screen.blit(self.__yellow_barrier, (1100, 385))
                    self.__screen.blit(self.__green_barrier, (1100, 465))
            else:
                self.__player1 = self.__48_font.render(
                    f"Vous êtes le joueur 1:       X{int(self.__game.get_player(1).get_amount_barrier())}", False,
                    self.__RED)
                self.__player2 = self.__48_font.render(
                    f"Joueur 2:       X{int(self.__game.get_player(2).get_amount_barrier())}", False,
                    self.__BLUE_PLAYER)
                self.__screen.blit(self.__player1, (710, 220))
                self.__screen.blit(self.__player2, (710, 320))
                self.__screen.blit(self.__red_barrier, (1200, 205))
                self.__screen.blit(self.__blue_barrier, (1100, 305))
                if len(self.__game.get_players()) == 4:
                    self.__player3 = self.__48_font.render(
                        f"Joueur 3:       X{int(self.__game.get_player(3).get_amount_barrier())}", False, self.__YELLOW)
                    self.__player4 = self.__48_font.render(
                        f"Joueur 4:       X{int(self.__game.get_player(4).get_amount_barrier())}", False, self.__GREEN)
                    self.__screen.blit(self.__player3, (710, 400))
                    self.__screen.blit(self.__player4, (710, 480))
                    self.__screen.blit(self.__yellow_barrier, (1100, 385))
                    self.__screen.blit(self.__green_barrier, (1100, 465))

        pygame.display.flip()

    def loop_sounds(self, arg):
        if self.__is_mute:
            return
        if arg == "move":
            music = pygame.mixer.Sound("./songs/move_player.wav")
            pygame.mixer.find_channel().play(music)
        elif arg == "place":
            music = pygame.mixer.Sound("./songs/place_barrier.wav")
            pygame.mixer.find_channel().play(music)

    def loop_game(self):
        self.__player_leave = False
        self.__running = True
        pygame.display.update()
        self.play_music()
        while self.__running:
            pygame.time.Clock().tick(60)
            if not self.__game.is_started():
                self.stop_music()
                self.__game.change_is_started()
                music = pygame.mixer.Sound("./songs/victoire.wav")
                pygame.mixer.find_channel().play(music)
                self.loop_page_finish_game()
                return
            for event in pygame.event.get():
                if self.__show_popup:
                    self.pop_up_for_pause()
                # récupérer un event
                if event.type == pygame.QUIT:  # Si l'event est du type fermer la fenetre
                    if type(self.__game) == Multiplayer:
                        try:
                            if self.__mode == "multiplayer" or self.__mode == "game":
                                self.send_leave()
                        finally:
                            self.__running = False
                            pygame.quit()
                    self.stop_music()
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__song_image_pos.collidepoint(event.pos):
                        self.__is_mute = not self.__is_mute
                        if self.__is_mute:
                            self.stop_music()
                        else:
                            self.play_music()
                    elif self.__burger_pos.collidepoint(event.pos):
                        if type(self.__game) == Multiplayer:
                            self.send_pause_put()
                        self.pop_up_for_pause()
                    for rect, (i, j) in self.__cases_items.items():
                        if rect is not None and rect.collidepoint(event.pos):
                            case = self.__game.get_case(i, j)
                            if case.get_case_type() == CaseType.BLANK:
                                pass
                            elif case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                                if self.__game.place_barrier(i, j, BarrierType.HORIZONTAL):
                                    self.__game.get_current_player().decrease_amount_barrier()
                                    self.__game.switch_player()
                                    self.__is_update = True
                                    self.loop_sounds("place")
                            elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
                                if self.__game.place_barrier(i, j, BarrierType.VERTICAL):
                                    self.__game.get_current_player().decrease_amount_barrier()
                                    self.__game.switch_player()
                                    self.__is_update = True
                                    self.loop_sounds("place")
                            else:
                                if self.__game.move_player(i, j):
                                    self.__is_update = True
                                    self.loop_sounds("move")
                                    self.__game_current_player = self.__game.get_current_player()
                                    self.__turn_player = self.__48_font.render(
                                        f"Au tour du joueur " + str(self.__game_current_player), False,
                                        (self.__WHITE))
            self.game_page()

    def pop_up_for_pause(self):
        self.pop_up()
        self.__show_popup = True

        while self.__show_popup:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_resume.collidepoint(self.__cursor_pos):
                        if type(self.__game) == Multiplayer:
                            self.send_pause_stop()
                        self.__show_popup = False

    def pop_up(self):
        self.popup = pygame.Surface((1500, 850), pygame.SRCALPHA)
        self.popup.fill(self.__BLUE)

        self.__resume = self.__96_font.render("Reprendre", False, (self.__BLACK))
        self.__get_resume = self.__resume.get_rect()
        self.__get_resume.topleft = (650, 400)

        self.__screen.blit(self.popup, (0, 0))
        self.__screen.blit(self.__resume, (650, 400))

        pygame.display.update()

    def play_music(self):
        music = pygame.mixer.Sound("./songs/jazz.wav")
        self.__channel_music = pygame.mixer.find_channel()
        self.__channel_music.set_volume(0.5)
        self.__channel_music.play(music, loops=120)

    def stop_music(self):
        self.__channel_music.stop()

    def loop_page_finish_game(self):
        if self.__player_leave:
            self.loop_home_page()
            return
        self.page_finish_game()
        self.__running = True
        # Boucle du jeu
        while self.__running:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    self.__running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__cursor_pos = pygame.mouse.get_pos()
                    if self.__get_menu.collidepoint(self.__cursor_pos):
                        if type(self.__game) == Multiplayer:
                            if not self.__player_leave:
                                self.send_leave()
                            self.__stop_listen = False
                            if self.__game.is_server():
                                self.__game.get_server().close_socket()
                            else:
                                self.__game.get_client().close_socket()

                        self.loop_home_page()
                        self.__running = False
                    elif self.__get_restart.collidepoint(self.__cursor_pos):
                        has_leave = False
                        if self.__mode == "multiplayer" or self.__mode == "game":
                            if not self.__player_leave:
                                if type(self.__game) == Multiplayer:
                                    self.__game.reset_current_player_for_sends_and_receive()
                                    has_leave = True
                        if not has_leave:
                            self.stop_music()
                            self.__game.restart()
                            self.loop_game()
                            self.__running = False

    def send_leave(self):
        logout_json = {"type": "logout"}
        if self.__game.is_server():
            self.__game.get_server().send_message_server_all_client(logout_json, None)
        else:
            self.__game.get_client().send_message_client(logout_json)

    def send_pause_put(self):
        pause_json = {"type": "pause", "state": "put"}
        if self.__game.is_server():
            self.__game.get_server().send_message_server_all_client(pause_json, None)
        else:
            self.__game.get_client().send_message_client(pause_json)

    def send_pause_stop(self):
        pause_json = {"type": "pause", "state": "stop"}
        if self.__game.is_server():
            self.__game.get_server().send_message_server_all_client(pause_json, None)
        else:
            self.__game.get_client().send_message_client(pause_json)

    def page_finish_game(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__surface = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__surface, pygame.Color(64, 91, 67, 50), (250, 100, 1000, 600))

        colors = {
            1: self.__RED,
            2: self.__BLUE_BORDER,
            3: self.__YELLOW,
            4: self.__GREEN
        }

        id = self.__game.get_winner().get_id()

        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (450, 325, 625, 80))
        pygame.draw.rect(self.__surface, self.__DARK_BLUE, (450, 450, 625, 80))

        self.__winner = self.__64_font.render("Le joueur " + str(id) + " a gagné !",
                                              False, colors[id])
        self.__get_winner = self.__winner.get_rect()
        self.__get_winner.topleft = (565, 200)

        if not self.__player_leave:
            self.__restart = self.__48_font.render("Rejouer", False, self.__WHITE)
            self.__get_restart = self.__restart.get_rect()
            self.__get_restart.topleft = (690, 350)

        self.__menu = self.__48_font.render("Retourner au menu", False, self.__WHITE)
        self.__get_menu = self.__menu.get_rect()
        self.__get_menu.topleft = (625, 470)

        self.__screen.blit(self.__surface, (0, 0))
        self.__screen.blit(self.__restart, (690, 350))
        self.__screen.blit(self.__menu, (625, 470))
        self.__screen.blit(self.__winner, (565, 200))

        pygame.display.flip()  # Mettre a jour l'affichage
