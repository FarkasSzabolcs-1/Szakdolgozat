import tkinter as tk
from tkinter import ttk
from models.matrixProblems import Matrixproblems
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Portfoliooptimization(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.matrixSolver = solver_handler
        self.create_screen()

    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Portfólió optimalizálás", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza", style='Back.TButton',
                   command=lambda: self.controller.show_screen("Realproblemsmenu")).grid(row=1, column=0, sticky="w")
        title_frame.grid(row=0, column=0)

        # tabcontrol létrehozása a generálási módszerek, valamint a tulajdonságok elkülönítéséhez
        self.tabcontrol = ttk.Notebook(self)
        self.tabcontrol.grid(row=2, column=0,sticky='we')

        # frame-k létrehozása a két generálási módszerhez
        self.pelda_adatok = ttk.Frame(self.tabcontrol)
        self.tulajdonsagok = ttk.Frame(self.tabcontrol)

        # tabcontrol-hoz hozzáadása ezeknek a frameknek
        self.tabcontrol.add(self.pelda_adatok, text="Portfólió optimalizálás")
        self.tabcontrol.add(self.tulajdonsagok, text="Tulajdonságok")

        # framek alaphelyzetbe allitasa
        self.error_frame = None
        self.result_frame = None
        self.secondary_frame = None

        # meghívjuk a ket
        self.build_example_datas()
        self.show_rules()





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
                  text=f'-Portfólió optimalizálás tab: a két eszközös kockázat-minimalizálási feladat').grid(row=0, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Kockázat/Szórás mezők-> pl. 0.15\n'
                       f'-Súly mezők-> pl. 40% (összegük mindig 100%)\n'
                       f'-Korelációs együttható-> -1 és 1 között, pl. 0.12').grid(row=1, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Üres mezőket a program nem fogad el.').grid(row=2, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-Szöveget tartalmazó mezőket a program nem fogad el.').grid(row=3, column=0, sticky='we')
        math_rules = ttk.LabelFrame(tab, text='Portfólió optimalizálás')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A portfólió teljes kockázatát a hozamok szórásával mérjük. Egy két eszközből álló portfólió varianciája:').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-σp² = (wA² * σA²) + (wB² * σB²) + (2 * wA * wB * σAB) , ahol:').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -σ: szórás jele\n'
                       f'   -σp²: A portfólió varianciája\n'
                       f'   -σA: A részvény szórása\n'
                       f'   -σB: A kötvény szórása\n'
                       f'   -wA: A részvény súlya\n'
                       f'   -wB: A kötvény súlya\n'
                       f'   -σAB: A két eszköz közötti kapcsolat (kovariancia)').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A kovariancia kiszámítható a következőképpen:\n'
                       f'   kovariancia = korreláció * részvény_szórás * kötvény_szórás\n'
                       f'-A korrelacio azt méri, hogyan ingazodik a két eszköz egymáshoz képest.').grid(
            row=4, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                 text=f'-A program kiszámolja a két eszköz kombinációjából adódó szórásfüggvény abszolút minimumát.').grid(
            row=5, column=0, sticky='we')


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
        block1 = ttk.LabelFrame(main_grid,text='Paraméterek beállítása')

        self.scale_frame = ttk.LabelFrame(block1,text = f'Eszközök súlya (%):')
        self.scale_frame.grid(row=6,column=0,columnspan=3)

        # kotveny es reszveny suly
        self.kotveny_entry = ttk.Entry(self.scale_frame,width=5)
        self.reszveny_entry = ttk.Entry(self.scale_frame,width=5)



        self.kotveny_entry.grid(row=7,column=1)
        self.reszveny_entry.grid(row=6, column=1)

        if self.result_frame is not None:
            self.result_frame.destroy()

        self.result_frame=ttk.Frame(tab)

        ttk.Label(self.scale_frame, text='Részvény: ').grid(row=6, column=0)
        ttk.Label(self.scale_frame, text='Kötvény: ').grid(row=7, column=0)

        ttk.Label(block1, text='Részvény->').grid(row=1, column=0)
        ttk.Label(block1, text='Kötvény->').grid(row=2, column=0)
        ttk.Label(block1, text='Szórás (kockázat) ').grid(row=0, column=1)

        self.entries = [[None]*2]

        # eszkozok szorasa
        for i in range(2):
            entry = ttk.Entry(block1)
            entry.grid(row=i+1,column=1)
            self.entries[0][i]=entry

        # korrelacios egyutthato
        ttk.Label(block1,text='Korrelációs együttható: ').grid(row=7,column=0,columnspan=2)
        korelacios_egyutthato = ttk.Entry(block1,width=20)
        korelacios_egyutthato.grid(row=7,column=2)


        # optimalizal gomb
        ttk.Button(block1, text="Portfólió optimalizálás", width=25,
                   command=lambda:self.kockazat_szamitas(self.result_frame,korelacios_egyutthato)).grid(row=8, column=0, columnspan=3)

        block1.grid(row=1, column=0)
        main_grid.grid(row=0, column=0,columnspan=2)
        self.result_frame.grid(row=2,column=0)

    def kockazat_szamitas(self,tab,korelacios_entry):
        """
        A program az optimalizalas gomb lenyomasa utan a kockazat minimalizalasi feladatot vegrehajtja.
        Kiszamitja a portfolio varianciajat a kovetkezo keplet szerint:
        σp² = (wA² * σA²) + (wB² * σB²) + (2 * wA * wB * σAB)
        (jelek megnevezeseert lasd tulajdonsag tab)
        :param tab:                 frame amiben dolgozunk
        :param korelacios_entry:    korrelacios egyutthato
        """


        #elozo diagram torlese
        plt.close()

        # elozo framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = ttk.Frame(tab)

        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        # eredmeny felkeszulese
        self.secondary_frame=ttk.LabelFrame(tab,text='Eredmény:')

        self.secondary_frame.grid(row=6,column=1,sticky='n')

        # ertekek ellenorzese es kinyerese
        try:
            resz_szor = float(self.entries[0][0].get())
            kotv_szor = float(self.entries[0][1].get())

            korelacio = float(korelacios_entry.get())
            resz_suly = float(self.reszveny_entry.get()) /100
            kotv_suly = float(self.kotveny_entry.get()) /100


            # korrelacio csak 1 es -1 kozott lehet
            if korelacio > 1 or korelacio <-1:
                ttk.Label(self.error_frame, text="A korelációs együttható csak -1 és 1 között lehet",
                          style="Error.TLabel").grid(row=0, column=0)
                print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
                self.error_frame.grid(row=5, column=0)
                return False

            # a sulyok osszege 100 mindig!
            if float(self.kotveny_entry.get())+float(self.reszveny_entry.get())!=100:
                ttk.Label(self.error_frame, text="Az eszközök súlya nem 1 (100%)",
                          style="Error.TLabel").grid(row=0, column=0)
                print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
                self.error_frame.grid(row=5, column=0)
                return False

            #kovariancia kiszamitasa
            kovarancia = korelacio * resz_szor * kotv_szor

            # portfolio varianciajanak kiszamitasa
            #σp² = (wA² * σA²) + (wB² * σB²) + (2 * wA * wB * σAB)
            var = (resz_suly ** 2 * resz_szor ** 2) + (kotv_suly ** 2 * kotv_szor ** 2) + (
                        2 * resz_suly * kotv_suly * kovarancia)

            # gyok alatt variancia
            kockazat = np.sqrt(var)

            # alap kockazat
            ttk.Label(self.secondary_frame, text=f'Alap kockázat = {kockazat}').grid(row=7,column=0)

            # osszes kockazat kiszamitasanak elokeszulete
            kock_mx = []

            #0%->100% ig minden kombinacio kiszamitasa
            for i in range(101):
                resz_suly = i/100
                kotv_suly = (100-i)/100
                var = (resz_suly ** 2 * resz_szor ** 2) + (kotv_suly ** 2 * kotv_szor ** 2) + (
                        2 * resz_suly * kotv_suly * kovarancia)

                kock=np.sqrt(var)
                kock_mx.append(kock)

            # legkisebb kockazat indexenek megkeresese
            index = np.argmin(kock_mx)
            #legkisebb kockazat
            min = np.min(kock_mx)

            # eredmeny kiiratasa optimalizalas utan
            ttk.Label(self.secondary_frame, text=f'----Optimalizálás után----').grid(row=8, column=0)
            ttk.Label(self.secondary_frame, text=f'Részvény súlya = {index}%').grid(row=9, column=0)
            ttk.Label(self.secondary_frame, text=f'Kötvény súlya  = {100-index}%').grid(row=10, column=0)
            ttk.Label(self.secondary_frame, text=f'Legkisebb kockázat = {min}').grid(row=11, column=0)

            # vizszintes tengely elokeszitese
            sulyok= [i for i in range(101)]

            #diagram letrehozasa, meret, tipus es frame adasa
            fig=plt.figure(figsize=(5,5))
            ax=fig.add_subplot(111)
            canvas=FigureCanvasTkAgg(fig,master=tab)

            # kockazat gorbe kirajzolasa
            ax.plot(sulyok,kock_mx,label="Portfólió kockázata",color='blue')

            # legkisebb kockazat megjelolese a diagrammon
            ax.scatter(index,min,color='red',s=30,zorder=5,label=f'Optimum: {index}%\n'
                                                                     f'Legkisebb kockázat: {min}')
            # cim, tengelyek elnevezese
            ax.set_title("Portfólió optimalizálás")
            ax.set_xlabel("Részvény súlya")
            ax.set_ylabel("Portfólió kockázata (Szórás)")
            #magyarazat kiiratasa
            ax.legend()

            # diagram kirajzolasa
            canvas.draw()
            canvas.get_tk_widget().grid(row=6, column=0)
            # diagram frissitese
            ax.figure.canvas.draw()
            ax.figure.canvas.flush_events()

        # egyeb hiba
        except Exception as e:
            tk.Label(self.error_frame, text="Kérem nézze újra a bevitt értékeket!",
                     style="Error.TLabel").grid(row=0, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=5, column=0)
            return False