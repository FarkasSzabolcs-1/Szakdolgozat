import tkinter as tk
from tkinter import ttk

class Vectormenu(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()

    def create_screen(self):
        """
        A program betolti a vektor problemak menujet
        """
        self.vector_menu=ttk.Frame(self)
        ttk.Label(self, text="Vektor problémák bemutatása", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self.vector_menu, text="Vektor hossza (norma)", width=30, command=lambda:self.controller.show_screen("Vectorlenght")).grid(row=2, column=0)
        ttk.Button(self.vector_menu, text="Összeadás", width=30, command=lambda:self.controller.show_screen("Vectorsum")).grid(row=3, column=0)
        ttk.Button(self.vector_menu, text="Skalárral való szorzás", width=30, command=lambda:self.controller.show_screen("Vectormult")).grid(row=4, column=0)
        ttk.Button(self.vector_menu, text="Lineáris kombináció", width=30, command=lambda:self.controller.show_screen("Vectorlinearcombination")).grid(row=5, column=0)
        ttk.Button(self.vector_menu, text="Két vektor sakláris szorzata", width=30, command=lambda:self.controller.show_screen("Vectorscalarmult")).grid(row=6, column=0)
        ttk.Button(self.vector_menu, text="Vektoriális szorzat", width=30, command=lambda:self.controller.show_screen("Vectorialmult")).grid(row=7, column=0)
        ttk.Button(self.vector_menu, text="Háromszög megoldás", width=30, command=lambda:self.controller.show_screen("Trianglesolution")).grid(row=8, column=0)
        ttk.Button(self.vector_menu, text="Vissza a problémákhoz", width=30, command=lambda: self.controller.show_screen("Problemsmenu"),style='Back.TButton').grid(row=10,column=0)

        # elemek kozepre illesztese
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.vector_menu.grid(row=1, column=0)