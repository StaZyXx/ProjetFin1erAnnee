import pygame


class View:
    def __init__(self):
        # Création des couleurs
        self.__WHITE = (255, 255, 255, 50)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (171, 242, 255, 50)
        self.__DARK_BLUE = (57, 73, 116, 200)
        self.__GREEN = (0, 255, 0)

        pygame.init()
        self.__font = pygame.font.SysFont('./fonts/Carme.ttf', 80, bold=False)
        pygame.display.set_caption("Quorridor")  # Nom de la fenêtre
        self.__screen = pygame.display.set_mode((1500, 850))  # Définit la taille de la fenetre
        self.__background = pygame.image.load("./assets/background.jpg").convert()  # Charge l'image

        #Création des tailles de polices
        self.__96_font = pygame.font.SysFont('./fonts/Carme.ttf', 96, bold=False)
        self.__64_font = pygame.font.SysFont('./fonts/Carme.ttf', 64, bold=False)
        self.__48_font = pygame.font.SysFont('./fonts/Carme.ttf', 48, bold=False)
        self.__32_font = pygame.font.SysFont('./fonts/Carme.ttf', 32, bold=False)

        self.__blue_image = pygame.Surface((1500, 850), pygame.SRCALPHA)

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

    def home_page(self):
        self.__screen.blit(self.__background, (0, 0))

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
        self.__get_leave.topleft = (700, 610)

        self.__screen.blit(self.__blue_image, (0, 0))
        self.__screen.blit(self.__quorridor, (620, 125))
        self.__screen.blit(self.__solo, (730, 315))
        self.__screen.blit(self.__multiplayer, (660, 460))
        self.__screen.blit(self.__leave, (700, 610))

        pygame.display.flip()  # Mettre a jour l'affichage

    def boucle_param(self, mode):
        self.couleur_2players, self.couleur_4players = self.__DARK_BLUE, self.__DARK_BLUE
        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE
        self.__nbr_joueur = None
        self.__size = None
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
                        self.__size = 5
                    elif self.__get_size_7x7.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE, self.__DARK_BLUE
                        self.__size = 7
                    elif self.__get_size_9x9.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN, self.__DARK_BLUE
                        self.__size = 9
                    elif self.__get_size_11x11.collidepoint(self.__cursor_pos):
                        self.__color_5x5, self.__color_7x7, self.__color_9x9, self.__color_11x11 = self.__DARK_BLUE, self.__DARK_BLUE, self.__DARK_BLUE, self.__GREEN
                        self.__size = 11
                    elif self.__get_less_barr.collidepoint(self.__cursor_pos):
                        if self.__nbr_barr > 4:
                            self.__nbr_barr -= 4
                    elif self.__get_more_barr.collidepoint(self.__cursor_pos):
                        if self.__nbr_barr < 40:
                            self.__nbr_barr += 4

                    self.param_game(mode)

    def param_game(self, mode):
        self.nbr_joueur = 2
        pygame.init()

        self.__size = (1500, 850)
        self.__blue_image2 = pygame.Surface(self.__size, pygame.SRCALPHA)

        # carré pricipale
        pygame.draw.rect(self.__blue_image2, self.__BLUE, (250, 200, 1000, 500))

        pygame.draw.rect(self.__blue_image2, self.__DARK_BLUE, (100, 100, 100, 100))
        self.__back = self.__font.render('Retour', False, (self.__WHITE))
        self.__get_back = self.__back.get_rect()
        self.__get_back.topleft = (100, 100)

        # choix nombre de joueur
        if mode != "multiplayer":
            pygame.draw.rect(self.__blue_image2, self.couleur_2players, (450, 250, 150, 100))
            pygame.draw.rect(self.__blue_image2, self.couleur_4players, (900, 250, 150, 100))

            self.__nbr_player2 = self.__font.render('2 joueurs', False, (self.__WHITE))
            self.__get_nbr_player2 = self.__nbr_player2.get_rect()
            self.__get_nbr_player2.topleft = (450, 250)

            self.__nbr_player4 = self.__font.render('4 joueurs', False, (self.__WHITE))
            self.__get_nbr_player4 = self.__nbr_player4.get_rect()
            self.__get_nbr_player4.topleft = (900, 250)

        # choix taille tableau

        pygame.draw.rect(self.__blue_image2, self.__color_5x5, (300, 400, 100, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_7x7, (500, 400, 100, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_9x9, (700, 400, 100, 50))
        pygame.draw.rect(self.__blue_image2, self.__color_11x11, (900, 400, 100, 50))

        self.__size_5x5 = self.__font.render('5x5', False, (self.__WHITE))
        self.__get_size_5x5 = self.__size_5x5.get_rect()
        self.__get_size_5x5.topleft = (300, 400)

        self.__size_7x7 = self.__font.render('7x7', False, (self.__WHITE))
        self.__get_size_7x7 = self.__size_7x7.get_rect()
        self.__get_size_7x7.topleft = (500, 400)

        self.__size_9x9 = self.__font.render('9x9', False, (self.__WHITE))
        self.__get_size_9x9 = self.__size_9x9.get_rect()
        self.__get_size_9x9.topleft = (700, 400)

        self.__size_11x11 = self.__font.render('11x11', False, (self.__WHITE))
        self.__get_size_11x11 = self.__size_11x11.get_rect()
        self.__get_size_11x11.topleft = (900, 400)

        # choix nombre barrière
        pygame.draw.rect(self.__blue_image2, self.__DARK_BLUE, (700, 500, 200, 50))

        self.__less_barr = self.__font.render('-', False, (self.__WHITE))
        self.__get_less_barr = self.__less_barr.get_rect()
        self.__get_less_barr.topleft = (700, 500)

        # nbr_barr = str(self.__nbr_barr)
        self.__show_nbr_barr = self.__font.render(str(self.__nbr_barr), False, (self.__WHITE))

        self.__more_barr = self.__font.render('+', False, (self.__WHITE))
        self.__get_more_barr = self.__more_barr.get_rect()
        self.__get_more_barr.topleft = (900, 500)

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
        self.__screen.blit(self.__size_5x5, (300, 400))
        self.__screen.blit(self.__size_7x7, (500, 400))
        self.__screen.blit(self.__size_9x9, (700, 400))
        self.__screen.blit(self.__size_11x11, (900, 400))

        # choice barr
        self.__screen.blit(self.__less_barr, (700, 500))
        self.__screen.blit(self.__show_nbr_barr, (800, 500))
        self.__screen.blit(self.__more_barr, (900, 500))

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

    def choice_server_client(self):
        pygame.init()
        self.__blue_image3 = pygame.Surface((1500, 850), pygame.SRCALPHA)

        pygame.draw.rect(self.__blue_image3, self.__BLUE, (50, 50, 1400, 750))
        pygame.draw.rect(self.__blue_image3, self.__DARK_BLUE, (200, 200, 1100, 150))
        pygame.draw.rect(self.__blue_image3, self.__DARK_BLUE, (200, 400, 1100, 150))

        self.__server = self.__font.render("Créer", False, (self.__WHITE))
        self.__get_server = self.__server.get_rect()
        self.__get_server.topleft = (700, 250)

        self.__client = self.__font.render("Rejoindre", False, (self.__WHITE))
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


View()
