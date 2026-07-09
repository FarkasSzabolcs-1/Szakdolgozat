import random
import tkinter as tk
from tkinter import ttk


class Matrixdeterminant(tk.Frame):
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
        ttk.Label(title_frame, text="Mátrix Determinánsa",style='Title.TLabel').grid(row=0,column=0)
        ttk.Button(self, text="Vissza",style='Back.TButton', command=lambda: self.controller.show_screen("Matrixmenu")).grid(row=1,column=0,sticky="w")
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

    # Tulajdonsagok tab
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

        math_rules = ttk.LabelFrame(tab, text='Mátrix determinánsa')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-n-tényezős szorzatokat képezünk minden lehetséges módon úgy, hogy a mátrix minden sorából és oszlopából pontosan egy tényezőt veszünk. A következő lépésben minden egyes szorzatot a “+” vagy “-” előjellel látunk el. Ez azt jelenti, hogy vagy magát a szorzatot, vagy pedig a negatívját tekintjük. Végül ezeket az előjeles szorzatokat összeadjuk. Az így kapott összeget nevezzük az A mátrix determinánsának.'
                  ).grid(
            row=0, column=0, sticky='we')

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
        block1 = ttk.LabelFrame(main_grid, text="Mátrix mérete")
        ttk.Label(main_grid, text="Példa adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="Mátrix rendje:").grid(row=2, column=0)
        matrix_size = ttk.Entry(block1)
        matrix_size.grid(row=2, column=1)
        block1.grid(row=2, column=0, columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix_size)).grid(row=8, column=0, columnspan=2)

    def build_empty_datas(self):
        """
        parameter beviteli panel betoltese, generalas utan ures mezokkel
        """
        tab = self.sajat_adatok
        # kozepre igazitas
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Mátrix mérete")
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0,columnspan=2)
        ttk.Label(block1, text="Mátrix rendje:").grid(row=2, column=0)
        matrix_size = ttk.Entry(block1)
        matrix_size.grid(row=2, column=1)
        block1.grid(row=2, column=0,columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_matrix(tab, matrix_size)).grid(row=8, column=0, columnspan=2)

    def build_matrix(self, tab, entry_matrix_size):
        """
        A program legeneralja a parameterek szerint a mezoket es felkesziti a veluk torteno muveletre
        :param tab:                 frame amiben dolgozunk
        :param entry_matrix_size:   matrix merete ami segitsegevel general
        """

        # elozo framek torlese
        if self.error_frame is not None:
            self.error_frame.destroy()
        self.error_frame = tk.Frame(tab)
        if self.result_frame is not None:
            self.result_frame.destroy()

        # generalas elotti ellenorzes
        try:
            matrix_size = int(entry_matrix_size.get())
        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # nemlehet 0 vagy kisebb
        if (matrix_size <= 0):
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg 0-nál nagyobb számot",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # masodlagos frame keszitese
        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        self.secondary_frame = tk.Frame(tab)
        self.block3 = tk.LabelFrame(self.secondary_frame, text="Mátrix")
        self.matrix1_entries = [[None] * matrix_size for i in range(matrix_size)]

        # generalt matrix kirajzolasa
        for i in range(matrix_size):
            for j in range(matrix_size):
                entry = ttk.Entry(self.block3, width=5)
                self.matrix1_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

        # ha sajat adat tab akkor ne toltse fel
        if (self.sajat_adatok == tab):
            pass
        else:
            self.generate_data(self.matrix1_entries)
        self.block3.grid(row=4, column=0,columnspan=2)
        self.result_frame = tk.Frame(tab)

        # kiszamitas gomb
        ttk.Button(self.secondary_frame, text="Determináns számítása",command=lambda: self.solver_controller.solver_handler('matrix_determinant',self.result_frame, self.matrix1_entries)).grid(row=5, column=0, columnspan=2)
        self.secondary_frame.grid(row=2, column=0, columnspan=2)

    def generate_data(self, entry_list):
        """
        A program kap egy listat ami [[None]*meret_a for i in range(meret_b)] alakban kapja meg
        (univerzalis hasznalat miatt ilyen az alak)
        A lista entry mezoket tartalmaz

        :param entry_list: adatok amiket felkell tolteni random ertekkel
        """
        for i in range(len(entry_list)):
            for j in range(len(entry_list[i])):
                entry_list[i][j].insert(0, random.randint(0, 50))
