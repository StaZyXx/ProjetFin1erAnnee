from tkinter import *

class Affichage:
    def __init__(self):
        root = Tk()
        root.geometry('1200x800')
        root.title("Quoridor")
        frame_left = Frame(root).grid(row=0, column=0)
        frame_left.pack()
        frame_right = Frame(root).grid(row=0, column=1)
        frame_right.pack()
        button_restart = Button(frame_right, text="Bouton redémarrer")
        button_restart.pack()
        root.mainloop()


jeu = Affichage()
jeu()