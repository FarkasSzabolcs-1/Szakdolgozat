from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Vectorproblems():
    def __init__(self):
        self.results = None

    def vector_norm(self, tab, vector_matrix):
        """
        Egy vektor hosszanak (normajanak) a kiszamitasa a Pitagorasz tetel segitsegevel, majd ennek kirajzolasa
        norma=(x^2 + y^2 + z^2)^(1/2)
        :param tab: frame amire az informaciokat visszairjuk
        :param vector_matrix: a kiszamolni kivant vektor
        """
        #hiba esetén törölje az előző megoldást ha van
        if self.results is not None:
            self.results.destroy()

        #frame amire kiíratjuk a megoldást
        self.results = ttk.Frame(tab)

        #norma kiszámítása pitagorasz tétel segítségével
        vector_norm = ( vector_matrix[0]**2 + vector_matrix[1]**2 + vector_matrix[2]**2 )**(1/2)

        # origo létrehozása
        vector_origo = np.zeros(3)

        # 3D diagram előkészítése, méretezése
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection="3d")

        # diagram határának meghatarozasa
        lim = max(vector_matrix)
        min_lim=min(vector_matrix)

        if min_lim>0:
            min_lim=0
        if (lim <0):
            lim=0

        ax.set_xlim(min_lim, lim)
        ax.set_ylim(min_lim, lim)
        ax.set_zlim(min_lim, lim)

        # vektor megrajzolása
        ax.quiver(
            *vector_origo,
            *vector_matrix,
            color='red', linewidth=3,
            arrow_length_ratio=0.15,label=f"A vektor normája: {round(vector_norm, 2)}"
        )
        #canvas amiben a diagram szerepel es az ablakra vetítünk
        canvas = FigureCanvasTkAgg(fig, master=self.results)

        # diagram felcimkézése
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Vektor normája')
        ax.legend()

        # diagram kirajzolása az ablakba
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)

        self.results.grid(row=7, column=0)


    def vector_sum(self, diagram, vector1, vector2):
        """
        Ket vektor osszeadasa, majd pedig kirajzolasa egy diagramra
        Minden koordinatat a sajat koordinatjaval adjuk hozza.
        :param diagram: diagram amire rajzolunk vektort
        :param vector1: vektor1
        :param vector2: vektor2
        """
        # összeadott vektor előkészítése
        sum_vector = []
        # ciklus amivel a két vektort összeadjuk
        for i in range(len(vector1)):
            sum_vector.append(vector1[i] + vector2[i])

        #az osszeadott vektor numpy kompatibilisse alakitasa hatarszamitashoz
        sum_vector_mx = np.array(sum_vector)

        # diagram hatarainak meghatarozasa
        lim = max(sum_vector_mx.max(),vector1.max(),vector2.max())
        min_lim = min(sum_vector_mx.min(),vector1.min(),vector2.min())

        if (min_lim>0):
            min_lim=0
        if (lim <0):
            lim=0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        # az osszeadott vektor kirajzolasa
        diagram.quiver(
            0, 0, 0,
            sum_vector_mx[0], sum_vector_mx[1], sum_vector_mx[2],
            color='purple', linewidth=3,
            arrow_length_ratio=0.15, linestyle="dashed"

        )

        #diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

    def vector_mult(self, diagram, vector, scalar):
        """
        Egy vektor skalarral valo szorzasa, majd pedig ennek kirajzolasa egy diagrammra.
        Minden koordinatat megszorzunk az adott skalarral
        :param diagram:
        :param vector:
        :param scalar:
        """
        #új vektor előkészítése
        mult_vector = []

        #skalárral való szorzás elemről elemre
        for i in range(len(vector)):
            mult_vector.append(vector[i] * scalar)

        # Korlat szamolashoz atalakitjuk a kapott skalarral szorzott vektort
        mult_vector_mx=np.array(mult_vector)

        # korlat szamolas
        lim = max(vector.max(),mult_vector_mx.max())
        min_lim = min(vector.min(),mult_vector_mx.min())

        if min_lim > 0:
            min_lim = 0
        if (lim <0):
            lim=0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        # kiszamolt vektor kirajzolasa
        diagram.quiver(
            0, 0, 0,
            mult_vector[0], mult_vector[1], mult_vector[2],
            color='red', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"

        )

        #diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

    # lineáris kombináció kiszámítása
    def vector_linear_combination(self, tab, vector1, vector2, scalars):
        """
        Linearis kombinacio kiszamolasakor a ket vektort megszorozzuk a kivant skalar ertekkel, majd pedig a ket vektort osszeadjuk.
        Ezutan a kapott vektort kirajzoljuk a diagramra
        :param diagram: diagram amire a vektort kirajzoljuk
        :param vector1: vektor1
        :param vector2: vektor2
        :param scalars: skalar
        """
        # diagram meretenek beallitasa
        fig = plt.figure(figsize=(5, 5))

        # diagram tipusanak beallitasa
        diagram = fig.add_subplot(111, projection="3d")

        # canvas letrehozasa amit az ablakra helyezunk
        canvas = FigureCanvasTkAgg(fig, master=tab)

        # diagram megjelenitese
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=0)
        mult_vector_1 = []
        mult_vector_2 = []

        # a két vektor skaláris szorzatának kiszámítása
        for i in range(len(vector1)):
            mult_vector_1.append(vector1[i] * scalars[0])

        for i in range(len(vector2)):
            mult_vector_2.append(vector2[i] * scalars[1])

        vector_combination = []

        # az új kiszámolt vektor lineáris kombináció segítségével
        for i in range(len(mult_vector_1)):
            vector_combination.append(mult_vector_1[i] + mult_vector_2[i])

        # a vektorokat korlat szamitashoz atalakitjuk
        vector1_coords = np.array(mult_vector_1)
        vector2_coords = np.array(mult_vector_2)
        vector_linear_coords = np.array(vector_combination)

        lim = max(vector1_coords.max(),vector2_coords.max(),vector_linear_coords.max())
        min_lim=min(vector1_coords.min(),vector2_coords.min(),vector_linear_coords.min())

        if min_lim>0:
            min_lim=0
        if (lim <0):
            lim=0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        # koordinata rendszer elnevezese
        diagram.set_xlabel('X')
        diagram.set_ylabel('Y')
        diagram.set_zlabel('Z')
        diagram.set_title('Vektorok lineáris kombinációja')

        #origo
        vector_or=np.zeros(3)

        # ket alapvektor kirajzolasa
        diagram.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector1[0], vector1[1], vector1[2],
            color='blue', linewidth=3,
            arrow_length_ratio=0.15,
        )

        diagram.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector2[0], vector2[1], vector2[2],
            color='blue', linewidth=3,
            arrow_length_ratio=0.15,
        )
        diagram.text(*vector1, 'u vektor')
        diagram.text(*vector2, 'v vektor')

        # skalarral szorzott vektorok
        diagram.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector1_coords[0], vector1_coords[1], vector1_coords[2],
            color='red', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"

        )

        diagram.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector2_coords[0], vector2_coords[1], vector2_coords[2],
            color='red', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"

        )


        # linearis kombinacioval kiszamolt vektor
        diagram.quiver(
            vector_or[0], vector_or[1], vector_or[2],
            vector_linear_coords[0], vector_linear_coords[1], vector_linear_coords[2],
            color='purple', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed",label='Az új vektor a lineáris kombinációból'

        )

        #kiegeszito vektorok
        diagram.quiver(
            *vector1_coords,
            *(vector_linear_coords-vector1_coords),
            color='grey', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"

        )
        diagram.quiver(
            *vector2_coords,
            *(vector_linear_coords - vector2_coords),
            color='grey', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"

        )

        # elnevezesek kiirasa
        diagram.legend()

        #diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

    # a két vektor skaláris szorzat kiszámítása
    def vector_scalar_mult(self, tab, vector1, vector2):
        """
        Ket vektor skalaris szorzata a ket vektor koordinatainak a szorzata, majd pedig ezeket osszeadjuk
        A ket vektor altal bezart szoget kitudjuk szamolni ugy hogy cos_a = scalar_value / (vector1_norm * vector2_norm)
        :param tab: frame amire az informaciokat vissza iratjuk
        :param vector1: vektor1
        :param vector2: vektor2
        """
        # skaláris szorzat kiszámítása
        # értékek szorzatának összege
        scalar_value = 0
        for i in range(len(vector1)):
            scalar_value += vector1[i] * vector2[i]

        # két vektor közötti szög koszinusz kiszámítása
        cos_a = scalar_value / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

        # előző eredmény törlése, majd felkészítése egy új eredményre
        if self.results is not None:
            self.results.destroy()

        self.results = ttk.LabelFrame(tab,text='Eredmények')

        # skaláris szorzat kiírása
        ttk.Label(self.results, text="2 vektor skaláris szorzata : " + str(round(scalar_value, 2))).grid(row=5,column=0)

        # a vektorok által bezárt szög pontos foka
        ttk.Label(self.results, text=f"u és v által bezárt szög : {round(np.degrees(np.arccos(cos_a)), 2)}°").grid(row=6,column=0)
        self.results.grid(row=7, column=0)

    # vektoriális szorzat kiszámítása
    def vectorial_mult(self,tab, diagram, vector1, vector2):
        """
        Kiszamolja a ket vektor vektorialis szorzatat, ami meroleges lesz a ket vektor altal letrehozott sikra, ezeket pedig kirajzolja a diagramra.
        Kiszamolja a ket vektor altal bezart szoget, es a vektorialis szorzat hosszat.
        :param tab:     frame amire az informaciokat kiiratjuk
        :param diagram: diagram amire kirajzoljuk a vektorialis szorzatot
        :param vector1: vektor1
        :param vector2: vektor2
        """
        # kapott vektor előkészítése
        vectorial_mult = []

        # x coord
        coord = (vector1[1] * vector2[2]) - (vector1[2] * vector2[1])
        vectorial_mult.append(coord)

        # y coord
        coord = (vector1[2] * vector2[0]) - (vector1[0] * vector2[2])
        vectorial_mult.append(coord)

        # z coord
        coord = (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])
        vectorial_mult.append(coord)

        # kapott vektor vektorialis szorzat alapjan
        vectorial_vector = np.array(vectorial_mult)

        #a vektorok hosszanak kiszamitasa
        vectorial_vector_norm=np.linalg.norm(vectorial_vector)
        norm_1=np.linalg.norm(vector1)
        norm_2 = np.linalg.norm(vector2)

        # a ket eredeteti vektor altal bezart szog szinusza
        sin_a=vectorial_vector_norm/(norm_1*norm_2)

        # u és v vektor hajlásszöge, radian szogge alakitasa
        radian = np.arcsin(sin_a)
        degree = np.degrees(radian)


        # a diagram korlatainak meghatarozasa
        lim = max(vector1.max(),vector2.max(),vectorial_vector.max())
        min_lim =min(vector1.min(),vector2.min(),vectorial_vector.min())

        if min_lim >0:
            min_lim=0
        if (lim <0):
            lim=0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        #vektorialis szorzat alapjan kiszamolt vektor kirajzolasa
        diagram.quiver(
            0, 0, 0,
            vectorial_vector[0], vectorial_vector[1], vectorial_vector[2],
            color='purple', linewidth=2,
            arrow_length_ratio=0.15, linestyle="dashed"
        )

        #elozo eredmeny resetelese
        if self.results is not None:
            self.results.destroy()

        self.results = ttk.LabelFrame(tab,text="Eredmény")

        #informaciok kiiratasa
        ttk.Label(self.results, text=f"u és v által bezárt szög : {round(degree,2)}°").grid(row=6,column=0)
        ttk.Label(self.results, text = f'A vektoriális szorzat hossza: {round(vectorial_vector_norm, 2)}').grid(row=7,column=0)
        self.results.grid(row=3,column=0)

        # diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

    def triangle_solution(self, tab, diagram, ab_vector, bc_vector, ca_vector,a_coord,b_coord,c_coord):
        """
        A harom pont megadasaval egy 3D terben kiszamolja az ezek altal kirajzolt haromszog tulajdonsagait
        Kirajzolja egy diagramra es kiiratja a tulajdonsgagokat.

        :param tab:         frame amire az informaciokat kiiratjuk
        :param diagram:     digram amire a haromszoget kirajzoljuk
        :param ab_vector:   AB vektor
        :param bc_vector:   BC vektor
        :param ca_vector:   CA vektor
        :param a_coord:     A pont a terben
        :param b_coord:     B pont a terben
        :param c_coord:     C pont a terben
        """

        #elozo eredmenyek resetelese
        if self.results is not None:
            self.results.destroy()

        self.results = ttk.LabelFrame(tab,text='A háromszög tulajdonságai:')

        #kerulet szamitas
        perimeter = 0
        perimeter += np.linalg.norm(ab_vector)
        perimeter += np.linalg.norm(bc_vector)
        perimeter += np.linalg.norm(ca_vector)

        ttk.Label(self.results, justify='left', text="A háromszög kerülete: " + str(round(perimeter, 2))).grid(row=5, column=0,sticky='w')

        #terulet szamitas
        vectorial_mult = []

        coord = (ab_vector[1] * bc_vector[2]) - (ab_vector[2] * bc_vector[1])
        vectorial_mult.append(coord)

        coord = (ab_vector[2] * bc_vector[0]) - (ab_vector[0] * bc_vector[2])
        vectorial_mult.append(coord)

        coord = (ab_vector[0] * bc_vector[1]) - (ab_vector[1] * bc_vector[0])
        vectorial_mult.append(coord)

        vectorial_vector = np.array(vectorial_mult)

        area = round(np.linalg.norm(vectorial_vector) / 2, 2)

        ttk.Label(self.results, justify='left', wraplength=350, text="A háromszög területe: " + str(round(area, 2))).grid(row=6, column=0,sticky='w')
        self.results.grid(row=7, column=0,sticky='n')


        #sulypont kiszamitasa
        sulypont = []

        for i in range(len(a_coord)):

            osszeg = a_coord[i] + b_coord[i] + c_coord[i]
            sulypont.append(osszeg / 3)


        diagram.scatter(*sulypont, color='black', s=10)

        diagram.text(*sulypont, 'G', fontsize=10, color='black')

        # A szog kiszamitasa
        a_scalar_value = 0
        for i in range(len(ab_vector)):
            a_scalar_value += ab_vector[i] * -ca_vector[i]

        cos_a = a_scalar_value / (np.linalg.norm(ab_vector) * np.linalg.norm(-ca_vector))

        # B szog kiszamitasa
        b_scalar_value = 0
        for i in range(len(ab_vector)):
            b_scalar_value += -ab_vector[i] * bc_vector[i]

        cos_b = b_scalar_value / (np.linalg.norm(-ab_vector) * np.linalg.norm(bc_vector))

        # C szog kiszamitasa
        c_scalar_value = 0
        for i in range(len(ab_vector)):
            c_scalar_value += ca_vector[i] * -bc_vector[i]

        cos_c = c_scalar_value / (np.linalg.norm(ca_vector) * np.linalg.norm(-bc_vector))

        #informaciok kiiratasa + (radiant szogge alakitani)
        ttk.Label(self.results, justify='left', text="A szög: " + str(round(np.degrees(np.arccos(cos_a)), 2))+"°").grid(row=7, column=0,sticky='w')
        ttk.Label(self.results, justify='left', text="B szög: " + str(round(np.degrees(np.arccos(cos_b)), 2))+"°").grid(row=8, column=0,sticky='w')
        ttk.Label(self.results, justify='left', text="C szög: " + str(round(np.degrees(np.arccos(cos_c)), 2))+"°").grid(row=9, column=0,sticky='w')


        #a haromszog kore irhato kor sugara
        outside_r = (np.linalg.norm(ab_vector) * np.linalg.norm(bc_vector) * np.linalg.norm(ca_vector)) / (4 * area)

        #a haromszogbe irhato kor sugara
        inside_r = (2 * area) / perimeter

        ttk.Label(self.results, justify='left', text="A háromszög köré írt kör sugara: " + str(round(outside_r, 2))).grid(row=10,column=0,sticky='w')
        ttk.Label(self.results, justify='left', text="A háromszögbe írt kör sugara: " + str(round(inside_r*2, 2))).grid(row=11, column=0,sticky='w')


        #A szoghoz tartozo magassag hossza
        a_magassag_hossz=(2*area)/np.linalg.norm(bc_vector)

        ttk.Label(self.results, justify='left', text="Az A csúcshoz tartó magasság hossza: " + str(round(a_magassag_hossz, 2))).grid(row=12, column=0,sticky='w')
        ttk.Label(self.results, justify='left', text=f'A háromszög súlypontja: [{str(round(sulypont[0], 2))},{str(round(sulypont[1], 2))},{str(round(sulypont[2], 2))}]').grid(row=13, column=0,sticky='w')
        self.results.grid(row=4, column=1)

        #diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()