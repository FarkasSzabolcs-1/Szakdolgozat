from tkinter import ttk
import tkinter as tk

class Matrixmenu(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()

    # ablak megjelenítése megnyitáskor
    def create_screen(self):
        """
        A matrix problemak bemutatasanak menujet a program megnyitaskor betolni
        """

        self.matrix_menu=ttk.Frame(self)
        ttk.Label(self, text="Mátrix problémák bemutatása", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self.matrix_menu, text="Összeadás", width=30, command=lambda:self.controller.show_screen("Matrixsum")).grid(row=2, column=0)
        ttk.Button(self.matrix_menu, text="Szorzás", width=30, command=lambda:self.controller.show_screen("Matrixmult")).grid(row=3, column=0)
        ttk.Button(self.matrix_menu, text="Transzponált mátrix", width=30, command=lambda:self.controller.show_screen("Matrixtranspose")).grid(row=4, column=0)
        ttk.Button(self.matrix_menu, text="Egyégmátrix", width=30, command=lambda:self.controller.show_screen("Matrixidentity")).grid(row=5, column=0)
        ttk.Button(self.matrix_menu, text="Inverz mátrix", width=30, command=lambda:self.controller.show_screen("Matrixinvert")).grid(row=6, column=0)
        ttk.Button(self.matrix_menu, text="Determináns", width=30, command=lambda:self.controller.show_screen("Matrixdeterminant")).grid(row=7, column=0)
        ttk.Button(self.matrix_menu, text="Háromszög mátrix", width=30, command=lambda:self.controller.show_screen("Matrixtriangle")).grid(row=8, column=0)
        ttk.Button(self.matrix_menu, text="Cramer szabály", width=30, command=lambda:self.controller.show_screen("Matrixcramer")).grid(row=9, column=0)
        (ttk.Button(self.matrix_menu, text="Vissza a problémákhoz", width=30, command=lambda: self.controller.show_screen("Problemsmenu"),style='Back.TButton')
         .grid(row=10,column=0))

        #menü elemek középre illesztése
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.matrix_menu.grid(row=1, column=0)