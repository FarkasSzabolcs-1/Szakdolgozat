import tkinter
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class Vectorspaceproblems():
    def __init__(self):
        self.results = None
        self.error_frame = None
        self.secondary_frame= None

    def vector_spaces(self,tab,vector1,vector2,scalar):
        """
        vektor terek 7-dik axióma bemutatása c(u+v)=cu+cv
        vektorok kiszamolasa, majd pedig kirajzolasa a diagramra

        :param tab:     tab amiben dolgozunk
        :param vector1: u vektor
        :param vector2: v vektor
        :param scalar:  c skalar
        """

        fig = plt.figure(figsize=(5,5))
        diagram = fig.add_subplot(111, projection="3d")
        canvas = FigureCanvasTkAgg(fig, master=tab)

        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)


        # vektorok előkészítése
        sum_vector=[]
        scalar_mult=[]
        scalar_vector1 = []
        scalar_vector2 = []
        vector1_into_sum = []
        vector2_into_sum = []
        scalar1_into_scalar_mult = []
        scalar2_into_scalar_mult = []

        # (u+v) kiszámítása
        for i in range(len(vector1)):
            sum_vector.append(vector1[i] + vector2[i])

        # c(u+v) kiszámítása
        for i in range(len(sum_vector)):
            scalar_mult.append(sum_vector[i]*scalar)
        sum_vector_mx=np.array(sum_vector)
        scalar_mult_mx=np.array(scalar_mult)

        # cu és cv kiszámítása
        for i in range(len(vector1)):
            scalar_vector1.append(vector1[i] * scalar)
            scalar_vector2.append(vector2[i] * scalar)
        scalar_vector1_mx = np.array(scalar_vector1)
        scalar_vector2_mx = np.array(scalar_vector2)

        # segédvektorok kiszámítása
        for i in range(len(vector1)):
            vector1_into_sum.append(sum_vector_mx[i]-vector1[i])
            vector2_into_sum.append(sum_vector_mx[i]-vector2[i])
        for i in range(len(vector1)):
            scalar1_into_scalar_mult.append(scalar_mult_mx[i]-scalar_vector1[i])
            scalar2_into_scalar_mult.append(scalar_mult_mx[i]-scalar_vector2[i])


        # korlat szamitashoz elokeszitjuk a vektorokat
        scalar_lim=np.array(scalar_mult_mx)
        vector1_lim=np.array(vector1)
        vector2_lim=np.array(vector2)
        sum_lim = np.array(sum_vector_mx)

        # korlat szamitas
        lim = max(scalar_lim.max(),scalar_vector1_mx.max(),scalar_vector2_mx.max(),vector1_lim.max(),vector2_lim.max(),sum_lim.max())
        min_lim= min(scalar_lim.min(),scalar_vector1_mx.min(),scalar_vector2_mx.min(),vector1_lim.min(),vector2_lim.min(),sum_lim.min())

        if min_lim>0:
            min_lim=0

        if lim<0:
            lim=0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        diagram.set_xlabel('X')
        diagram.set_ylabel('Y')
        diagram.set_zlabel('Z')
        diagram.set_title('7. axióma: c(u+v)=cu+cv')

        #origo
        origo=np.zeros(3)

        # a ket alap vektor kirajzolasa
        diagram.quiver(*origo, *vector1, color='red', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *vector2, color='blue', linewidth=3, arrow_length_ratio=0.15)

        # u+v vektor
        diagram.quiver(*origo,*sum_vector_mx,
            color='green', linewidth=3,
            arrow_length_ratio=0.1,label='u+v vektor'
        )
        # c(u+v) vektor
        diagram.quiver(*origo, *scalar_mult_mx,
                       color='green', linewidth=2.5,
                       arrow_length_ratio=0.1,alpha=0.55,label='c(u+v) vektor'
                       )

        # cu vektor
        diagram.quiver(*origo, *scalar_vector1_mx,
                       color='red', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55,label='cu vektor'
                       )
        # cv vektor
        diagram.quiver(*origo, *scalar_vector2_mx,
                       color='blue', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55,label='cv vektor'
                       )

        #kiegeszito vektorok
        diagram.quiver(*vector1, *vector1_into_sum,
                       color='red', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55,linestyle='dashed'
                       )
        diagram.quiver(*vector2, *vector2_into_sum,
                       color='blue', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55,linestyle='dashed'
                       )
        diagram.quiver(*scalar_vector1, *scalar1_into_scalar_mult,
                       color='red', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55, linestyle='dashed'
                       )
        diagram.quiver(*scalar_vector2, *scalar2_into_scalar_mult,
                       color='blue', linewidth=2.5,
                       arrow_length_ratio=0.1, alpha=0.55, linestyle='dashed'
                       )

        # magyarazat kiirasa es diagram frissitese
        diagram.legend()
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()



    def linear_independence(self,tab,vector_u_entry,vector_v_entry,vector_w_entry):
        """
        2 vektor letrehoz egy sikot, es egy haramadik vektor ha kilep a harmadik dimenzioba, akkor linearisan fuggetlen.
        A program az elso ketto vektor altal letrehozott sikra rapakolja a harmadik vektort, es ezeket pedig kirajzolja.
        Lathato lesz a linearis fuggetlenseg.

        :param tab:             tab amire kiirjuk az informaciokat
        :param vector_u_entry:  u vektor
        :param vector_v_entry:  v vektor
        :param vector_w_entry:  w vektor
        """

        #elozo diagram bezarasa
        plt.close()

        #vektorok elokeszitese
        vector1_matrix = []
        vector2_matrix = []
        vector3_matrix = []

        #hiba frame resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame = ttk.Frame(tab)


        # a 3 vektor ertekeinek az ellenorzese es ertekeinek a kinyerese
        try:
            for coord_entry in vector_u_entry:
                cooridnate = float(coord_entry.get())

                vector1_matrix.append(cooridnate)

            for coord_entry in vector_v_entry:
                cooridnate = float(coord_entry.get())

                vector2_matrix.append(cooridnate)

            for coord_entry in vector_w_entry:
                cooridnate = float(coord_entry.get())

                vector3_matrix.append(cooridnate)



        # szam vagy ures ertek eseten hiba
        except Exception as e:
            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            plt.close()

            ttk.Label(self.error_frame, text="Kérem adjon meg számot értékként!", style='Error.TLabel').grid(row=10,
                                                                                                             column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas: {e}\033[0m")
            self.error_frame.grid(row=5, column=0)
            tab.grid(row=4,column=0)
            return False

        # a harom vektor elokeszitese
        vector_v = np.array(vector1_matrix)
        vector_u = np.array(vector2_matrix)
        vector_w = np.array(vector3_matrix)

        matrix=[]
        matrix.append(vector_v)
        matrix.append(vector_u)
        matrix.append(vector_w)

        mx=np.array(matrix)

        det_mx=np.linalg.det(mx)

        if det_mx ==0:
            fuggetlenseg= 'A vektorok lineárisan függőek'
        else:
            fuggetlenseg= 'A vektorok lineárisan függetlenek'


        # diagram letrehozasa, es meret beallitasa
        fig = plt.figure(figsize=(5, 5))

        # diagram beallitasa, hogy 3D legyen
        ax = fig.add_subplot(111, projection="3d")

        # canvas letrehozasa, amibe belepakoljuk a diagrammot, es hogy melyik frameben lesz
        canvas = FigureCanvasTkAgg(fig, master=tab)

        # dimenziok megnevezese
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Lineáris függetlenség')

        # a 2 sik letrehozasanak az elkeszitese
        # s,t -1 és 1 kozotti ertekekkel feltoltott lista
        s = np.linspace(-1, 1, 10)
        t = np.linspace(-1, 1, 10)

        # sikokka alakitjuk
        S, T = np.meshgrid(s, t)

        # megadjuk a siknak, hogy a 2 vektor alapjan hogyan helyezkedjen el -> 2 vektor altal letrehozott sik
        X = vector_u[0] * S + vector_v[0] * T
        Y = vector_u[1] * S + vector_v[1] * T
        Z = vector_u[2] * S + vector_v[2] * T

        # a diagram korlatja sik alapjan
        lim = max(X.max(), Y.max(), Z.max())
        min_lim = min(X.min(), Y.min(), Z.min())
        if (lim) < 0:
            lim = 0
        if min_lim > 0:
            min_lim = 0
        ax.set_xlim(min_lim, lim)
        ax.set_ylim(min_lim, lim)
        ax.set_zlim(min_lim, lim)

        # sik kirajzolas
        ax.plot_surface(X, Y, Z, alpha=0.2, cmap=plt.cm.coolwarm)

        #origo
        origo=np.zeros(3)

        # a harom vektor kirajzolasa
        ax.quiver(*origo,*vector_w, color='green',linewidth=3,arrow_length_ratio=0.15,label=fuggetlenseg)
        ax.quiver(*origo, *vector_u, color='blue', linewidth=3, arrow_length_ratio=0.15)
        ax.quiver(*origo, *vector_v, color='red', linewidth=3, arrow_length_ratio=0.15)

        # origo kirajzolasa
        ax.scatter(0, 0, 0, s=20, color="black")

        # megjegyzes kiirasa
        ax.legend()
        #diagram rajzolasa es kivetitese az ablakra
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

        tab.grid(row=4, column=0, columnspan=2)

    def bases(self,tab,u_vector,v_vector,t_vector,scalar_a,scalar_b,scalar_c):
        """
        3 vektor alapjan a program kirajzolja a linearisan fuggetlen generatorrendszert.
        kiszamolja a 3 vektor skalarral valo szorzatat, valamint a linearis kombinaciojat.
        ezeket kirajzolja egy diagramra

        :param tab:         frame amiben dolgozunk
        :param u_vector:    u vektor
        :param v_vector:    v vektor
        :param t_vector:    t vektor
        :param scalar_a:    a skalar
        :param scalar_b:    b skalar
        :param scalar_c:    c skalar
        """

        #elozo diagram bezarasa
        plt.close()

        # diagram letrehozasa, meret, frame es tipus megadasa
        fig = plt.figure(figsize=(5, 5))
        diagram = fig.add_subplot(111, projection="3d")
        canvas = FigureCanvasTkAgg(fig, master=tab)





        #vektorok elokeszitese
        u_scalar_vector=[]
        v_scalar_vector = []
        t_scalar_vector = []

        # a három bázisvektort megszorozzuk a skalárokkal
        for i in range(len(u_vector)):
            u_scalar_vector.append(u_vector[i]*scalar_a)

        for i in range(len(v_vector)):
            v_scalar_vector.append(v_vector[i]*scalar_b)

        for i in range(len(t_vector)):
            t_scalar_vector.append(t_vector[i]*scalar_c)

        # origo
        origo=np.zeros(3)

        scalar_vector=[]
        scalar_vector.append(scalar_a)
        scalar_vector.append(scalar_b)
        scalar_vector.append(scalar_c)

        # eredo vektor kiszamitasa

        matrix=[]
        matrix.append(u_vector)
        matrix.append(v_vector)
        matrix.append(t_vector)

        mx=np.array(matrix)

        result=np.linalg.solve(mx,scalar_vector)



        # a három skalárvektor kirajzolása
        diagram.quiver(*origo, *u_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *v_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15,label='Skalárokkal szorzott vektorok')

        #linearis kombinacioval kiszamolt vektor elokeszitese
        mult_vector=result

        # Lineáris kombinációval kiszámolt eredő vektor
        diagram.quiver(*origo, *mult_vector, color='green', linewidth=3, arrow_length_ratio=0.15,label='Eredő vektor')
        diagram.scatter(*result,label=f"A három skalár [{round(result[0],2)},{round(result[1],2)},{round(result[2],2)}]")

        # a diagram korlatainak a kiszamitasanak az elokeszulete
        mult_vect_lim=np.array(mult_vector)
        vector1_lim = np.array(u_scalar_vector)
        vector2_lim = np.array(v_scalar_vector)
        vector3_lim = np.array(t_scalar_vector)

        #korlatok kiszamitasa
        lim = max(vector1_lim.max(), vector2_lim.max(), vector3_lim.max(),mult_vect_lim.max())
        min_lim = min(vector1_lim.min(), vector2_lim.min(), vector3_lim.min(),mult_vect_lim.max())


        if (lim) < 0:
            lim = 0
        if min_lim > 0:
            min_lim = 0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        #dimenziok elnevezese
        diagram.set_xlabel('X')
        diagram.set_ylabel('Y')
        diagram.set_zlabel('Z')
        diagram.set_title('Bázis')

        # a 3 bazisvektor kirajzolasa
        diagram.quiver(*origo, *u_vector, color='blue', linewidth=3, arrow_length_ratio=0.15, label='Bázisvektor')
        diagram.quiver(*origo, *v_vector, color='blue', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_vector, color='blue', linewidth=3, arrow_length_ratio=0.15)

        #segedvektorok kiszamolasa es kirajzolasa
        mult_to_u_vector=[]
        mult_to_v_vector = []
        mult_to_t_vector = []
        for i in range(len(u_vector)):
            mult_to_u_vector.append(u_scalar_vector[i]*-1)
            mult_to_v_vector.append(v_scalar_vector[i] * -1)
            mult_to_t_vector.append(t_scalar_vector[i] * -1)



        diagram.quiver(*u_scalar_vector,*v_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*u_scalar_vector,*t_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*v_scalar_vector,*u_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*v_scalar_vector,*t_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *u_scalar_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *v_scalar_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')

        diagram.quiver(*mult_vector, *mult_to_t_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_u_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_v_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')

        #diagram feliratozasa magyarazatnal
        diagram.legend()

        # diagram kirajzolasa
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

    def base_transformation(self,tab,u_vector,v_vector,t_vector,scalar_a,scalar_b,scalar_c,new_base):
        """
        Eloszor kirajzoljuk a bazist az eredeti bazis es skalar vektorok alapjan,
        majd utana az eredo vektor es az uj bazis alkalamzasaval bazis traszformaciot hajtunk vegre

        :param tab:         frame amiben dolgozunk
        :param u_vector:    u vektor
        :param v_vector:    v vektor
        :param t_vector:    t vektor
        :param scalar_a:    a skalar
        :param scalar_b:    b skalar
        :param scalar_c:    c skalar
        :param new_base:    az uj bazis
        """
        # diagram letrehozasa, meret, frame es tipus megadasa
        fig = plt.figure(figsize=(5, 5))
        diagram = fig.add_subplot(111, projection="3d")
        canvas = FigureCanvasTkAgg(fig, master=tab)

        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)

        #vektorok elokeszitese es skalarral valo szorzata
        u_scalar_vector=[]
        v_scalar_vector = []
        t_scalar_vector = []

        for i in range(len(u_vector)):
            u_scalar_vector.append(u_vector[i]*scalar_a)

        for i in range(len(v_vector)):
            v_scalar_vector.append(v_vector[i]*scalar_b)

        for i in range(len(t_vector)):
            t_scalar_vector.append(t_vector[i]*scalar_c)

        #origo
        origo=np.zeros(3)

        # 3 skalar vektor kirajzolasa
        diagram.quiver(*origo, *u_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *v_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_scalar_vector, color='red', linewidth=2, arrow_length_ratio=0.15)

        # vektor a 3 vektor linearis kombinaciojabol-> eredo vektor
        mult_vector=[]
        for i in range(len(u_vector)):
            mult_vector.append(u_scalar_vector[i]+v_scalar_vector[i]+t_scalar_vector[i])

        # diagram korlatozasanak kiszamitasanak az elokeszulete
        mult_vect_lim = np.array(mult_vector)
        vector1_lim = np.array(u_scalar_vector)
        vector2_lim = np.array(v_scalar_vector)
        vector3_lim = np.array(t_scalar_vector)

        # korlatozas kiszamitasa es beallitasa
        lim = max(vector1_lim.max(), vector2_lim.max(), vector3_lim.max(), mult_vect_lim.max())
        min_lim = min(vector1_lim.min(), vector2_lim.min(), vector3_lim.min(), mult_vect_lim.max())

        if (lim) < 0:
            lim = 0
        if min_lim > 0:
            min_lim = 0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        #dimenziok elnevezese
        diagram.set_xlabel('X')
        diagram.set_ylabel('Y')
        diagram.set_zlabel('Z')
        diagram.set_title('Bázis transzformáció')

        # eredo vektor kiszamitasa

        scalar_vector = []
        scalar_vector.append(scalar_a)
        scalar_vector.append(scalar_b)
        scalar_vector.append(scalar_c)


        matrix = []
        matrix.append(u_vector)
        matrix.append(v_vector)
        matrix.append(t_vector)

        mx = np.array(matrix)

        result = np.linalg.solve(mx, scalar_vector)

        mult_vector=result


        # bazis vektorok kirajzolasa
        diagram.quiver(*origo, *u_vector, color='blue', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *v_vector, color='blue', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_vector, color='blue', linewidth=3, arrow_length_ratio=0.15, label='Bázisvektor')

        #eredo vektor kirajzolasa
        diagram.quiver(*origo, *mult_vector, color='green', linewidth=3, arrow_length_ratio=0.15,label='Eredő vektor')


        # kiegeszito vektorok
        mult_to_u_vector=[]
        mult_to_v_vector = []
        mult_to_t_vector = []

        for i in range(len(u_vector)):
            mult_to_u_vector.append(u_scalar_vector[i]*-1)
            mult_to_v_vector.append(v_scalar_vector[i] * -1)
            mult_to_t_vector.append(t_scalar_vector[i] * -1)

        diagram.quiver(*u_scalar_vector,*v_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*u_scalar_vector,*t_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*v_scalar_vector,*u_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*v_scalar_vector,*t_scalar_vector,color='grey', linewidth=3, arrow_length_ratio=0,linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *u_scalar_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *v_scalar_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')

        diagram.quiver(*mult_vector, *mult_to_t_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_u_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_v_vector, color='grey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')



        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

        self.change_base(diagram,new_base,mult_vector)

    def change_base(self,diagram,new_base,mult_vector):
        """
        Miutan a program felrajzolta az eredeti bazis alapjan a vektorokat, a program az eredovektor es az uj bazis segitsegevel kiszamolja az uj skalarokat.
        Az uj skalarokat úgy kapjuk meg hogy D = T^(-1) * regi_bazis_eredo_vektor
        Ezek a szamok mondjak meg, hogy az uj bazisvektorokat mennyivel kell megszorozni, hogy beloluk osszeadva ugyanazt az eredo vektort osszeadjuk


        :param diagram:     diagram amire rajzoljuk az uj vektorokat
        :param new_base:    az uj bazis ami segitsegevel uj vektorokat kepezunk
        :param mult_vector: az eredeti bazis alapjan kiszamitott eredovektor
        """

        #eredeti eredo vektor
        old_mult=mult_vector

        #kiszamoljuk az uj skalarokat
        v_new = np.linalg.inv(new_base) @ old_mult

        #vektorok elokeszitese
        u_scalar_vector = []
        v_scalar_vector = []
        t_scalar_vector = []

        u_vector=[]
        v_vector=[]
        t_vector=[]

        # skalarok kinyerese a keplet altal kiszamitott eredmenybol
        scalar_a = v_new[0]
        scalar_b = v_new[1]
        scalar_c = v_new[2]

        # 3 vektor kinyerese az uj bazisbol
        for i in range(3):
            u_vector.append(new_base[i][0])
            v_vector.append(new_base[i][1])
            t_vector.append(new_base[i][2])

        # vektorok skalarral valo szorzatanak kiszamitasa
        for i in range(3):
            u_scalar_vector.append(u_vector[i] * scalar_a)
            v_scalar_vector.append(v_vector[i] * scalar_b)
            t_scalar_vector.append(t_vector[i] * scalar_c)

        #origo
        origo = np.zeros(3)

        # uj bazisbol szarmazo eredo vektorok
        diagram.quiver(*origo, *u_vector, color='pink', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *v_vector, color='pink', linewidth=3, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_vector, color='pink', linewidth=3, arrow_length_ratio=0.15)


        # skalar vektorok
        diagram.quiver(*origo, *u_scalar_vector, color='purple', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *v_scalar_vector, color='purple', linewidth=2, arrow_length_ratio=0.15)
        diagram.quiver(*origo, *t_scalar_vector, color='purple', linewidth=2, arrow_length_ratio=0.15)

        mult_vector = []

        #linearis kombinaciobol szarmazo eredo vektor
        for i in range(len(u_vector)):
            mult_vector.append(u_scalar_vector[i] + v_scalar_vector[i] + t_scalar_vector[i])

        # az uj eredo vektor pontjanak kirajzolasa, es koordinatainak kiiratasa
        diagram.scatter(*mult_vector, s=20, color="black")
        diagram.text(*mult_vector,f'({v_new[0]:.2f}, {v_new[1]:.2f}, {v_new[2]:.2f})',fontsize=10,color='black')

        # az uj eredo vektor kirajzolasa
        diagram.quiver(*origo, *mult_vector, color='orange', linewidth=3,linestyle='dashed', arrow_length_ratio=0.15,label='Eredő vektor új bázissal')


        #kiegeszito vektorok
        mult_to_u_vector = []
        mult_to_v_vector = []
        mult_to_t_vector = []

        for i in range(len(u_vector)):
            mult_to_u_vector.append(u_scalar_vector[i] * -1)
            mult_to_v_vector.append(v_scalar_vector[i] * -1)
            mult_to_t_vector.append(t_scalar_vector[i] * -1)

        diagram.quiver(*u_scalar_vector, *v_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*u_scalar_vector, *t_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*v_scalar_vector, *u_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*v_scalar_vector, *t_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *u_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*t_scalar_vector, *v_scalar_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')

        diagram.quiver(*mult_vector, *mult_to_t_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_u_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')
        diagram.quiver(*mult_vector, *mult_to_v_vector, color='darkgrey', linewidth=3, arrow_length_ratio=0,
                       linestyle='dashed')


        # diagram korlatozasanak elokeszitese
        mult_vect_lim=np.array(mult_vector)
        old_mult_lim=np.array(old_mult)
        vector1_lim = np.array(u_scalar_vector)
        vector2_lim = np.array(v_scalar_vector)
        vector3_lim = np.array(t_scalar_vector)

        # diagram korlatozasa
        lim = max(mult_vect_lim.max(),old_mult_lim.max(),new_base.max(),vector1_lim.max(),vector2_lim.max(),vector3_lim.min())
        min_lim = min(mult_vect_lim.min(),old_mult_lim.min(),new_base.min(),vector1_lim.min(),vector2_lim.min(),vector3_lim.min())

        if (lim) < 0:
            lim = 0
        if min_lim > 0:
            min_lim = 0

        diagram.set_xlim(min_lim, lim)
        diagram.set_ylim(min_lim, lim)
        diagram.set_zlim(min_lim, lim)

        #diagram magyarazatainak kiiratasa
        diagram.legend()
        #diagram frissitese
        diagram.figure.canvas.draw()
        diagram.figure.canvas.flush_events()

    def matrix_rank(self,tab,matrix_values,matrix_row,matrix_col):
        """
        A program kiszamolja a kapott matrix rangjat.
        A rang nemlehet nagyobb mint a sor vagy oszlop
        :param tab:             frame amire az informaciokat kiiratjuk
        :param matrix_values:   kapott matrix
        :param matrix_row:      matrix sorainak szama
        :param matrix_col:      matrix oszlopainak szama

        """

        # hiba es eredmeny framek resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()

        self.error_frame=ttk.Frame(tab)

        if self.results is not None:
            self.results.destroy()

        self.results=ttk.LabelFrame(tab,text='Eredmény:')

        #matrix ertekeinek a kinyerese
        matrix = [[None] * matrix_col for i in range(matrix_row)]
        try:
            for i in range(matrix_row):
                for j in range(matrix_col):
                    entry=matrix_values[i][j]
                    ertek=float(entry.get())
                    matrix[i][j]=ertek


        except Exception as e:

            if self.secondary_frame is not None:
                self.secondary_frame.destroy()

            ttk.Label(self.error_frame, text="Kérem adjon meg számokat értékként!", style='Error.TLabel').grid(row=10,
                                                                                                               column=0)

            print(f"    \033[91m-> Sikertelen matrix rang szamolas :{e}\033[0m")
            self.error_frame.grid(row=4, column=0)
            return False


        #matrix rangjanak kiszamolasa
        matrix_mx=np.array(matrix)
        rank=np.linalg.matrix_rank(matrix_mx)

        #eredmeny kiiratasa
        ttk.Label(self.results, text=f"A mátrix rangja: {rank}").grid(row=10, column=0, columnspan=matrix_col)
        self.results.grid(row=5,column=0)

    def linear_equations_solver(self,tab,equation_matrix_entries,result_vector_entries):
        """
        A program kiszamolja a linearis egyenletrendszer megoldasait, ezeket pedig kirajzolja az ablakra.
        Az egyenletek szama egyenlo az ismeretlenek szamaval, ezert Cramer-szabaly segitsegevel oldjuk meg
        :param tab:                     frame amire kiiratjuk az informaciokat/eredmenyeket
        :param equation_matrix_entries: egyenlet matrix
        :param result_vector_entries:   oszlopvektor
        """

        # elozo diagram bezarasa
        plt.close()

        # elozo megoldas resetelese
        if self.results is not None:
            self.results.destroy()

        self.results = ttk.Frame(tab)

        # ertekek kinyerese a beviteli mezokbol, valamint ezek ellenorzese
        equation_values = [[None] * len(row) for row in equation_matrix_entries]
        result_values = []
        for i in range(len(equation_values)):
            for j in range(len(equation_values[i])):
                try:
                    value = float(equation_matrix_entries[i][j].get())
                except Exception as e:
                    ttk.Label(self.results, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen linearis egyenletrendszer szamitas: {e}\033[0m")
                    self.results.grid(row=5, column=0, columnspan=2)
                    return False

                equation_values[i][j] = value

        for i in range(len(result_vector_entries[0])):
            try:
                value = float(result_vector_entries[0][i].get())
            except Exception as e:
                ttk.Label(self.results, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                print(f"    \033[91m-> SSikertelen linearis egyenletrendszer szamitas: {e}\033[0m")
                self.results.grid(row=5, column=0, columnspan=2)
                return False

            result_values.append(value)

        # ertekek NumPy formaba alakitasa
        equation_matrix=np.array(equation_values)
        result_vector=np.array(result_values)

        # egyenlet megoldasa
        try:
            results=np.linalg.solve(equation_matrix,result_vector)

        except np.linalg.LinAlgError:
            ttk.Label(self.results, text="Az egyenlet nem oldható meg (párhuzamos egyenesek)!", style='Error.TLabel').grid(
                row=5, column=0)
            print(f"    \033[91m-> Sikertelen egyenlet megoldás:\033[0m")
            self.results.grid(row=5, column=0, columnspan=2)
            return False






        #diagram tipus eldöntése ismeretlenek szama alapjan
        # ha tobb mint 3 akkor oszlop diagram
        if len(result_values) > 3:

            #diagram meretenek, framejenek, es tipusanak a beallitasa
            fig = plt.figure(figsize=(5, 5))
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=self.results)

            # indexek letrehozasa, attol fuggoen hany ismeretlen van
            indexes = np.arange(len(results))

            # megoldasok felpakolasa a diagramra
            ax.scatter(indexes,results,color='red', s=20, edgecolors='black',zorder=3,label='Megoldások')
            ax.plot(indexes,results,color='black',linestyle='dashed',alpha=0.3,zorder=2)

            # szoveg pakolasa az eredmenyek koordinataihoz
            for i in range(len(results)):
                ax.text(i,results[i],f'{results[i]:.2f}')

            # Megoldasok cimkezese
            x_titles=[f'x{i}' for i in range(len(results))]
            plt.xticks(indexes,x_titles,fontsize=10)

            # axisok elnevezese
            plt.xlabel("Ismeretlenek", fontsize=10)
            plt.ylabel("Értékek", fontsize=10)

            # vizszintes fekete vonal az origobol (negativ ertekek jobban lathatoak legyenek)
            ax.axhline(0, color='black')

            # halo a hatterbe, hogy jobban lathatoak legyenek az ertekek
            ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

            # diagram cime
            ax.set_title(f"{len(equation_values)} ismeretlenes egyenletrendszer megoldásai", fontsize=14)

            #diagram cimkezese
            ax.legend()



        # ha ismeretlenek szama 3 akkor 3D
        elif len(result_values) == 3:

            #diagram merete, frameje, es tipusanak beallitasa
            fig = plt.figure(figsize=(5, 5))
            ax = fig.add_subplot(111,projection='3d')
            canvas = FigureCanvasTkAgg(fig, master=self.results)

            # sikok meretenek beallitasa
            lim =np.abs(results).max()

            s = np.linspace(-lim-5,lim+5, 10)
            t = np.linspace(-lim-5,lim+5, 10)

            #sikok letrehozasa
            X, Y = np.meshgrid(s,t)

            colors = ['blue','green','red']
            # a harom sik kirajzolasa
            for i in range(3):


                a = equation_matrix[i][0]
                b = equation_matrix[i][1]
                c = equation_matrix[i][2]

                d = result_vector[i]

                if c==0:
                    c=1e-9

                # ax+by+cz=d
                Z = (d - a * X - b * Y) / c
                ax.plot_surface(X, Y, Z, alpha=0.5, color=colors[i])

            # 3 sik talalkozasi pontja (a megoldas)
            ax.scatter(*results,color='black',s=20, zorder=3, label=f'Megoldás: ({results[0]:.2f},{results[1]:.2f},{results[2]:.2f})')

            # dimenziok elnevezese
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('3 ismeretlenes egyenletrendszer')

            # magyarazat kiirasa
            ax.legend()

        # ha 2 ismeretlenes, tehat 2D diagramra valo kirajzolas
        else:

            #eredmenyek kinyerese
            x_solution, y_solution = results
            # diagram tipusa, merete, es framejenek a beallitasa
            fig = plt.figure(figsize=(5, 5))
            ax = fig.add_subplot(111)
            canvas = FigureCanvasTkAgg(fig, master=self.results)

            # az egyenes alapja
            x_values = np.linspace(x_solution-5,x_solution+5,100)

            # egyenesek létrehozása es kirajzolasa: ax + by = c => y = (c - ax) / b
            for i in range(2):
                # egyutthatok kinyerese
                a=equation_matrix[i][0]
                b_orig=equation_matrix[i][1]
                c=result_vector[i]

                # 0 val valo osztas kezelese
                if b_orig ==0:
                    b=1e-9
                else:
                    b=b_orig

                # y ertekek kiszamitasa
                y_values = (c - a * x_values) / b

                #egyenes kirajzolasa
                ax.plot(x_values,y_values,label=f'{a}x + {b_orig}y = {c}')

            # metszespont kirajzolasa
            ax.scatter(x_solution,y_solution, color='black', s=20, zorder=3, label=f'Megoldás: ({round(x_solution,2)}, {round(y_solution)})')

            #hatterbeli halo letrehozasa
            ax.grid(True,linestyle="dashed",alpha=0.3)

            #dimenziok elnevezese
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("Az egyenesek metszéspontja")
            # magyarazatok megjelenitese
            ax.legend()

        #diagram kirajzolasa
        canvas.draw()
        canvas.get_tk_widget().grid(row=6,column=0)

        # framek kirajzolasa
        self.results.grid(row=6,column=0)
        tab.grid(row=6,column=0)


