import random
import tkinter as tk
from tkinter import ttk


class Matrixmult(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.solver_controller = solver_handler
        self.create_screen()

    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame=tk.Frame(self)
        ttk.Label(title_frame, text="Mátrixok szorzása",style='Title.TLabel').grid(row=0,column=0)
        ttk.Button(self, text="Vissza",style='Back.TButton', command=lambda: self.controller.show_screen("Matrixmenu")).grid(row=1,column=0,sticky="w")
        title_frame.grid(row=0,column=0)

        # tabok elokeszitesse
        self.tabcontrol = ttk.Notebook(self)
        self.tabcontrol.grid(row=2, column=0,sticky='we')

        # a 3 tab
        self.pelda_adatok = ttk.Frame(self.tabcontrol)
        self.sajat_adatok = ttk.Frame(self.tabcontrol)
        self.tulajdonsagok = ttk.Frame(self.tabcontrol)

        # nevek adasa
        self.tabcontrol.add(self.pelda_adatok, text="Példa adatok")
        self.tabcontrol.add(self.sajat_adatok, text="Saját adatok")
        self.tabcontrol.add(self.tulajdonsagok,text="Tulajdonságok")

        # 3 tab fuggvenyenek a meghivasa
        self.build_example_datas()
        self.build_empty_datas()
        self.show_rules()

        #framek alaphelyzetbe allitasa
        self.secondary_frame = None
        self.block3=None
        self.block4=None
        self.result_frame=None
        self.error_frame=None

        #kozepre igazitas
        self.columnconfigure(0, weight=1)

    def show_rules(self):
        """
        Betolti az altalanos es matematikai tulajdonsagokat a problemahoz kapcsolodoan
        """
        tab = self.tulajdonsagok

        tab.columnconfigure(0, weight=1)

        general_rules = ttk.LabelFrame(tab, text='Általános ismertetők')
        ttk.Label(general_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Példa adatok tab: Random generált értékek.').grid(row=0, column=0, sticky='we')
        ttk.Label(general_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Saját adatok tab: Felhasználó által megadott értékek.').grid(row=1, column=0, sticky='we')
        ttk.Label(general_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Üres mezőket a program nem fogad el.').grid(row=2, column=0, sticky='we')
        ttk.Label(general_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')

        math_rules = ttk.LabelFrame(tab, text='Mátrixok szorzása')
        ttk.Label(math_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Két mátrix akkor szorozható össze, ha a bal oldali mátrix oszlopainak a száma megegyezik a jobb oldali mátrix sorainak a számával.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-A szorzásuk nem kommunatív. A*B!=B*A').grid(row=1,column=0,sticky='we')
        ttk.Label(math_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-A szorzásuk asszociatív. (A*B)*C=A*(B*C)').grid(row=2, column=0, sticky='we')
        ttk.Label(math_rules, style='TLabel', justify='left', wraplength=800,
                  text=f'-Egységmátrixxal szorozva a szorzás semleges. E*A=A vagy A*E=A').grid(row=3, column=0, sticky='we')

        general_rules.grid(row=0, column=0, sticky='nsew')
        general_rules.columnconfigure(0, weight=1)

        math_rules.grid(row=1, column=0, sticky='nsew')
        math_rules.columnconfigure(0, weight=1)


    def build_example_datas(self):
        """
        parameter beviteli panel betoltese, generalas utan elore generalt ertekekkel
        """
        tab = self.pelda_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Mátrix 1 mérete")
        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="sor:").grid(row=1, column=0)
        matrix1_szam1 = ttk.Entry(block1)
        matrix1_szam1.grid(row=1, column=1)
        ttk.Label(block1, text="oszlop:").grid(row=2, column=0)
        matrix1_szam2 = ttk.Entry(block1)
        matrix1_szam2.grid(row=2, column=1)
        block1.grid(row=2, column=0)

        block2 = ttk.LabelFrame(main_grid, text="Mátrix 2 mérete")
        ttk.Label(block2, text="sor:").grid(row=5, column=0)
        matrix2_szam1 = ttk.Entry(block2)
        matrix2_szam1.grid(row=5, column=1)
        ttk.Label(block2, text="oszlop:").grid(row=6, column=0)
        matrix2_szam2 = ttk.Entry(block2)
        matrix2_szam2.grid(row=6, column=1)
        block2.grid(row=2, column=1)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix1_szam1, matrix1_szam2, matrix2_szam1,
                                                     matrix2_szam2)).grid(row=8, column=0, columnspan=2)

    def build_empty_datas(self):
        """
        parameter beviteli panel betoltese, generalas utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Mátrix 1 mérete")
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="sor:").grid(row=1, column=0)
        matrix1_szam1 = ttk.Entry(block1)
        matrix1_szam1.grid(row=1, column=1)
        ttk.Label(block1, text="oszlop:").grid(row=2, column=0)
        matrix1_szam2 = ttk.Entry(block1)
        matrix1_szam2.grid(row=2, column=1)
        block1.grid(row=2, column=0)

        block2 = ttk.LabelFrame(main_grid, text="Mátrix 2 mérete")
        ttk.Label(block2, text="sor:").grid(row=0, column=0)
        matrix2_szam1 = ttk.Entry(block2)
        matrix2_szam1.grid(row=0, column=1)
        ttk.Label(block2, text="oszlop:").grid(row=1, column=0)
        matrix2_szam2 = ttk.Entry(block2)
        matrix2_szam2.grid(row=1, column=1)
        block2.grid(row=2, column=1)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix1_szam1, matrix1_szam2, matrix2_szam1,
                                                     matrix2_szam2)).grid(row=8, column=0, columnspan=2)

    def build_matrix(self, tab, matrix1_sor, matrix1_oszlop, matrix2_sor, matrix2_oszlop):
        """
        A program legeneralja a parameterek szerint a mezoket es felkesziti a veluk torteno muveletre

        :param tab:             frame amiben dolgozunk
        :param matrix1_sor:     A matrix sorainak szama
        :param matrix1_oszlop:  A matrix oszlopainak szama
        :param matrix2_sor:     B matrix sorainak szama
        :param matrix2_oszlop:  B matrix oszlopainak szama
        """

        # ha hiba javitas utan generalunk a hiba uzenet tunjon el
        if self.error_frame is not None:
            self.error_frame.destroy()

        # hiba uzenetnek a frame
        self.error_frame = tk.Frame(tab)

        # kozepre igazitas
        self.error_frame.grid_columnconfigure(0, weight=1)
        self.error_frame.grid_columnconfigure(1, weight=1)

        # elozo megoldas torlese
        if self.result_frame is not None:
            self.result_frame.destroy()

        # generalas elotti parameter ellenorzes
        try:
            matrix1_sor_ertek = int(matrix1_sor.get())
            matrix1_oszlop_ertek = int(matrix1_oszlop.get())
            matrix2_sor_ertek = int(matrix2_sor.get())
            matrix2_oszlop_ertek = int(matrix2_oszlop.get())
        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas :{e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # szabaly szerint ellenorzes valamint nem lehet negativ vagy 0
        if ((matrix1_oszlop_ertek!=matrix2_sor_ertek) or (matrix1_oszlop_ertek <= 0 or matrix2_oszlop_ertek <= 0 or matrix2_sor_ertek <= 0 or matrix1_sor_ertek <= 0)):
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame,wraplength=300,justify='left', text="Két mátrixot csak akkor lehet összeszorozni, ha az első mátrix oszlopszáma, megegyezik a második mátrix sorzámával",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=5, column=0)
            return False

        #a ket generalt matrixnak egy masodlagos frame (ha ujra generalnank ne rakja egymasra az elozo matrixokra, hanem torolje)
        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        # torles utani reset (tehat ujra letrahozas)
        self.secondary_frame = tk.Frame(tab)

        self.block3 = ttk.LabelFrame(self.secondary_frame, text="Mátrix 1")
        self.block4 = ttk.LabelFrame(self.secondary_frame, text="Mátrix 2")

        self.matrix1_entries = [[None] * matrix1_oszlop_ertek for i in range(matrix1_sor_ertek)]

        # matrix 1 kiiratasa
        for i in range(matrix1_sor_ertek):
            for j in range(matrix1_oszlop_ertek):
                entry = ttk.Entry(self.block3, width=5)
                self.matrix1_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

        self.matrix2_entries = [[None] * matrix2_oszlop_ertek for i in range(matrix2_sor_ertek)]

        # matrix 2 kiiratasa
        for i in range(matrix2_sor_ertek):
            for j in range(matrix2_oszlop_ertek):
                entry = ttk.Entry(self.block4, width=5)
                self.matrix2_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

        # ha sajat adat tab akkor ne toltse fel
        if (self.sajat_adatok == tab):
            pass
        else:
            self.generate_data(self.matrix1_entries)
            self.generate_data(self.matrix2_entries)

        self.block3.grid(row=4, column=0, padx=(0, 15))
        self.block4.grid(row=4, column=1)


        self.result_frame=tk.Frame(tab)

        # megoldas gomb
        ttk.Button(self.secondary_frame, text="Mátrixok összeszorzása", command=lambda:self.solver_controller.solver_handler('matrix_mult',self.result_frame,self.matrix1_entries,self.matrix2_entries)).grid(row=5, column=0, columnspan=2)
        self.secondary_frame.grid(row=2, column=0,columnspan=2)

    def generate_data(self, entry_list):
        """
        A program kap egy listat ami [[None]*meret_a for i in range(meret_b)] alakban kapja meg
        (univerzalis hasznalat miatt ilyen az alak)
        A lista entry mezoket tartalmaz
        :param entry_list: adatok amiket felkell tolteni random ertekkel
        """
        for i in range(len(entry_list)):
            for j in range(len(entry_list[i])):
                entry_list[i][j].insert(0,random.randint(0, 10))



