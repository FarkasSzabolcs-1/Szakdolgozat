import random
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Bases(tk.Frame):
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
        ttk.Label(title_frame, text="Bázis", style='Title.TLabel').grid(row=0, column=0)
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
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Bázisok')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A bázis az egy lineárisan független generátorrendszer.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egy V vektortérben egy vektorrendszer akkor és csakis akkor alkot bázist, ha a tér tetszőleges v eleme egyértelműen felírható a bázisvektorok lineáris kombinációjaként.').grid(
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

        #elozo diagram torlese
        plt.close()

        # elozo framek resetelese
        if self.input_frames is not None:
            self.input_frames.destroy()

        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()


        # bazis es vektor mezoinek felkeszitese
        self.input_frames = ttk.Frame(tab)

        block1 = ttk.LabelFrame(self.input_frames,text='Bázis')
        block4 = ttk.LabelFrame(self.input_frames, text="Egy pont a térben:")

        self.input_frames.grid(row=1, column=0)

        # bazis
        vector1_x = ttk.Entry(block1)
        vector1_x.grid(row=2, column=0)
        vector1_y = ttk.Entry(block1)
        vector1_y.grid(row=3, column=0)
        vector1_z = ttk.Entry(block1)
        vector1_z.grid(row=4, column=0)

        vector2_x = ttk.Entry(block1)
        vector2_x.grid(row=2, column=1)
        vector2_y = ttk.Entry(block1)
        vector2_y.grid(row=3, column=1)
        vector2_z = ttk.Entry(block1)
        vector2_z.grid(row=4, column=1)

        vector3_x = ttk.Entry(block1)
        vector3_x.grid(row=2, column=2)
        vector3_y = ttk.Entry(block1)
        vector3_y.grid(row=3, column=2)
        vector3_z = ttk.Entry(block1)
        vector3_z.grid(row=4, column=2)

        block1.grid(row=2, column=0, columnspan=4)


        # skalarok
        scalar_a = ttk.Entry(block4)
        scalar_a.grid(row=2,column=0)

        scalar_b = ttk.Entry(block4)
        scalar_b.grid(row=2, column=1)

        scalar_c = ttk.Entry(block4)
        scalar_c.grid(row=2, column=2)

        block4.grid(row=3, column=0,columnspan=3)

        # kozepre illesztes
        self.input_frames.columnconfigure(0,weight=1)
        self.input_frames.columnconfigure(1, weight=1)

        # vektorok osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]
        vector3 = [vector3_x, vector3_y, vector3_z]

        # ertekek generelese ha szukseges
        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)
            self.generate_data(vector3)
            scalar_a.insert(0, random.randint(0, 10))
            scalar_b.insert(0, random.randint(0, 10))
            scalar_c.insert(0, random.randint(0, 10))

        # diagram megjelenitese
        ttk.Button(self.input_frames, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2,vector3,scalar_a,scalar_b,scalar_c)).grid(row=4, column=0,columnspan=3)

    def show_diagram(self,tab,vector1,vector2,vector3,scalar_a_entry,scalar_b_entry,scalar_c_entry):
        """
        A program kirajzolja a vektorokat a diagramra, es a diagrammot kirajzolja az ablakra

        :param tab:             frame amin belul dolgozunk
        :param vector1:         vektor 1
        :param vector2:         vektor 2
        :param vector3:         vektor 3
        :param scalar_a_entry:  a skalar
        :param scalar_b_entry:  b skalar
        :param scalar_c_entry:  c skalar
        """

        #diagram torlese
        plt.close()

        # ertekek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []
        vector3_matrix = []
        big_matrix=[]

        #elozo ertekek torlese
        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        self.error_frame = tk.Frame(tab)

        self.diagram_frame = ttk.Frame(tab, borderwidth=1, relief='solid')

        # ertekek ellenorzese es kinyerese
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

            big_matrix.append(vector1_matrix)
            big_matrix.append(vector2_matrix)
            big_matrix.append(vector3_matrix)

            big_mx = np.array(big_matrix)

            # bazis determinansa es rangjanak ellenorzese
            if np.linalg.det(big_mx) !=0 and np.linalg.matrix_rank(big_mx)==3:
                pass
            else:
                if self.secondary_frame is not None:
                    self.secondary_frame.destroy()

                ttk.Label(self.error_frame, text="Determináns nem 0, és a Rank nem 3. Tehát nincs bázis", style='Error.TLabel').grid(row=10,
                                                                                                                 column=0)
                print(f"    \033[91m-> Sikertelen bazis generalas:\033[0m")
                self.error_frame.grid(row=4, column=0)
                return False

            # skalarok ertekeinek kinyerese
            scalar_a=float(scalar_a_entry.get())
            scalar_b=float(scalar_b_entry.get())
            scalar_c = float(scalar_c_entry.get())



        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen bazis generalas: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False



        self.diagram_frame.grid(row=4, column=0, columnspan=2)

        # bazis szamolasok
        self.solver_controller.solver_handler('bases',self.diagram_frame,vector1_matrix,vector2_matrix,vector3_matrix,scalar_a,scalar_b,scalar_c)

    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))