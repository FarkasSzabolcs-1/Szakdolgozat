import random
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Vectorsubspaces(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.create_screen()
        self.vector_space_solver=solver_handler

    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Alterek", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza", style='Back.TButton',
                   command=lambda: self.controller.show_screen("Vectorspacemenu")).grid(row=1, column=0, sticky="w")
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
                  text=f'-Szöveget tartalmazó m11ezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Alterek')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egy vektortérnek egy nem üres U halmaza V részhalmazát akkor nevezzük a V vektortér alterének, ha U maga is vektortér ugyanazon a K test felett a V-ből örökölt összeadás és a skalárral való szorzás műveleteire nézve.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egy részhalmazról úgy állítható be a legkönnyebben, hogy altér, ha ellenőrizzük a műveletekre való zártságát.').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Minden vektortérnek léteznek úgynevezett triviális alterei, ami azt jelenti, hogy maga a teljes V vektortér, valamint kizárólag a nullvektorokból álló halmaz mindig alteret alkot.').grid(
            row=3, column=0, sticky='we')

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
        tab.columnconfigure(0,weight=1)

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

        # elozo framek resetelese
        if self.input_frames is not None:
            self.input_frames.destroy()

        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        self.input_frames=ttk.Frame(tab)


        # vektorok mezoinek elokeszitese
        block1 = ttk.LabelFrame(self.input_frames, text="u Vektor koordinátái")
        block2 = ttk.LabelFrame(self.input_frames, text="v Vektor koordinátái")


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

        # v vektorok
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


        # kozepre illesztes
        self.input_frames.columnconfigure(0,weight=1)
        self.input_frames.columnconfigure(1, weight=1)

        # vektorok osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]

        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)



        ttk.Button(self.input_frames, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2)).grid(row=3, column=0,columnspan=3)

    def show_diagram(self,tab,vector_u_entry,vector_v_entry):
        """
        A 3 vektor segitsegevel letrehozunk 2 sikot, az elso atmegy az origon,
        a masodik sik pedig ugyanolyan sik mint az elso, viszont a Z dimenzioban eltoljuk 5-el.
        Ezutan kirajzoljuk oket a diagramra
        :param tab:             frame amiben dolgozunk
        :param vector_u_entry:  u vektor mezok
        :param vector_v_entry:  v vektor mezok
        :return:
        """

        # elozo diagram torlese
        plt.close()

        # vektorok ertekeinek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []

        # elozo framek resetelese
        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = ttk.Frame(tab)

        self.diagram_frame = ttk.Frame(tab, borderwidth=1, relief='solid')

        # ertekek ellenorzese es kinyerese
        try:
            for coord_entry in vector_u_entry:
                cooridnate = float(coord_entry.get())

                vector1_matrix.append(cooridnate)

            for coord_entry in vector_v_entry:
                cooridnate = float(coord_entry.get())

                vector2_matrix.append(cooridnate)

        except Exception as e:

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen vektor altér generalas: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # vektorok NumPy kompatibilissa tevese
        vector_v = np.array(vector1_matrix)
        vector_u = np.array(vector2_matrix)

        # diagram letrehozasa, meret, tipus es frame megadasa
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection="3d")
        canvas = FigureCanvasTkAgg(fig, master=self.diagram_frame)

        # dimenziok elnevezese
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Alterek')

        # két sík előkészítése
        s = np.linspace(-1, 1, 10)
        t = np.linspace(-1, 1, 10)

        # síkká alakítás
        S, T = np.meshgrid(s, t)

        # az első sík koordinátáinak kiszámítása lineáris kombináció segítségével
        X = vector_u[0] * S + vector_v[0] * T
        Y = vector_u[1] * S + vector_v[1] * T
        Z = vector_u[2] * S + vector_v[2] * T

        # első sík kirajzolása (metszi az origót)
        ax.plot_surface(X, Y, Z, alpha=0.9, cmap=plt.cm.coolwarm)

        # második sík eltolása 5-el, többé már nem altér
        Z2 =(vector_u[2] * S + vector_v[2] * T)+5

        # második sík kirajzolása a diagramra
        ax.plot_surface(X, Y, Z2, alpha=0.9, cmap=plt.cm.jet)

        # diagram korlatainek kiszamitasa es beallitasa
        lim = max(X.max(), Y.max(),Z.max())
        min_lim = min(X.min(), Y.min(),Z.min())

        if (lim) < 0:
            lim = 0
        if min_lim > 0:
            min_lim = 0

        ax.set_xlim(min_lim, lim)
        ax.set_ylim(min_lim, lim)
        ax.set_zlim(min_lim, lim)

        # origo kirajzolasa
        ax.scatter(0, 0, 0, s=20, color="black",label='origó')
        # magyarazat kiirasa
        ax.legend()
        # diagram kirajzolasa
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

        self.diagram_frame.grid(row=4, column=0, columnspan=2)


    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))