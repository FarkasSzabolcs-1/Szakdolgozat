import random
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Trianglesolution(tk.Frame):
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
        ttk.Label(title_frame, text="Háromszög megoldás", style='Title.TLabel').grid(row=0, column=0)
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
        math_rules = ttk.LabelFrame(tab, text='Háromszög megoldás')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Bármely 3 vektor alkalmazásával egy tetszőleges háromszöget rajzolhatunk a térben.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Ezeknek a vektoroknak a segítségével a háromszög tulajdonságait képesek vagyunk meghatározni.').grid(
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
        tab.columnconfigure(0,weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)

        main_grid.grid(row=0, column=0, columnspan=3)

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
        #elozo diagram bezarasa
        plt.close()

        # elozo framek resetelese
        if self.input_frames is not None:
            self.input_frames.destroy()

        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()


        # beviteli mezok elokeszitese
        self.input_frames = ttk.Frame(tab)

        block1 = ttk.LabelFrame(self.input_frames, text="Vektor 1 koordinátái")
        block2 = ttk.LabelFrame(self.input_frames, text="Vektor 2 koordinátái")
        block3 = ttk.LabelFrame(self.input_frames, text="Vektor 3 koordinátái")

        self.input_frames.grid(row=1, column=0)

        #vektor 1
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

        # vektor 2
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

        # vektor 3
        ttk.Label(block3, text="x = ").grid(row=2, column=0)
        vector3_x = ttk.Entry(block3)
        vector3_x.grid(row=2, column=1)
        ttk.Label(block3, text="y = ").grid(row=3, column=0)
        vector3_y = ttk.Entry(block3)
        vector3_y.grid(row=3, column=1)
        ttk.Label(block3, text="z = ").grid(row=4, column=0)
        vector3_z = ttk.Entry(block3)
        vector3_z.grid(row=4, column=1)

        block3.grid(row=2, column=2)

        self.input_frames.columnconfigure(0,weight=1)
        self.input_frames.columnconfigure(1, weight=1)

        # vektorok osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]
        vector3 = [vector3_x, vector3_y, vector3_z]

        # ertekkel feltoltes ha random ertekekkel generalunk
        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)
            self.generate_data(vector3)

        # diagram megjelenitese
        ttk.Button(self.input_frames, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2,vector3)).grid(row=3, column=0,columnspan=3)



    def show_diagram(self, tab, vector1, vector2,vector3):
        """
        A program kirajzolja a vektorokat a diagramra, es a diagrammot kirajzolja az ablakra
        :param tab:         frame amiben dolgozunk
        :param vector1:     vektor 1
        :param vector2:     vektor 2
        :param vector3:     vektor 2
        """
        #elozo diagram bezarasa
        plt.close()

        # vektorok ertekenek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []
        vector3_matrix = []

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

            for coord_entry in vector3:
                cooridnate = float(coord_entry.get())

                vector3_matrix.append(cooridnate)




        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen háromszög megoldás számolás: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # a 3 terbeli pont NumPy kompatibilissa tevese szamolashoz es korlat szamolashoz
        a_coord = np.array(vector1_matrix)
        b_coord = np.array(vector2_matrix)
        c_coord = np.array(vector3_matrix)

        #diagram meretenek beallitasa
        fig = plt.figure(figsize=(5,5))
        #diagram tipusanak beallitasa
        ax = fig.add_subplot(111, projection="3d")

        # diagram korlatainak kiszamitasa
        lim=max(a_coord.max(),b_coord.max(),c_coord.max())
        min_lim = min(a_coord.min(), b_coord.min(), c_coord.min())

        if min_lim>0:
            min_lim=0
        if (lim <0):
            lim=0

        ax.set_xlim(min_lim, lim)
        ax.set_ylim(min_lim, lim)
        ax.set_zlim(min_lim, lim)

        # diagramot ablakra helyezhetove tesszuk
        canvas = FigureCanvasTkAgg(fig, master=self.diagram_frame)

        # dimenziok elnevezese
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Háromszög megoldás')

        # 3 vektor kiszamitasa
        ab_vector=b_coord-a_coord
        bc_vector=c_coord-b_coord
        ca_vector=a_coord-c_coord

        # A B C pontok kirajzolasa
        ax.scatter(*a_coord, color='black', s=10)
        ax.scatter(*b_coord, color='black', s=10)
        ax.scatter(*c_coord, color='black', s=10)

        # neveket adni nekik diagrammon
        ax.text(*a_coord + 0.15, 'A', fontsize=10, color='black')
        ax.text(*b_coord + 0.15, 'B', fontsize=10, color='black')
        ax.text(*c_coord + 0.15, 'C', fontsize=10, color='black')

        # vektorok/ haromszog oldalai megrajzolasa
        ax.quiver(*a_coord, *ab_vector, color='red', linewidth=3, arrow_length_ratio=0.15)
        ax.quiver(*b_coord, *bc_vector, color='green', linewidth=3, arrow_length_ratio=0.15)
        ax.quiver(*c_coord, *ca_vector, color='blue', linewidth=3, arrow_length_ratio=0.15)

        # diagram megjelenitese
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)
        self.diagram_frame.grid(row=4, column=0,columnspan=2)

        # megoldas gomb amivel haromszog tulajdonsagait kiszamolhatjuk
        ttk.Button(self.diagram_frame, text="Kiszámítás", width=25,
                   command=lambda: self.solver_controller.solver_handler('triangle_solution',self.diagram_frame,ax,ab_vector,bc_vector,ca_vector,a_coord,b_coord,c_coord)).grid(row=6, column=0)

    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))
