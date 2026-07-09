import random
import tkinter as tk
from tkinter import ttk


class Linearequations(tk.Frame):
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
        ttk.Label(title_frame, text="Lineáris egyenletrendszerek",style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza",style='Back.TButton', command=lambda: self.controller.show_screen("Vectorspacemenu")).grid(row=1, column=0,
                                                                                                        sticky="w")
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
        self.diagram_frame= None
        self.error_frame = None

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
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.\n'
                       f'-A program a Cramer-szabály segítségével oldja meg az egyenleteket.\n'
                       f'-Az ismeretlenek száma megegyezik az egyenletek számával.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Lineáris egyenletrendszerek')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Az általános lineáris egyenletrendszerek megoldására az egyik legtermészetesebben adódó, egyszerű és gyakorlati szempontból is jól alkalmazható eljárás a Gauss-féle kiküszöbölés.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Speciális egyenletrendszerekre vonatkozik a Cramer-szabály, amely a determinánsok segítségével ad képletet a megoldásra.').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A folyamat során az úgynevezett elemi ekvivalens átalakításokat alkalmazzuk a sorokon:').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'E1. Valamelyik egyenletet egy nullától különböző skalárral végigszorozzuk').grid(
            row=4, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'E2. Valamelyik egyenlethez egy másik egyenlet skalárszorzatát hozzáadjuk').grid(
            row=5, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'E3. Két egyenletet felcserélünk').grid(
            row=6, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'E4. A tiszta nulla sorokat elhagyjuk').grid(
            row=7, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Abban az esetben, ha az egyenletrendszerek száma megegyezik az ismeretlenek számával, valamint az A együtthatómátrix determinánsa nem nulla, akkor a megoldást Cramer-szabály segítségével is kiszámíthatjuk.').grid(
            row=8, column=0, sticky='we')

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
        block1 = ttk.LabelFrame(main_grid, text="Egyenletrendszer felépítése")
        ttk.Label(block1,text='(egyenletek száma = ismeretlenek száma)').grid(row=0,column=0,columnspan=2)
        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="Egyenletek száma:").grid(row=3, column=0)
        equations_number = ttk.Entry(block1)
        equations_number.grid(row=3, column=1)
        block1.grid(row=2, column=0, columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab,equations_number)).grid(row=8, column=0, columnspan=2)

    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Egyenletrendszer felépítése")
        ttk.Label(block1,text='(egyenletek száma = ismeretlenek száma)').grid(row=0,column=0,columnspan=2)
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="Egyenletek száma:").grid(row=3, column=0)
        equations_number = ttk.Entry(block1)
        equations_number.grid(row=3, column=1)
        block1.grid(row=2, column=0, columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, equations_number)).grid(row=8, column=0,
                                                                                               columnspan=2)


    def build_matrix(self, tab,equations_number_entry):
        """
        A program generalas gomb lenyomasa utan letrehoozza az egyutthato matrixot es az eredmeny vektor
        A program a tabtol (sajat- vagy pelda adatok) fuggoen feltolti ezutan ertekkel, vagy uresen hagyja.
        Az egyenletek szama egyenlo az ismeretlenek szamaval, ezert az egyutthato matrix negyzetmatrix

        :param tab:                     frame amiben dolgozunk
        :param equations_number_entry:  egyenletek szama
        :return:
        """

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = tk.Frame(tab)

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        # generalas elotti parameter ellenorzes
        try:
            equations_size=int(equations_number_entry.get())
        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen egyenlet generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        if equations_size <=0:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg 0-nál nagyobb számot",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # elozo secondary frame reset
        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        self.secondary_frame = tk.Frame(tab)

        # matrixok kiiratasanak felkeszulese
        self.block3 = tk.LabelFrame(self.secondary_frame, text="Együttható mátrix (A)")
        self.block4 = tk.LabelFrame(self.secondary_frame, text="Eredmény vektor (b)")

        self.matrix1_entries = [[None] * equations_size for i in range(equations_size)]
        self.matrix2_entries = [[None] * equations_size]


        self.block4.columnconfigure(0,weight=1)
        # egyutthato matrix
        for i in range(equations_size):
            for j in range(equations_size):
                entry = ttk.Entry(self.block3, width=5)
                self.matrix1_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

        # eredmeny vektor
        for i in range(equations_size):

            entry = ttk.Entry(self.block4, width=5)
            self.matrix2_entries[0][i] = entry
            entry.grid(row=8 + i, column=0,columnspan=equations_size)



        # ha sajat adat tab akkor ne toltse fel
        if (self.sajat_adatok == tab):
            pass
        else:
            self.generate_data(self.matrix1_entries)
            self.generate_data(self.matrix2_entries)

        # kiiras ablakra
        self.block3.grid(row=4, column=0 , padx=(0, 15))
        self.block4.grid(row=4, column=1)

        # diagram kirajzolasahoz frame letrehozasa
        self.diagram_frame = tk.Frame(tab)

        # megoldas gomb
        ttk.Button(self.secondary_frame, text="Kiszámítás",
                   command=lambda: self.solver_controller.solver_handler('linear_equations',self.diagram_frame, self.matrix1_entries,self.matrix2_entries)).grid(
            row=5, column=0, columnspan=2)
        self.secondary_frame.grid(row=2, column=0, columnspan=2)

    def generate_data(self, entry_list):
        """
        A program a kapott entry listat feltolti random generalt ertekekkel
        :param entry_list:  beviteli mezok
        """
        for i in range(len(entry_list)):
            for j in range(len(entry_list[i])):
                entry_list[i][j].insert(0, random.randint(0, 50))