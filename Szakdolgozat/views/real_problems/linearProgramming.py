import random
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Linearprogramming(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.solver_handler = solver_handler

        self.mode_options = {"Minimum":1,'Maximum':2}

        self.selected_mode = tk.StringVar(value=2)
        self.create_screen()

    def create_screen(self):
        """
        Ablak megnyitasakor a program letrehozza az alap parameter mezoket generalashoz
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Lineáris programozás",style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza",style='Back.TButton', command=lambda: self.controller.show_screen("Realproblemsmenu")).grid(row=1, column=0,
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

        # kozepre igazitas
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
        math_rules = ttk.LabelFrame(tab, text='Lineáris programozás')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Legyen egy m x n méretű mátrix, b egy m-komponensű vektor, és egy c n-komponensű vektor.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Keresünk egy olyan n komponensű x vektort, amely maximalizálja a cx lineáris függvényt az Ax = b, x>=0 lineáris feltételek mellett.').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Általános formájában egy LP feladat tartalmnazhat egyenlőtlenségi feltételt, előjelkötetlen változókat, maximalizálás helyett lehet minimalizálás a cél.').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-Mivel a minimalizálási és maximalizálási feladatok szoros kapcsolatban állnak egymással, a célfüggvény irányának megváltoztatása egyszerűen kezelhető azon azonosság révén, miszerint a cx függvény maximalizálása teljesen ekvivalens a -cx függvényérték minimalizálásával.').grid(
            row=4, column=0, sticky='we')

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
        block1 = ttk.LabelFrame(main_grid, text="Lineáris programozás felépítése")
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="Korlátozások száma:").grid(row=3, column=0)
        limit_equations = ttk.Entry(block1)
        limit_equations.grid(row=3, column=1)
        ttk.Label(block1, text="Ismeretlenek száma:").grid(row=4, column=0)
        unknown_values = (ttk.Entry(block1))
        unknown_values.grid(row=4, column=1)

        block1.grid(row=2, column=0, columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_equations(tab, limit_equations, unknown_values)).grid(row=8, column=0,
                                                                                                    columnspan=2)

    def build_empty_datas(self):
        """
        generalas gomb, megnyomasa utan ures mezokkel
        """
        tab = self.sajat_adatok
        tab.columnconfigure(0, weight=1)

        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.LabelFrame(main_grid, text="Lineáris programozás felépítése")
        ttk.Label(main_grid, text="Saját adatok").grid(row=0, column=0, columnspan=2)
        ttk.Label(block1, text="Egyenlőségek száma:").grid(row=3, column=0)
        limit_equations = ttk.Entry(block1)
        limit_equations.grid(row=3, column=1)
        ttk.Label(block1, text="Ismeretlenek száma:").grid(row=4, column=0)
        unknown_values = (ttk.Entry(block1))
        unknown_values.grid(row=4, column=1)

        block1.grid(row=2, column=0, columnspan=2)
        main_grid.grid(row=0, column=0, columnspan=2)

        ttk.Button(main_grid, text="Generálás", width=25,
                   command=lambda: self.build_equations(tab, limit_equations,unknown_values)).grid(row=8, column=0, columnspan=2)


    def build_equations(self, tab,limit_numbers,unknown_numbers):
        """
        A program legeneralja a kapott parameterek alapjan az egyenlosegeket, korlatozasi felteteleket, valamint az eredmenyvektort
        :param tab:                 frame amiben dolgozunk
        :param limit_numbers:       egyenlosegek szama
        :param unknown_numbers:     ismeretlenek szama
        """

        # elozo diagram torlese
        plt.close()

        #beviteli mezok elokeszitese
        self.limit_entries = []
        self.equation_entries = []
        self.combo_entries=[]
        self.limiters=[]

        # elozo framek torlese
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = tk.Frame(tab)

        if self.diagram_frame is not None:
            self.diagram_frame.destroy()

        if self.result_frame is not None:
            self.result_frame.destroy()

        # generalas elotti parameter ellenorzes es ertek kinyeres
        try:
            limit_size=int(limit_numbers.get())
            unknown_size=int(unknown_numbers.get())

        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        if limit_size <=0 or unknown_size <=0:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()
            ttk.Label(self.error_frame, text="Kérem adjon meg 0-nál nagyobb számot",style='Error.TLabel').grid(row=10, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False

        # frame reset
        if self.secondary_frame is not None:
            self.secondary_frame.destroy()

        self.secondary_frame = tk.Frame(tab)

        # mezok kiiratasanak elokeszitese
        self.block3 = ttk.LabelFrame(self.secondary_frame,text="Korlátozási feltételek")
        self.block4 = ttk.LabelFrame(self.secondary_frame, text='Célfüggvény:')
        self.block5 = ttk.LabelFrame(self.secondary_frame,text='Minimum|Maximum')


        # korlatozasi feltetelek
        combobox_values=['=','>=','<=']
        limit_combo_values=['>=','<=']

        self.limit_entries = [[None] * unknown_size for i in range(limit_size)]
        self.equation_entries = [[None] * unknown_size]
        self.combo_entries = [[None] * limit_size]
        self.limiters=[[None]*limit_size]

        # egyenlosegek matrixa + korlatozasi feltetelek + eredmenyvektor
        for i in range(limit_size):
            for j in range(unknown_size):

                # egyenlosegek matrixa
                entry = ttk.Entry(self.block3, width=5)
                self.limit_entries[i][j] = entry
                entry.grid(row=8 + i, column=0 + j)

            # korlatozasi feltetelek
            combo_box = ttk.Combobox(self.block3, values=combobox_values, width=5, state='readonly')

            self.combo_entries[0][i]=combo_box
            combo_box.grid(row=8+i,column=unknown_size+1)

            # eredmeny vektor
            limiter=ttk.Entry(self.block3,width=5)
            self.limiters[0][i]=limiter
            limiter.grid(row=8+i,column=unknown_size+2)



        # ismeretlenek korlatozasanak kiiratasa pl. x1,x2,x3 >=0
        for i in range(unknown_size):
            entry=ttk.Entry(self.block3,width=5)
            entry.insert(0,f'x{i+1}')
            entry.config(state='readonly')
            entry.grid(row=8+limit_size+1,column=i)

        #utolso combobox kikapcsolasa, hiszen az csak informativ (mindig pozitiv)
        self.unknown_limit_type_entry = ttk.Combobox(self.block3, values=limit_combo_values, width=5, state='readonly')
        self.unknown_limit_type_entry.grid(row=limit_size+1+8, column=unknown_size + 1)
        self.unknown_limit_type_entry.set('>=')

        #ismeretlenek korlatozasanak hatarertekenek entry kikapcsolasa, hiszen az csak informativ (mindig pozitiv)
        self.unknown_limit=ttk.Entry(self.block3,width=5)
        self.unknown_limit.grid(row=limit_size+1+8,column=unknown_size + 2)
        self.unknown_limit.insert(0,"0")

        # celfuggveny
        for i in range(unknown_size):

            entry = ttk.Entry(self.block4, width=5)
            self.equation_entries[0][i] = entry
            entry.grid(row=8, column=i,)

        # minimum vagy maximum radio gomb
        for (text, value) in self.mode_options.items():
            ttk.Radiobutton(self.block5, text=text, value=value, variable=self.selected_mode).grid(row= limit_size+10,column=value-1)


        # ha sajat adat tab akkor ne toltse fel
        if (self.sajat_adatok == tab):
            pass
        else:
            self.generate_data(self.limit_entries)
            self.generate_data(self.equation_entries)
            self.generate_data(self.limiters)

        # mezok kiiratasa kepernyore
        self.block3.grid(row=4, column=0 , padx=(0, 15))
        self.block4.grid(row=5, column=0)
        self.block5.grid(row=6,column=0)

        # szamitas gomb
        ttk.Button(self.secondary_frame, text="Kiszámítás",
                   command=lambda: self.linear_prog_solve(tab,unknown_size,limit_size)).grid(
            row=8, column=0, columnspan=2)
        self.secondary_frame.grid(row=2, column=0, columnspan=2)


    def generate_data(self, entry_list):
        """
        A program a kapott entry listat feltolti random generalt ertekekkel
        :param entry_list:  beviteli mezok
        """
        for i in range(len(entry_list)):
            for j in range(len(entry_list[i])):
                entry_list[i][j].insert(0, random.randint(0, 50))

    def linear_prog_solve(self,tab,unknown_size,limit_size):
        """
        A program a kapott ertekek alapjan kiszamolja a korlatozasi felteteleknek megfelelo eredmeny, es kiiratja kijelzore egy diagramban

        :param tab:             frame amiben dolgozunk
        :param unknown_size:    ismeretlenek szama
        :param limit_size:      korlatozasi feltetelek szama
        """

        #eredmenyek ellenorzesenek felkeszulese
        equation_values=[]
        limiters=[]

        # elozo diagram torlese
        plt.close()

        # elozo diagram frame reset
        if self.diagram_frame is not None:
            self.diagram_frame.destroy()
        self.diagram_frame=ttk.Frame(tab)
        self.diagram_frame.grid(row=4,column=0)

        # elozo hibak reset
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = ttk.Frame(tab)

        # ertekek ellenorzese es kinyerese
        try:

            # celfuggveny ertekei
            for i in range(unknown_size):
                value=float(self.equation_entries[0][i].get())
                equation_values.append(value)

            # korlatozasi feltetelek kijelolve
            for i in range(limit_size):
                if(self.combo_entries[0][i].get()=="" or self.unknown_limit_type_entry.get()==""):
                    ttk.Label(self.error_frame, text="Kérem válassza ki milyen határértéket szeretne",
                              style='Error.TLabel').grid(
                        row=10, column=0)
                    print(f"    \033[91m-> Sikertelen LP szamolas\033[0m")
                    self.error_frame.grid(row=4, column=0)
                    return False

            if float(self.unknown_limit.get())=="":
                ttk.Label(self.error_frame, text="Kérem válassza ki az ismeretlenek korlátozási értékét!",
                          style='Error.TLabel').grid(
                    row=10, column=0)
                print(f"    \033[91m-> Sikertelen LP szamolas\033[0m")
                self.error_frame.grid(row=4, column=0)
                return False

            # eredmenyvektor ertekei
            for i in range(limit_size):
                value=float(self.limiters[0][i].get())
                limiters.append(value)

            limit_equations = [[None] * unknown_size for i in range(limit_size)]

            # egyenlosegek matrixa
            for i in range(limit_size):
                for j in range(unknown_size):
                    value=float(self.limit_entries[i][j].get())
                    limit_equations[i][j]=value

        except Exception as e:
            ttk.Label(self.error_frame, text="Kérem válassza ki milyen határértéket szeretne",
                      style='Error.TLabel').grid(
                row=10, column=0)
            print(f"    \033[91m-> Sikertelen LP szamolas\033[0m {e}")
            self.error_frame.grid(row=4, column=0)
            return False

        # ha maximalizalunk, akkor negativva tesszuk a celfuggvenyt mert csak minimalizalni kepes a program
        if self.selected_mode.get() == "2":
            clfg = -np.array(equation_values)
        else:
            clfg = np.array(equation_values)

        # korlatozo listak letrahozasa
        # up= felso korlat -> <= felteteleknek
        # eq= egyenloseg   ->  = felteteleknek
        # A -> egyutthato matrix
        # b -> jobb oldali eredmeny vektor
        A_ub=[]
        b_ub=[]
        A_eq=[]
        b_eq=[]

        # korlatozasok feldolgozasa
        for i in range(limit_size):

            #aktualis egyutthato matrix sora
            current_row=limit_equations[i]

            #aktualis eredmenyvektor
            current_limit_val=limiters[i]
            limit_type=self.combo_entries[0][i].get()

            # jelek alapjan feltetelek atalakitasa
            # majd pedig feltoltjuk a korlatozo listaba
            if(limit_type=="<="):
                A_ub.append(current_row)
                b_ub.append(current_limit_val)

            #megforditjuk az elojelt
            elif(limit_type==">="):
                A_ub.append([value * -1 for value in current_row])
                b_ub.append(current_limit_val *-1)

            elif (limit_type == '='):
                A_eq.append(current_row)
                b_eq.append(current_limit_val)

        # NumPy tombbe alakitas, ahol nincs ertek ott None-ra valtoztatjuk
        A_ub=np.array(A_ub) if A_ub else None
        b_ub=np.array(b_ub) if b_ub else None
        A_eq=np.array(A_eq) if A_eq else None
        b_eq=np.array(b_eq) if b_eq else None

        # valtozok korlatainak beallitasa
        if(self.unknown_limit_type_entry.get()==">="):
            bounds_values=(float(self.unknown_limit.get()),None)
        elif(self.unknown_limit_type_entry.get()=="<="):
            bounds_values = (None,float(self.unknown_limit.get()))
        else:
            bounds_values = (None, None)

        # linearis programozas megoldasa
        result = linprog(c=clfg,A_ub=A_ub,b_ub=b_ub,A_eq=A_eq,b_eq=b_eq,bounds=bounds_values,method='highs')

        # ha van megoldas
        if result.success:
            # ha maximalizaltunk akkor vissza alakitjuk az erteket
            if (self.selected_mode.get() == "2"):
                final_value = -result.fun
            else:
                final_value = result.fun


            # megoldasok kiiratasa
            self.result_frame=ttk.LabelFrame(self.diagram_frame,text="Megoldások")
            self.result_frame.grid(row=6,column=0)

            # eredmenyek osszegyujtese
            valtozok_ertekei=[]
            for i in range(len(result.x)):
                valtozok_ertekei.append(float(round(result.x[i],2)))

            # optimalis ertek es valtozok kiiratasa
            ttk.Label(self.result_frame,text=f"Optimális érték: {final_value:.2f}").grid(row=0,column=0)
            ttk.Label(self.result_frame,text=f"Változók értékei: {valtozok_ertekei}").grid(row=1,column=0)


            # ha 2 ismeretlen, akkor 2D diagram
            if unknown_size ==2:

                # x es y megoldasok
                x_solution, y_solution = valtozok_ertekei

                # diagram merete, tipusa es framejenek beallitasa
                fig = plt.figure(figsize=(5, 5))
                ax = fig.add_subplot(111)
                canvas = FigureCanvasTkAgg(fig, master=self.result_frame)

                # egyenesek alapjanak elkeszitese
                x_values = np.linspace(x_solution - 5, x_solution + 5, 100)

                # egyenlet létrehozása: ax + by = c => y = (c - ax) / b
                for i in range(limit_size):
                    a = limit_equations[i][0]
                    b_orig = limit_equations[i][1]
                    c = limiters[i]

                    # 0 val valo osztas kezelese
                    if b_orig == 0:
                        b = 1e-9
                    else:
                        b = b_orig

                    # y ertekek kiszamitasa
                    y_values = (c - a * x_values) / b

                    # egyenes kirajzolasa
                    ax.plot(x_values, y_values, label=f'{a}x + {b_orig}y {self.combo_entries[0][i].get()} {c}')

                # a korlatozasi feltetelbool szarmazo fuggoleges es vizszintes vonalak
                ax.axhline(float(self.unknown_limit.get()),color='black')
                ax.axvline(float(self.unknown_limit.get()),color='black')
                # megoldas kiiratasa
                ax.scatter(x_solution, y_solution, color='black', s=20, zorder=3,
                           label=f'Megoldás: ({x_solution}, {y_solution})')

                # hatter
                ax.grid(True, linestyle="dashed", alpha=0.3)

                # dimenziok elnevezese
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_title("2 ismeretlenes lineáris programozás")

                # magyarazat kiirasa
                ax.legend()

                # diagram kirajzolasa
                canvas.draw()
                canvas.get_tk_widget().grid(row=6, column=0)


            # ha 3 ismeretlenes
            elif unknown_size==3:

                # diagram merete, frameje, es tipusanak beallitasa
                fig = plt.figure(figsize=(5, 5))
                ax = fig.add_subplot(111, projection='3d')
                canvas = FigureCanvasTkAgg(fig, master=self.result_frame)


                # sikok meretenek beallitasa
                lim = max(valtozok_ertekei)

                s = np.linspace(-lim - 5, lim + 5, 10)
                t = np.linspace(-lim - 5, lim + 5, 10)

                # sikok letrehozasa

                X, Y = np.meshgrid(s, t)


                colors = ['blue', 'green', 'red']

                # a harom sik kirajzolasa
                for i in range(limit_size):

                    a = limit_equations[i][0]
                    b = limit_equations[i][1]
                    c = limit_equations[i][2]

                    d = limiters[i]

                    if c == 0:
                        c = 1e-9

                    #ax+by+cz=d
                    Z = (d - a * X - b * Y) / c

                    # sik kirajzolasa
                    ax.plot_surface(X, Y, Z, alpha=0.5, color=colors[i])

                # harom sik metszespontja
                ax.scatter(*valtozok_ertekei, color='black', s=20, zorder=3,
                           label=f'Megoldás: ({valtozok_ertekei[0]},{valtozok_ertekei[1]},{valtozok_ertekei[2]})')

                # dimenziok elnevezese
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_title('3 ismeretlenes lineáris programozás')

                # magyarazatok kiirasa
                ax.legend()

                #diagram rajzolasa
                canvas.draw()
                canvas.get_tk_widget().grid(row=6, column=0)

            # ha tobb mint 3 akkor oszlopdiagram
            elif unknown_size>3:

                # diagram meretenek, framejenek, es tipusanak a beallitasa
                fig = plt.figure(figsize=(5, 5))
                ax = fig.add_subplot(111)
                canvas = FigureCanvasTkAgg(fig, master=self.result_frame)

                # indexek letrehozasa, attol fuggoen hany ismeretlen van
                indexes = np.arange(len(valtozok_ertekei))

                # megoldasok felpakolasa a diagramra
                ax.scatter(indexes, valtozok_ertekei, color='red', s=20, edgecolors='black', zorder=3, label='Megoldások')
                ax.plot(indexes, valtozok_ertekei, color='black', linestyle='dashed', alpha=0.3, zorder=2)

                # szoveg pakolasa az eredmenyek koordinataihoz
                for i in range(len(valtozok_ertekei)):
                    ax.text(i, valtozok_ertekei[i], f'{valtozok_ertekei[i]:.2f}')

                # Megoldasok cimkezese
                x_titles = [f'x{i}' for i in range(len(valtozok_ertekei))]

                # axisok elnevezese
                plt.xticks(indexes, x_titles, fontsize=10)
                plt.xlabel("Ismeretlenek", fontsize=10)
                plt.ylabel("Értékek", fontsize=10)

                # vizszintes fekete vonal az origobol (negativ ertekek jobban lathatoak legyenek)
                ax.axhline(0, color='black', linewidth=1, zorder=1)

                # halo a hatterbe, hogy jobban lathatoak legyenek az ertekek
                ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

                # diagram cime
                ax.set_title(f"{len(equation_values)} ismeretlenes egyenletrendszer megoldásai", fontsize=14)
                # diagram cimkezese
                ax.legend()

                # diagram rajzolasa
                canvas.draw()
                canvas.get_tk_widget().grid(row=6, column=0)

        # hiba eseten diagram torlese
        else:
            self.diagram_frame.destroy()
            # ha feltetelek ellentmondanak egymasnak
            if result.status==2:
                ttk.Label(self.error_frame, text="Az egyenlet nem oldható meg: A feltételek ellentmondanak egymásnak, nincs megoldás!",
                      style='Error.TLabel').grid(
                row=10, column=0)
            #celfuggveny vegtelenbe tart
            elif result.status==3:
                ttk.Label(self.error_frame,
                          text="Az egyenlet nem oldható meg: A célfüggvény a végtelenbe tart, mert a feltételek nem korlátozzák eléggé!",
                          style='Error.TLabel').grid(
                    row=10, column=0)
            # egyeb hiba
            else:
                ttk.Label(self.error_frame,
                          text="Az egyenlet nem oldható meg!",
                          style='Error.TLabel').grid(
                    row=10, column=0)

            self.error_frame.grid(row=4, column=0)
            print(f"    \033[91m-> Sikertelen egyenlet megoldás:\033[0m")
            print(f'nemsikerult megoldani:{result.message}')
            return False






