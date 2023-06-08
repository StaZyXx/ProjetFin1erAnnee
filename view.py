import tkinter
from tkinter import *
from tkinter import messagebox as mb, Text

import direction
from case import CaseType, BarrierType
class View:
    def __init__(self, game):
        self.__game_frame = None
        self.__root = Tk()
        self.__root.geometry('1200x800')
        self.__root.title("Quoridor")

        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        sizeLabel = Label(self.__selection_frame, text="Taille du jeu : ")
        sizeLabel.config(bg='white')
        sizeLabel.grid(row=0, column=0)

        self.__sizeText = Text(self.__selection_frame, height=1, width=20, bg='white')

        self.__sizeText.grid(row=0, column=1)

        startButton = Button(self.__selection_frame, height=1, width=10, text="Commencez",
                             command=lambda: self.canStart(game))
        startButton.config(bg='white')
        startButton.grid(row=2, column=0)

        self.__root.mainloop()

    def canStart(self, game):

        size = self.__sizeText.get("1.0", "end-1c")
        if not size.isnumeric():
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 3 et 12 \ndans la case colonne !")
            return
        size = int(eval(size))

        print(size)
        if size == 7 or size == 9 or size == 11:
            self.__selection_frame.destroy()
            self.__game_frame = tkinter.Frame(self.__root)
            self.__game_frame.grid(row=0, column=0, rowspan=5)
            self.__root.bind('z', lambda event: self.key_board(direction.Direction.NORTH, game))
            self.__root.bind('q', lambda event: self.key_board(direction.Direction.WEST, game))
            self.__root.bind('s', lambda event: self.key_board(direction.Direction.SOUTH, game))
            self.__root.bind('d', lambda event: self.key_board(direction.Direction.EAST, game))
            game.start(size, 2)

            self.show_board(game)
        else:
            mb.showerror("Erreur", "Veuillez choisir une taille de jeux conforme !")

    def show_board(self, game):
        cases = game.get_cases()
        for i in range(len(cases)):
            for j in range(len(cases[i])):
                self.show_case(cases[i][j], i, j, game)

    def show_case(self, case, x, y, game):
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
            canvas.bind("<Button-1>", lambda event: self.click(x, y, game))
        elif case.get_case_type() == CaseType.SLOT_BARRIER_VERTICAL:
            canvas.grid(row=x, column=y, padx=0, pady=0)
            canvas.config(width=5, height=32, highlightbackground="red", highlightcolor="red",
                        highlightthickness=1)
            canvas.create_rectangle(0, 0, 5, 32, fill="white")
            canvas.bind("<Button-1>", lambda event: self.click(x, y, game))
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
            canvas.bind("<Button-1>", lambda event: self.click(x, y, game))

    def click(self, x, y, game):
        if not game.is_started():
            return
        case = game.get_case(x, y)
        if case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL or case.get_case_type() == \
                CaseType.SLOT_BARRIER_VERTICAL:
            print("barrier")
            if case.get_case_type() == CaseType.SLOT_BARRIER_HORIZONTAL:
                game.place_barrier(x, y, BarrierType.HORIZONTAL)
            else:
                game.place_barrier(x, y, BarrierType.VERTICAL)
            self.show_board(game)
        else:
            game.move_player(x, y)
            self.show_board(game)

    def key_board(self, direction, game):
        print("key", direction)
        if not game.is_started():
            return
        game.move_player_with_direction(direction)
        self.show_board(game)
