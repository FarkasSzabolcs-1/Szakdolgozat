import tkinter as tk
from tkinter import ttk

class Mainmenu(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.create_screen()


    def create_screen(self):
        """
        A program betolti a fomenut
        """
        # fomenu megjelenítése
        self.mainmenu=ttk.Frame(self)
        ttk.Label(self, text=f"Lineáris algebrai problémák\n"
                             f" számítógépes prezentálása",style='Title.TLabel').grid(row=0, column=0,rowspan=1)
        ttk.Button(self.mainmenu, text="Problémák", width=30, command=lambda:self.controller.show_screen('Problemsmenu')).grid(row=0,column=0)
        ttk.Button(self.mainmenu, text="Kilépés", width=30, command=self.kilepes,style='Back.TButton').grid(row=2, column=0)

        #menü elemek középre illesztése
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1, weight=1)
        self.mainmenu.grid(row=1,column=0)

    def kilepes(self):
        """
        A program leallitja a mainloop-ot, majd torli a fo ablakot, ezzel bezarva teljesen
        """

        self.winfo_toplevel().quit()
        self.winfo_toplevel().destroy()
