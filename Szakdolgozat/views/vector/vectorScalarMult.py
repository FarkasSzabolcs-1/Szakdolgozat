import random
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Vectorscalarmult(tk.Frame):
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
        ttk.Label(title_frame, text="Két vektor skaláris szorzata", style='Title.TLabel').grid(row=0, column=0)
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
        self.input_frames=None

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
        math_rules = ttk.LabelFrame(tab, text='Két vektor skaláris szorzata')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A két vektor skaláris szorzata alatt azt a műveletet értjük, amikor a vektor elemeit összeszorozzuk egymással, majd pedig ezeket összeadjuk.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A két vektor akkor és csakis akkor merőleges egymásra, ha a két vektor skaláris szorzata 0.').grid(
            row=1, column=0, sticky='we')

        general_rules.grid(row=0, column=0, sticky='nsew')
        general_rules.columnconfigure(0, weight=1)
        math_rules.grid(row=1, column=0, sticky='nsew')
        math_rules.columnconfigure(0, weight=1)



    def build_example_datas(self):
        """
        generalas gomb, megnyomasa utan a mezoket elore generalt ertekekkel feltolti
        """
        tab = self.pelda_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)

        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Vektorok létrehozása", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0)

        tab.columnconfigure(0, weight=1)

    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)

        main_grid.grid(row=0, column=0,columnspan=2)

        ttk.Button(main_grid, text="Vektorok létrehozása", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0)

        tab.columnconfigure(0, weight=1)

    def vector_create(self,tab):
        """
        A generalas gomb lenyomasa utan a program legeneralja a problemanak megfelelo beviteli mezoket
        :param tab:     frame amivel dolgozunk
        """

        # elozo diagram torlese
        plt.close()


        #elozo framek torlese
        if self.input_frames is not None:
            self.input_frames.destroy()

        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()


        # inputmezok elokeszitese
        self.input_frames = ttk.Frame(tab)


        block1 = ttk.LabelFrame(self.input_frames, text="u vektor koordinátái")
        block2 = ttk.LabelFrame(self.input_frames, text="v vektor koordinátái")


        self.input_frames.grid(row=1, column=0)

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

        self.input_frames.columnconfigure(0,weight=1)
        self.input_frames.columnconfigure(1, weight=1)







        # a ket vektor osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]

        # vektorokat ertekekkel feltolteni ha szukseges
        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)

        # diagram megjelenitese a vektorokkal
        ttk.Button(self.input_frames, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2)).grid(row=3, column=0,columnspan=2)



    def show_diagram(self, tab, vector1, vector2):
        """
        A program kirajzolja a vektorokat a diagramra, es a diagrammot kirajzolja az ablakra
        :param tab:         frame amiben dolgozunk
        :param vector1:     vektor 1
        :param vector2:     vektor 2
        """

        #elozo diagram bezarasa
        plt.close()

        # vektorok ertekenek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []



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

        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen vektor megjelenites: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # vektorok NumPy kompatibilisse valtoztatasa
        vector1_mx = np.array(vector1_matrix)
        vector2_mx = np.array(vector2_matrix)

        # origo
        vector_or = np.zeros(3)

        # diagram meretenek beallitasa
        fig = plt.figure(figsize=(4,4))

        # diagram tipusanak beallitasa
        ax = fig.add_subplot(111, projection="3d")

        # diagram korlatainak kiszamitasa es beallitasa
        lim = max(vector1_mx.max(),vector2_mx.max())

        min_lim= min(vector1_mx.min(),vector2_mx.min())

        if (min_lim>0):
            min_lim=0
        if (lim <0):
            lim=0

        ax.set_xlim(min_lim, lim)
        ax.set_ylim(min_lim, lim)
        ax.set_zlim(min_lim, lim)

        # canvas letrehozasa amit az ablakra helyezunk
        canvas = FigureCanvasTkAgg(fig, master=self.diagram_frame)

        # diagram dimenzioinak elnevezese
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('2 vektor skaláris szorzata')


        # u vektor
        ax.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector1_mx[0], vector1_mx[1], vector1_mx[2],
            color='red', linewidth=3,
            arrow_length_ratio=0.15,label='u vektor'
        )
        # v vektor
        ax.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector2_mx[0], vector2_mx[1], vector2_mx[2],
            color='blue', linewidth=3,
            arrow_length_ratio=0.15,label='v vektor'
        )
        # magyarazat kiirasa
        ax.legend()
        # diagram kirajzolasa
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)



        self.diagram_frame.grid(row=4, column=0,columnspan=2)
        # muvelet megoldasa gomb
        ttk.Button(self.diagram_frame, text="Kiszámítás", width=25,
                   command=lambda: self.solver_controller.solver_handler('vector_scalar_mult',self.diagram_frame, vector1_mx,vector2_mx)).grid(row=6, column=0)

    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 50))
