import random
import tkinter as tk
from tkinter import ttk

class Vectorlenght(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller

        self.current_tab = None
        self.create_screen()
        self.solver_controller = solver_handler

    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Vektor normája", style='Title.TLabel').grid(row=0, column=0)
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
        math_rules = ttk.LabelFrame(tab, text='Vektor normája')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egy vektor hosszát normának nevezzük.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A normát a Pitagorasz tétellel számoljuk ki:  ||v||=(v1**2 + v2**2 + v3**2)**(1/2)').grid(
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

        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0,columnspan=2)
        ttk.Button(main_grid, text="Vektor létrehozása", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0,columnspan=2)

        tab.columnconfigure(0, weight=1)

        main_grid.grid(row=0, column=0)


    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')

        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Vektor létrehozása", width=25,
                   command=lambda: self.vector_create(tab)).grid(row=8, column=0)

        main_grid.grid(row=0, column=0)

        tab.columnconfigure(0, weight=1)


    def vector_create(self, tab):
        """
        A generalas gomb lenyomasa utan a program legeneralja a problemanak megfelelo beviteli mezoket
        :param tab:     frame amivel dolgozunk
        """

        # a vektor beviteli mezoi
        block1 = ttk.LabelFrame(tab, text="Vektor koordinátái")
        ttk.Label(block1, text="x = ").grid(row=2, column=0)
        vector_x = ttk.Entry(block1)
        vector_x.grid(row=2, column=1)
        ttk.Label(block1, text="y = ").grid(row=3, column=0)
        vector_y = ttk.Entry(block1)
        vector_y.grid(row=3, column=1)
        ttk.Label(block1, text="z = ").grid(row=4, column=0)
        vector_z = ttk.Entry(block1)
        vector_z.grid(row=4, column=1)
        block1.grid(row=2, column=0, columnspan=2)

        # vektor osszerakasa
        vector = [vector_x, vector_y, vector_z]

        # ha generalunk bele ertekeket akkor toltse fel
        if tab == self.pelda_adatok:
            self.generate_data(vector)

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()
        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        # diagram megjelenitese
        ttk.Button(tab, text="Megjelenítés", width=25,
                   command=lambda: self.show_diagram(tab, vector)).grid(row=5, column=0)

    def show_diagram(self, tab, vector):
        """
        A program kirajzolja a vektort a diagramra, es a diagrammot kirajzolja az ablakra
        :param tab:         frame amiben dolgozunk
        :param vector:     vektor 1
        """

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        self.error_frame = ttk.Frame(tab)
        self.diagram_frame = ttk.Frame(tab, borderwidth=1, relief='solid')

        # vektor ertekeinek kinyeresenek felkeszulese
        vector_matrix = []

        # vektor ertekeinek ellenorzese es kinyerese
        try:
            for coord_entry in vector:
                cooridnate = float(coord_entry.get())

                vector_matrix.append(cooridnate)

        except Exception as e:

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen vektor megjelenites: {e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False


        self.diagram_frame.grid(row=6, column=0)
        self.solver_controller.solver_handler('vector_norm',self.diagram_frame, vector_matrix)


    def generate_data(self,vector):
        """
        A program feltolti a vektorokat random ertekekkel
        :param vector: vector
        """
        for i in range(len(vector)):
            vector[i].insert(0, random.randint(0, 10))
