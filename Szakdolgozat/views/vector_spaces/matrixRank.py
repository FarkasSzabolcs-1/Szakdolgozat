import random
import tkinter as tk
from tkinter import ttk


class Matrixrank(tk.Frame):
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
        ttk.Label(title_frame, text="Mátrix rangja",style='Title.TLabel').grid(row=0,column=0)
        ttk.Button(self, text="Vissza",style='Back.TButton', command=lambda: self.controller.show_screen("Vectorspacemenu")).grid(row=1,column=0,sticky="w")
        title_frame.grid(row=0,column=0)

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
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Példa adatok tab: Random generált értékek.').grid(row=0, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Saját adatok tab: Felhasználó által megadott értékek.').grid(row=1, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Üres mezőket a program nem fogad el.').grid(row=2, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Mátrix rangja')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egy B vektorrendszerről maximálisan kiválasztható r lineárisan független vektorok számát a vektorrendszer rangjának nevezzük.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Egymás mellé helyezve az oszlopvektorokat egy A mátrixot kapunk, aminek a rangja nem más mint rang(A) értelmezés szerint azonos az r vektorrendszer rangjával.').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A mátrix rangjára a következő állítások igazak:').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-r<=min(m,n),rang(A^t)=rang(A)').grid(
            row=4, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A kicserélési tételből következik tehát, hogy a mátrix rangja egyenlő a maximálisan választható főelemek számával.').grid(
            row=5, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Az egyik legelterjedtebb és legszisztematikusabb módszer a bázistranszformáció, amely lépésről lépésre haladva vizsgálja meg a vektorok egymástól való lineáris függetlenségét.').grid(
            row=5, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Elkészítünk egy kiinduló táblázatot, majd keresünk egy nullától különböző elemet (főelemet). A transzformáció során a kiválasztott főelem sora és oszlopa mentén módosítjuk a tábllázat többi elemét a báziscsere szabályai szerint.').grid(
            row=6, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Ezt a lépést ismételjük mindaddig, amíg találunk bevihető vektort és egy nem nullával azonos főelemet. A rendszer rangja pontosan egyenlő azzal a számmal, ahány alkalommal sikeresen ki tudtunk választani főelemet.').grid(
            row=7, column=0, sticky='we')
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
        block1 = ttk.LabelFrame(main_grid, text="Mátrix mérete")
        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="sor:").grid(row=2, column=0)
        matrix1_szam1 = ttk.Entry(block1)
        matrix1_szam1.grid(row=2, column=1)
        ttk.Label(block1, text="oszlop:").grid(row=3, column=0)
        matrix1_szam2 = ttk.Entry(block1)
        matrix1_szam2.grid(row=3, column=1)
        block1.grid(row=2, column=0,columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix1_szam1, matrix1_szam2)).grid(row=8, column=0, columnspan=2)

    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0,weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Mátrix mérete")
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0,columnspan=2)
        ttk.Label(block1, text="sor:").grid(row=2, column=0)
        matrix1_szam1 = ttk.Entry(block1)
        matrix1_szam1.grid(row=2, column=1)
        ttk.Label(block1, text="oszlop:").grid(row=3, column=0)
        matrix1_szam2 = ttk.Entry(block1)
        matrix1_szam2.grid(row=3, column=1)
        block1.grid(row=2, column=0,columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix1_szam1, matrix1_szam2)).grid(row=8, column=0, columnspan=2)

    def build_matrix(self, tab, matrix1_sor, matrix1_oszlop):
        """
        A program legeneralja a parametereknek megfelelo matrixot es megjeleniti az ablakon
        :param tab:             frame amiben dolgozunk
        :param matrix1_sor:     matrix sorainak szama
        :param matrix1_oszlop:  matrix oszlopainak szama
        """

        # matrix ertekeinek kinyeresenek elokeszitese
        matrix1_entries = []

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()


        self.error_frame = tk.Frame(tab)

        if self.result_frame is not None:
            self.result_frame.destroy()

        # generalas elotti ertek ellenorzes
        try:
            matrix1_sor_ertek = int(matrix1_sor.get())
            matrix1_oszlop_ertek = int(matrix1_oszlop.get())

        except Exception as e:

            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas :{e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        if(matrix1_oszlop_ertek<=0 or matrix1_sor_ertek<=0):
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg 0-nal nagyobb erteket",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # frame reseteles
        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        self.secondary_frame = tk.Frame(tab)

        if self.block3 is not None:
            self.block3.destroy()

        # matrix generalasa es kiiratasa
        self.block3 =ttk.LabelFrame(tab, text="Mátrix")
        matrix1_entries = [[None] * matrix1_oszlop_ertek for i in range(matrix1_sor_ertek)]
        for i in range(matrix1_sor_ertek):
            for j in range(matrix1_oszlop_ertek):
                entry = ttk.Entry(self.block3, width=5)
                matrix1_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

        # ha sajat adat tab akkor ne toltse fel
        if (self.sajat_adatok == tab):
            pass
        else:
            self.generate_data(matrix1_entries)

        self.block3.grid(row=1, column=0,columnspan=2)
        self.result_frame = tk.Frame(tab)

        # megoldas gomb
        ttk.Button(self.secondary_frame, text="Mátrix rangjának kiszámítása",command=lambda: self.solver_controller.solver_handler('matrix_rank',self.result_frame, matrix1_entries,matrix1_sor_ertek,matrix1_oszlop_ertek)).grid(row=5, column=0, columnspan=2)
        self.secondary_frame.grid(row=2, column=0, columnspan=2)
        self.result_frame.grid(row=3,column=0, columnspan=2)

    def generate_data(self, entry_list):
        """
        A program a kapott beviteli mezoket feltolti random generalt ertekekkel
        :param entry_list:  beviteli mezok
        """
        for i in range(len(entry_list)):
            for j in range(len(entry_list[i])):
                entry_list[i][j].insert(0, random.randint(0, 50))