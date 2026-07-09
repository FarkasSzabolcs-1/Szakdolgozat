import tkinter as tk
from tkinter import ttk

class Vectorspacemenu(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()

    def create_screen(self):
        """
        A program betolti a vektorterek problemainak menujet
        :return:
        """
        self.vector_menu=ttk.Frame(self)
        ttk.Label(self, text="Vektortér műveletek ", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self.vector_menu, text="Vektorterek", width=30, command=lambda:self.controller.show_screen("Vectorspaces")).grid(row=2, column=0)
        ttk.Button(self.vector_menu, text="Alterek", width=30, command=lambda:self.controller.show_screen("Vectorsubspaces")).grid(row=3, column=0)
        ttk.Button(self.vector_menu, text="Lineáris függetlenség", width=30, command=lambda:self.controller.show_screen("Linearindependence")).grid(row=4, column=0)
        ttk.Button(self.vector_menu, text="Bázis", width=30, command=lambda:self.controller.show_screen("Bases")).grid(row=5, column=0)
        ttk.Button(self.vector_menu, text="Bázis transzformáció", width=30, command=lambda:self.controller.show_screen("Basetransformation")).grid(row=6, column=0)
        ttk.Button(self.vector_menu, text="Mátrix rangja", width=30, command=lambda:self.controller.show_screen("Matrixrank")).grid(row=7, column=0)
        ttk.Button(self.vector_menu, text="Lineáris egyenletrendszerek", width=30, command=lambda:self.controller.show_screen("Linearequations")).grid(row=8, column=0)
        ttk.Button(self.vector_menu, text="Vissza a problémákhoz", width=30, command=lambda: self.controller.show_screen("Problemsmenu"),style='Back.TButton').grid(row=10,column=0)

        #elemek kozepre illesztese
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.vector_menu.grid(row=1, column=0)