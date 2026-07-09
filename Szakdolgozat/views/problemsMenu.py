import tkinter as tk
from tkinter import ttk

class Problemsmenu(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()

    def create_screen(self):
        """
        A program betolti a problemak kategorizalt menujet
        """
        self.problem_menu=ttk.Frame(self)

        ttk.Label(self, text="Lineáris algebrai problémák menü", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self.problem_menu, text="Mátrix műveletek", width=30, command=lambda:self.controller.show_screen("Matrixmenu")).grid(row=2, column=0)
        ttk.Button(self.problem_menu, text="Vektor műveletek", width=30, command=lambda:self.controller.show_screen("Vectormenu")).grid(row=3, column=0)
        ttk.Button(self.problem_menu, text="Vektorterek", width=30, command=lambda:self.controller.show_screen("Vectorspacemenu")).grid(row=4, column=0)
        ttk.Button(self.problem_menu, text="Lineáris algebra a mindennapokban", width=30, command=lambda:self.controller.show_screen("Realproblemsmenu")).grid(row=5, column=0)
        ttk.Button(self.problem_menu, text="Vissza a főmenübe", width=30, command=lambda: self.controller.show_screen("Mainmenu"),style='Back.TButton').grid(row=7,column=0)


        #elemek kozepre illesztese
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.problem_menu.grid(row=1, column=0)
