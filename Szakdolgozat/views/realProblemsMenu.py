import tkinter as tk
from tkinter import ttk

class Realproblemsmenu(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()

    def create_screen(self):
        """
        A program betolti a linearis algebra mindennapokban hasznalt peldait
        """
        self.real_problems_menu=ttk.Frame(self)
        ttk.Label(self, text="Lineáris algebra a mindennapokban", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self.real_problems_menu, text="Képfeldolgozás", width=30, command=lambda:self.controller.show_screen("Imageprocessing")).grid(row=2, column=0)
        ttk.Button(self.real_problems_menu, text="Portfolió optimalizálás", width=30, command=lambda:self.controller.show_screen("Portfoliooptimization")).grid(row=3, column=0)
        ttk.Button(self.real_problems_menu, text="Lineáris programozás", width=30, command=lambda:self.controller.show_screen("Linearprogramming")).grid(row=4, column=0)


        ttk.Button(self.real_problems_menu, text="Vissza a problémákhoz", width=30, command=lambda: self.controller.show_screen("Problemsmenu"),style='Back.TButton').grid(row=7,column=0)

        # elemek kozepre illesztese
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.real_problems_menu.grid(row=1, column=0)