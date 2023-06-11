import threading
import time
import tkinter
from tkinter import *
from tkinter import messagebox as mb, Text

import direction
import network
from case import CaseType, BarrierType

from game import Game
from multiplayer import Multiplayer
from network import Client

class View:
    def __init__(self):
        self.game = None
        self.__game_frame = None
        self.__root = Tk()
        self.__root.geometry('1200x800')
        self.__root.title("Quoridor")

        self.nbr_player = 2

        self.init_main_page()
        self.__root.mainloop()

    def init_main_page(self):
        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        soloButton = Button(self.__selection_frame, height=1, width=10, text="Solo",
                            command=lambda: self.init_final_page())
        soloButton.config(bg='white')
        soloButton.grid(row=0, column=0)

        multiButton = Button(self.__selection_frame, height=1, width=10, text="Multi",
                             command=lambda: self.init_multiplayer_page())
        multiButton.config(bg='white')
        multiButton.grid(row=1, column=0)

    def init_multiplayer_page(self):
        self.__selection_frame.destroy()
        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        createButton = Button(self.__selection_frame, height=1, width=10, text="Créer",
                              command=lambda: self.create_game_with_thread())
        createButton.config(bg='white')
        createButton.grid(row=0, column=0)

        joinButton = Button(self.__selection_frame, height=1, width=10, text="Rejoindre",
                            command=lambda: self.init_join_page())
        joinButton.config(bg='white')
        joinButton.grid(row=1, column=0)

    def create_game_with_thread(
            self):  # permet le lancement de la recherche des joueur directement après le choix de création d'une partie
        self.game = Multiplayer(True, self.nbr_player)
        thread = threading.Thread(target=self.game.wait_for_all_players)  # création du thread
        thread.start()  # lancement du thread
        self.init_create_page(thread)  # lancement de la page de selction de jeu

    def init_create_page(self, thread):
        self.__selection_frame.destroy()
        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        sizeLabel = Label(self.__selection_frame, text="Taille du jeu : ")
        sizeLabel.config(bg='white')
        sizeLabel.grid(row=0, column=0)

        self.__sizeText = Text(self.__selection_frame, height=1, width=20, bg='white')

        self.__sizeText.grid(row=0, column=1)

        startButton = Button(self.__selection_frame, height=1, width=10, text="Commencez",
                             command=lambda: self.check_if_player_have_join(thread))
        startButton.config(bg='white')
        startButton.grid(row=2, column=0)

        address = network.get_address_ip()
        ip_address_label = Label(self.__selection_frame, text=address)
        ip_address_label.config(bg='white')
        ip_address_label.grid(row=3, column=0)

    def check_if_player_have_join(self,
                                  thread):  # pour ne pas lancer la game si il y a pas les joueurs et que la taille est mauvaise
        size = self.__sizeText.get("1.0", "end-1c")
        if thread.is_alive():
            mb.showerror("Erreur", "Les Joueurs ne sont pas tous la")
            return
        else:
            if size == "7" or size == "9" or size == "11":
                self.can_start(self.game, "server")
            else:
                mb.showerror("Erreur", "La taille de jeu choisi n'est pas bonne")

    def init_join_page(self):
        self.__selection_frame.destroy()
        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)
        ipLabel = Label(self.__selection_frame, text="IP du serveur : ")
        ipLabel.config(bg='white')
        ipLabel.grid(row=0, column=0)
        self.__ipText = Text(self.__selection_frame, height=1, width=20, bg='white')
        self.__ipText.grid(row=0, column=1)
        startButton = Button(self.__selection_frame, height=1, width=10, text="Commencez",
                             command=self.can_join)
        startButton.config(bg='white')
        startButton.grid(row=2, column=0)

    def init_final_page(self):
        self.__selection_frame.destroy()
        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        sizeLabel = Label(self.__selection_frame, text="Taille du jeu : ")
        sizeLabel.config(bg='white')
        sizeLabel.grid(row=0, column=0)

        self.__sizeText = Text(self.__selection_frame, height=1, width=20, bg='white')

        self.__sizeText.grid(row=0, column=1)

        startButton = Button(self.__selection_frame, height=1, width=10, text="Commencez",
                             command=lambda: self.can_start(Game()))
        startButton.config(bg='white')
        startButton.grid(row=2, column=0)

    def can_join(self):
        ip = self.__ipText.get("1.0", "end-1c")
        if not ip:
            mb.showerror("Erreur", "Veuillez remplir les champs IP !")
            return
        client = Client(ip)
        response = client.connect()
        if response == 0:
            mb.showerror("Erreur", "Impossible de se connecter au serveur !")
            return
        self.create_lobby(client)

    def create_lobby(self, client):
        self.__selection_frame.destroy()
        self.__lobby_frame = tkinter.Frame(self.__root)
        self.__lobby_frame.config(bg='white')
        self.__lobby_frame.grid(row=0, column=1, padx=25)

        self.__players = Label(self.__lobby_frame, text="Joueurs : ")

        self.__players.config(bg='white')
        self.__players.grid(row=0, column=0)

        self.__players_list = Listbox(self.__lobby_frame, height=5, width=20, bg='white')
        self.__players_list.grid(row=0, column=1)

        self.game = Multiplayer(False, self.nbr_player, client)

        thread_join = threading.Thread(target=self.start_lobby)
        thread_join.start()

    def start_lobby(self):
        dico = {"type": "None"}
        while dico["type"] != "parameter":
            dico = self.game.get_client().receipt_message_client()
            if dico["type"] == "player":
                print(f"Le player {dico['num_player']} à rejoins la partie")
                self.__players_list.insert(END, f"Player {dico['num_player']}")
        self.__lobby_frame.destroy()
        self.can_start(self.game, "client", dico)

    def can_start(self, game, gamer="base", info_game=None):

        global size
        if gamer == "base":
            self.game = game
        if gamer == "client":
            size = info_game["size"]
        elif gamer == "server" or gamer == "base":
            size = self.__sizeText.get("1.0", "end-1c")
        if not size.isnumeric():
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 3 et 12 \ndans la case colonne !")
            return
        elif gamer == "server":
            info_game = {"type": "parameter", "size": size}
            self.game.get_server().send_message_server_all_client(info_game, None)
        size = int(eval(size))
        if size == 7 or size == 9 or size == 11:
            self.__selection_frame.destroy()
            self.__game_frame = tkinter.Frame(self.__root)
            self.__game_frame.grid(row=0, column=0, rowspan=5)
            self.__root.bind('z', lambda event: self.key_board(direction.Direction.NORTH))
            self.__root.bind('q', lambda event: self.key_board(direction.Direction.WEST))
            self.__root.bind('s', lambda event: self.key_board(direction.Direction.SOUTH))
            self.__root.bind('d', lambda event: self.key_board(direction.Direction.EAST))
            print(size)
            self.game.start(size, self.nbr_player)

            self.show_board()
        else:
            mb.showerror("Erreur", "Veuillez choisir une taille de jeux conforme !")

        if type(game) == Multiplayer:
            thread2 = threading.Thread(target=self.manage_game_action)  # création du thread
            thread2.start()

            # TODO : ADD THREAD ON START
            game.managements_sends()

    def manage_game_action(self):
        while True:
            time.sleep(1)
            if self.game.get_have_play():
                self.show_board()
                self.game.change_have_play()

    def show_board(self):
        cases = self.game.get_cases()
        for i in range(len(cases)):
            for j in range(len(cases[i])):
                self.show_case(cases[i][j], i, j)

    def show_case(self, case, x, y):
        canvas = tkinter.Canvas(self.__game_frame)
        if case.get_case_type() == CaseType.BARRIER:
            if case.get_barrier_type() == BarrierType.VERTICAL:
                canvas.grid(row=x, column=y, padx=0, pady=0)
                canvas.config(width=5, height=32, highlightbackground="red", highlightcolor="red",
                              highlightthickness=1)
                canvas.create_rectangle(0, 0, 5, 32, fill="black")
            else:
                canvas.grid(row=x, column=y, padx=0, pady=0)
                canvas.config(width=32, height=5, highlightbackground="red", highlightcolor="red",
                              highlightthickness=1)
                canvas.create_rectangle(0, 0, 32, 5, fill="black")

        elif case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
            canvas.grid(row=x, column=y, padx=0, pady=0)
            canvas.config(width=32, height=5, highlightbackground="red", highlightcolor="red",
                          highlightthickness=1)
            canvas.create_rectangle(0, 0, 32, 5, fill="white")
            canvas.bind("<Button-1>", lambda event: self.click(x, y))
        elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
            canvas.grid(row=x, column=y, padx=0, pady=0)
            canvas.config(width=5, height=32, highlightbackground="red", highlightcolor="red",
                          highlightthickness=1)
            canvas.create_rectangle(0, 0, 5, 32, fill="white")
            canvas.bind("<Button-1>", lambda event: self.click(x, y))
        elif case.has_player():
            canvas.grid(row=x, column=y, padx=0, pady=0)
            canvas.config(width=32, height=32, highlightbackground="red", highlightcolor="red",
                          highlightthickness=1)
            canvas.create_oval(0, 0, 32, 32, fill="red")
        elif case.get_case_type() != CaseType.BLANK:
            canvas.create_rectangle(0, 0, 32, 32, fill="white")
            canvas.grid(row=x, column=y, padx=0, pady=0)
            canvas.config(width=32, height=32, highlightbackground="red", highlightcolor="red",
                          highlightthickness=1)
            canvas.bind("<Button-1>", lambda event: self.click(x, y))

    def click(self, x, y):
        case = self.game.get_case(x, y)
        if case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL or case.get_case_type() == \
                CaseType.SLOT_BARRIER_VERTICAL:
            print("barrier")
            if case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                self.game.place_barrier(x, y, BarrierType.HORIZONTAL)

            else:
                self.game.place_barrier(x, y, BarrierType.VERTICAL)

            self.show_board()
        else:
            self.game.move_player(x, y)
            self.show_board()

    def key_board(self, target_direction):
        print("key", target_direction)
        if not self.game.is_started():
            return
        self.game.move_player_with_direction(target_direction)
        self.show_board()
