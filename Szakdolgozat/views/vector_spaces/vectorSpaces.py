import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Vectorspaces(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.create_screen()
        self.solver_controller = solver_handler

    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Vektorterek", style='Title.TLabel').grid(row=0, column=0)
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
        math_rules = ttk.LabelFrame(tab, text='Vektorterek')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Legyen K egy kommutatív test a V != 0, halmazon értelmezünk egy belső (összeadás +) és egy külső (skalárral való szorzás) műveletet.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A V halmazt K feletti vektortérnek nevezzük, ha teljesülnek az alábbi összeadásra és skalárral való szorzásra vonatkozó axiómák:').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'1. Bármely két u és v vektor összege szintén a V halmazban van, tehát létezik zártság az összeadásra.').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'2. kommutatívitás: u + v = v + u, minden u, v eleme V-re.').grid(
            row=4, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'3. Asszociatívitás: (u + v) + w = u + (v + w)').grid(
            row=5, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'4. Létezik nullvektor: olyna 0 vektor V-ben, amelyre u + 0 = u teljesül minden u-ra.').grid(
            row=6, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'5. Létezik ellentett vektor: minden V-beli u vektorhoz létezik olyan -u vektor V-ben, amelyre u + (-u) = 0.').grid(
            row=7, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'6. Bármely u vektor c skalárral vett szorzata szintén a V halmazban van.').grid(
            row=8, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'7. Disztributívitás vektorösszegre: c(u+v) = cu + cv').grid(
            row=9, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'8. Disztributívitás skalárösszegre: (c + d)u = cu + du').grid(
            row=10, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'9. Skalárszorzat asszociatívitása: c(du) = (cd)u').grid(
            row=11, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'10. Egységelem tulajdonsága: 1u = u , ahol 1 a skalártest egységeleme.').grid(
            row=12, column=0, sticky='we')


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


        # vektorok es skalar beviteli mezok elokeszitese
        self.input_frames = ttk.Frame(tab)

        block1 = ttk.LabelFrame(self.input_frames, text="u Vektor koordinátái")
        block2 = ttk.LabelFrame(self.input_frames, text="v Vektor koordinátái")
        block3 = ttk.LabelFrame(self.input_frames, text="Skalár")



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

        # skalar
        ttk.Label(block3, text="c = ").grid(row=2, column=0)
        scalar = ttk.Entry(block3)
        scalar.grid(row=2,column=1)

        block3.grid(row=2, column=2)

        self.input_frames.columnconfigure(0,weight=1)
        self.input_frames.columnconfigure(1, weight=1)


        # vektorok osszerakasa
        vector1 = [vector1_x, vector1_y, vector1_z]
        vector2 = [vector2_x, vector2_y, vector2_z]


        if tab == self.pelda_adatok:
            self.generate_data(vector1)
            self.generate_data(vector2)
            scalar.insert(0, random.randint(0, 10))

        # diagram megjelenitese
        ttk.Button(self.input_frames, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector1,vector2,scalar)).grid(row=3, column=0,columnspan=3)

    def show_diagram(self,tab,vector1,vector2,scalar):
        """
        A program megjeleniti a diagrammot es a benne kirajzolt vektorokat
        :param tab:     frame amiben dolgozunk
        :param vector1: u vektor
        :param vector2: v vektor
        :param scalar:  skalar
        """

        #diagram torlese
        plt.close()

        # ertekek kinyeresenek felkeszulese
        vector1_matrix = []
        vector2_matrix = []

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        self.error_frame = tk.Frame(tab)

        self.diagram_frame = ttk.Frame(tab, borderwidth=1, relief='solid')

        # ertekek ellenorzese es kinyerese a mezokbol
        try:
            for coord_entry in vector1:
                cooridnate = float(coord_entry.get())

                vector1_matrix.append(cooridnate)

            for coord_entry in vector2:
                cooridnate = float(coord_entry.get())

                vector2_matrix.append(cooridnate)

            scalar_value=float(scalar.get())

        except Exception as e:

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen vektor generalas: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False



        self.diagram_frame.grid(row=4, column=0, columnspan=2)

        self.solver_controller.solver_handler('vector_spaces',self.diagram_frame,vector1_matrix,vector2_matrix,scalar_value)

    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))