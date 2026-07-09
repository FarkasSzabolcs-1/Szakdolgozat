import random
import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Vectorlinearcombination(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.solver_controller=solver_handler
        self.create_screen()


    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Vektorok lineáris kombinációja", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza", style='Back.TButton',
                   command=lambda: self.controller.show_screen("Vectormenu")).grid(row=1, column=0, sticky="w")
        title_frame.grid(row=0, column=0)

        # tabcontrol létrehozása a generálási módszerek, valamint a tulajdonságok elkülönítéséhez
        self.tabcontrol = ttk.Notebook(self)
        self.tabcontrol.grid(row=2, column=0,sticky='we')

        # frame-k létrehozása a két generálási módszerhez
        self.pelda_adatok = ttk.Frame(self.tabcontrol)
        self.sajat_adatok = ttk.Frame(self.tabcontrol)
        self.tulajdonsagok = ttk.Frame(self.tabcontrol)

        # tabcontrol-hoz hozzáadása ezeknek a frameknek
        self.tabcontrol.add(self.pelda_adatok, text="Példa adatok")
        self.tabcontrol.add(self.sajat_adatok, text="Saját adatok")
        self.tabcontrol.add(self.tulajdonsagok, text="Tulajdonságok")

        # meghívjuk mindhárom tabot
        self.build_example_datas()
        self.build_empty_datas()
        self.show_rules()

        #framek alaphelyzetbe allitasa
        self.secondary_frame = None
        self.block3 = None
        self.block4 = None
        self.result_frame = None
        self.error_frame = None
        self.diagram_frame = None

        #kozepre igazitas
        self.columnconfigure(0, weight=1)

    def show_rules(self):
        """
        Betolti az altalanos es matematikai tulajdonsagokat a problemahoz kapcsolodoan
        """
        tab = self.tulajdonsagok
        tab.columnconfigure(0, weight=1)
        general_rules = ttk.LabelFrame(tab, text='Általános ismertetők')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Példa adatok tab: Random generált értékek.').grid(row=0, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Saját adatok tab: Felhasználó által megadott értékek.').grid(row=1, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Üres mezőket a program nem fogad el.').grid(row=2, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Vektorok lineáris kombinációja')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Két vektor, u és v lineáris kombinációja alatt azt a műveletet értjük, amikor a vektorokat megszorozzuk egy-egy skalár számmal, majd az így kapott szorzatvektorokat összeadjuk.').grid(
            row=0, column=0, sticky='we')


        general_rules.grid(row=0, column=0, sticky='nsew')
        general_rules.columnconfigure(0, weight=1)
        math_rules.grid(row=1, column=0, sticky='nsew')
        math_rules.columnconfigure(0, weight=1)

    def build_example_datas(self):
        """
        generalas gomb, megnyomasa utan a mezoket elore generalt ertekekkel feltolti
        """
        tab = self.pelda_adatok
        tab.columnconfigure(0,weight=1)


        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)

        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0)

        tab.columnconfigure(0, weight=1)

    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0,weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)

        main_grid.grid(row=0, column=0,columnspan=2)

        ttk.Button(main_grid, text="Vektor létrehozása", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0)

        tab.columnconfigure(0, weight=1)

    def vector_create(self,tab):
        """
        A generalas gomb lenyomasa utan a program legeneralja a problemanak megfelelo beviteli mezoket
        :param tab:     frame amivel dolgozunk
        """

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        # beviteli mezok elokeszitese
        input_frames = ttk.Frame(tab)

        block1 = ttk.LabelFrame(input_frames, text="u vektor koordinátái")
        block2 = ttk.LabelFrame(input_frames, text="v vektor koordinátái")
        block3 = ttk.LabelFrame(input_frames, text="a skalár")
        block4 = ttk.LabelFrame(input_frames, text="b skalár")



        input_frames.grid(row=1, column=0)

        # u vektor
        ttk.Label(block1, text="x = ").grid(row=2, column=0)
        vector1_x = ttk.Entry(block1)
        vector1_x.grid(row=2, column=1)
        ttk.Label(block1, text="y = ").grid(row=3, column=0)
        vector1_y = ttk.Entry(block1)
        vector1_y.grid(row=3, column=1)
        ttk.Label(block1, text="z = ").grid(row=4, column=0)
        vector1_z = ttk.Entry(block1)
        vector1_z.grid(row=4, column=1)

        block1.grid(row=2, column=0)

        # v vektor
        ttk.Label(block2, text="x = ").grid(row=2, column=0)
        vector2_x = ttk.Entry(block2)
        vector2_x.grid(row=2, column=1)
        ttk.Label(block2, text="y = ").grid(row=3, column=0)
        vector2_y = ttk.Entry(block2)
        vector2_y.grid(row=3, column=1)
        ttk.Label(block2, text="z = ").grid(row=4, column=0)
        vector2_z = ttk.Entry(block2)
        vector2_z.grid(row=4, column=1)

        block2.grid(row=2, column=1)


        # a skalar
        ttk.Label(block3, text="a = ").grid(row=2, column=0)
        vector1_scalar = ttk.Entry(block3)
        vector1_scalar.grid(row=2, column=1)

        block3.grid(row=3, column=0)

        # b skalar
        ttk.Label(block4, text="b = ").grid(row=2, column=0)
        vector2_scalar = ttk.Entry(block4)
        vector2_scalar.grid(row=2, column=1)

        block4.grid(row=3, column=1)

        input_frames.columnconfigure(0, weight=1)
        input_frames.columnconfigure(1, weight=1)

        # vektorok osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]
        # skalarok osszegyujtese
        scalars=[vector1_scalar,vector2_scalar]

        # ertekek generalasa ha szukseges
        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)
            vector1_scalar.insert(0, str(random.randint(0, 10)))
            vector2_scalar.insert(0, str(random.randint(0, 10)))

        # diagram megjelenitese
        ttk.Button(tab, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2,scalars)).grid(row=4, column=0,columnspan=2)



    def show_diagram(self, tab, vector1,vector2, scalars):
        """
        A program kirajzolja a vektorokat a diagramra, es a diagrammot kirajzolja az ablakra
        :param tab:         frame amiben dolgozunk
        :param vector1:     u vektor
        :param vector2:     v vektor
        :param scalars:     scalarok listaja
        """

        #elozo diagram bezarasa
        plt.close()

        # vektorok ertekenek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []

        vector_scalars=[]

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        self.error_frame = tk.Frame(tab)

        self.diagram_frame = ttk.Frame(tab, borderwidth=1, relief='solid')

        # vektorok ertekenek ellenorzese es kinyerese
        try:
            for coord_entry in vector1:
                cooridnate = float(coord_entry.get())

                vector1_matrix.append(cooridnate)

            for coord_entry in vector2:
                cooridnate = float(coord_entry.get())

                vector2_matrix.append(cooridnate)

            for scalar in scalars:
                vector_scalars.append(float(scalar.get()))

        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen vektor megjelenites: {e}\033[0m")
            self.error_frame.grid(row=5, column=0)
            return False

        # vektorok NumPy kompatibilisse valtoztatasa
        vector1_mx = np.array(vector1_matrix)
        vector2_mx = np.array(vector2_matrix)

        self.diagram_frame.grid(row=6, column=0,columnspan=2)

        # linearis kombinacio kiszamolasa
        self.solver_controller.solver_handler('vector_linear_combination',self.diagram_frame, vector1_mx,vector2_mx,vector_scalars)

    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))
