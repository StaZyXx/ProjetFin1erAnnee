from tkinter import *
from random import *


class Case:

    def __init__(self):
        self.__nbr_pion = 0
        self.__joueur = 0

    def increment_pion(self):
        self.__nbr_pion += 1

    def get_nbr_pion(self):
        return self.__nbr_pion

    def get_joueur(self):
        return self.__joueur


class Jeu:

    def __init__(self, x, y, nbr_joueur):
        self.__place = False
        self.__currentPlayer = 1
        self.tableau = []
        for i in range(x):
            self.tableau.append([])
            for j in range(y):
                self.tableau[i].append(Case())

    def get_tableau(self):
        return self.tableau[0][0].get_nbr_pion()

    def place_joueur(self, x, y, joueur_2):
        if self.tableau[x][y].get_joueur() == joueur_2 or self.tableau[x][y].joueur == 0:
            self.tableau[x][y].increment_pion()
            self.case_full(x, y, joueur_2)
            self.switch_player()
            if self.__place:
                self.update_players()

    def switch_player(self):
        if self.__currentPlayer != len(self.liste_player):
            self.__currentPlayer += 1
        else:
            self.__currentPlayer = 1
            self.__place = True

    def update_players(self):
        for i in self.liste_player:
            if not self.check_player(i):
                self.list_player.pop(i)

    def check_player(self, player):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                case = self.tableau[i][j]
                if player == case.get_joueur():
                    return True
        return False

    def check_case(self, i, j):
        if (i == 0 and j == 0) or (i == len(self.tableau) - 1 and j == 0) or (
                j == len(self.tableau) - 1 and i == 0) or (
                i == len(self.tableau) - 1 and j == len(self.tableau) - 1):
            return 2
        elif (i == 0) or (i == len(self.tableau) - 1) or (j == 0) or (j == len(self.tableau) - 1):
            return 3
        elif (i != 0) and (i != len(self.tableau) - 1) and (j != 0) and (j != len(self.tableau) - 1):
            return 4

    def case_full(self, i, j, joueur):
        position_case = self.check_case(i, j)  # point nécessaire
        if self.tableau[i][j].get_nbr_pion() == position_case:
            if i - 1 >= 0:
                self.tableau[i - 1][j].nbr_pion += 1
                self.tableau[i - 1][j].joueur = joueur
                self.case_full(i - 1, j, joueur)
            if j - 1 >= 0:
                self.tableau[i][j - 1].nbr_pion += 1
                self.tableau[i][j - 1].joueur = joueur
                self.case_full(i, j - 1, joueur)
            if i + 1 < len(self.tableau):
                self.tableau[i + 1][j].nbr_pion += 1
                self.tableau[i + 1][j].joueur = joueur
                self.case_full(i + 1, j, joueur)
            if j + 1 < len(self.tableau):
                self.tableau[i][j + 1].nbr_pion += 1
                self.tableau[i][j + 1].joueur = joueur
                self.case_full(i, j + 1, joueur)
            self.tableau[i][j].nbr_pion = 0
            self.tableau[i][j].joueur = 0


# jeu = Jeu(5,5)


class Affichage:
    def __init__(self):
        # ----------------------------- 1 ère page -----------------------------
        self.__page = Tk()
        self.__page.title("Paramètre")
        self.__page.geometry("300x150")
        self.__x = 0
        self.__y = 0
        self.__nbr_joueur = 0

        self.plateau = 0

        self.__barre_texte = Entry(self.__page, width=20)
        self.__barre_texte.insert(0, "6")  # c'est y
        self.__barre_texte.pack(pady=10)  # c'est x
        self.__barre_texte1 = Entry(self.__page, width=20)
        self.__barre_texte1.insert(0, "6")
        self.__barre_texte1.pack(pady=10)
        self.__barre_texte_joueur = Entry(self.__page, width=20)
        self.__barre_texte_joueur.insert(0, "2")
        self.__barre_texte_joueur.pack(pady=10)
        self.__bouton = Button(self.__page, height=1, width=10, text="Start", command=self.getEntry)
        self.__bouton.pack()
        self.__page.mainloop()

        # ----------------------------- 2 ème page -----------------------------

        self.__root = Tk()
        self.__root.title("Page de jeu")

        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0, rowspan=2)
        self.__frame1.config(bg="white")

        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=self.__y * 71, height=self.__x * 71, highlightthickness=0, bd=0, bg="#FFF")
        self.__canvas.pack()
        self.__canvas.bind('<Button-1>', self.clic)

        self.show_board()

        self.carre = 0

    # ----------------------------- fin init -----------------------------

    # ----------------------------- 1 ère page -----------------------------

    def getEntry(self):
        x = int(self.__barre_texte1.get())  # c'est x
        y = int(self.__barre_texte.get())  # c'est y
        nb_joueur = int(self.__barre_texte_joueur.get())
        if 3 <= x <= 10:
            if 3 <= y <= 12:
                if 2 <= nb_joueur <= 8:
                    self.__x = x
                    self.__y = y
                    self.__nbr_joueur = nb_joueur
                    self.plateau = Jeu(x, y, nb_joueur)
                    self.__page.destroy()

    # ----------------------------- 2 ème page -----------------------------

    def getelementbyid(self, i, j):
        print("couleur :")
        print(self.plateau.tableau[i][j].joueur)
        print("nbr_pion :")
        print(self.plateau.tableau[i][j].nbr_pion)

    def getx(self):
        return self.__x

    def show_board(self):
        y = -71
        for i in range(len(self.plateau.tableau)):
            x = 0
            y += 71
            for j in range(len(self.plateau.tableau[i])):
                if self.plateau.tableau[i][j].get_joueur() == 0:
                    couleur = "white"
                elif self.plateau.tableau[i][j].get_joueur() == 1:
                    couleur = "yellow"
                elif self.plateau.tableau[i][j].get_joueur() == 2:
                    couleur = "blue"
                elif self.plateau.tableau[i][j].get_joueur() == 3:
                    couleur = "green"
                elif self.plateau.tableau[i][j].get_joueur() == 4:
                    couleur = "red"
                elif self.plateau.tableau[i][j].get_joueur() == 5:
                    couleur = "orange"
                elif self.plateau.tableau[i][j].get_joueur() == 6:
                    couleur = "purple"
                elif self.plateau.tableau[i][j].get_joueur() == 7:
                    couleur = "pink"
                elif self.plateau.tableau[i][j].get_joueur() == 8:
                    couleur = "brown"
                self.carre = self.__canvas.create_rectangle(x, y, x + 70, y + 70, fill=couleur)
                if self.plateau.tableau[i][j].get_nbr_pion() == 1:
                    self.carre = self.__canvas.create_oval(x + 30, y + 30, x + 40, y + 40, fill="black", width=5)
                if self.plateau.tableau[i][j].get_nbr_pion() == 2:
                    self.carre = self.__canvas.create_oval(x + 20, y + 20, x + 30, y + 30, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 50, y + 50, x + 40, y + 40, fill="black", width=5)
                if self.plateau.tableau[i][j].get_nbr_pion() == 3:
                    self.carre = self.__canvas.create_oval(x + 10, y + 10, x + 20, y + 20, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 30, y + 30, x + 40, y + 40, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 50, y + 50, x + 60, y + 60, fill="black", width=5)
                if self.plateau.tableau[i][j].get_nbr_pion() == 4:
                    self.carre = self.__canvas.create_oval(x + 8, y + 8, x + 16, y + 16, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 24, y + 24, x + 32, y + 32, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 40, y + 40, x + 48, y + 48, fill="black", width=5)
                    self.carre = self.__canvas.create_oval(x + 56, y + 56, x + 64, y + 64, fill="black", width=5)
                x += 71
        self.__root.mainloop()

    def clic(self, event):
        x = event.x
        x = x * self.__x // (71 * self.__x)
        y = event.y
        y = event.y * self.__y // (71 * self.__y)
        print(x, y)
        return x, y


page = Affichage()
