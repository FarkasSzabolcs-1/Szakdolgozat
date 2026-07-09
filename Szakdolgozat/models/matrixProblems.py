import numpy as np
from tkinter import ttk

class Matrixproblems():
    def __init__(self):
        self.results=None
        self.error_frame=None


    def matrix_sum(self,tab,matrix1_entries,matrix2_entries):
        """
        Ket matrix osszeadasa, ha sor es oszlopszam egyenlo. Majd pedig ablakra kiiratasa
        A[aij] + B[bij] = [aij + bij]
        :param tab:             frame amire informaciot iratunk vissza
        :param matrix1_entries: matrix 1
        :param matrix2_entries: matrix 2
        """
        # osszeg matrix elokeszitese
        sum_matrix=[[None] * len(row) for row in matrix1_entries]

        #elozo megoldas torlese ujraszamolas eseten
        if self.results is not None:
            self.results.destroy()

        # frame elokeszitese uj megoldas eseten
        self.results=ttk.LabelFrame(tab,text="Összeadott mátrix")

        # elozo hiba torlese
        if self.error_frame is not None:
            self.error_frame.destroy()

        # esetleges hibara frame letrehozasa
        self.error_frame = ttk.LabelFrame(tab,text='Hiba:')

        #két mátrix összeadása
        # A[aij] + B[bij] = [aij + bij]
        for i in range(len(matrix1_entries)) :
            for j in range(len(matrix1_entries[i])):
                try:
                    value1 = float(matrix1_entries[i][j].get())
                    value2 = float(matrix2_entries[i][j].get())
                    sum_matrix[i][j] = value1 + value2

                except Exception as e:

                    ttk.Label(self.error_frame, text="Hibás értékeket adott meg, kérem ellenőrizze!", style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen matrix osszeadas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False

        # feleslegess .0 eltorlese (mivel float minden)
        for i in range(len(sum_matrix)):
            for j in range(len(sum_matrix[i])):
                if sum_matrix[i][j]==int(sum_matrix[i][j]):
                    sum_matrix[i][j]=int(sum_matrix[i][j])


        # matrix kiiratasa a frame-re
        for i in range(len(sum_matrix)):
            for j in range(len(sum_matrix[i])):
                entry=ttk.Entry(self.results,width=5)
                entry.grid(row=i+1,column=j)
                entry.insert(0,str(sum_matrix[i][j]))

        # megoldas frame megjelenitese
        self.results.grid(row=0,column=0)
        tab.grid(row=5,column=0,columnspan=2)

    def matrix_mult(self,tab,matrix1_entries,matrix2_entries):
        """
        Ket matrix osszeszorzasa, ha matrix1_sor=matrix2_oszlop es matrix1_oszlop=matrix2_sor
        Majd pedig ablakra kiiratasa
        :param tab:             frame amire informaciot iratunk vissza
        :param matrix1_entries: matrix 1
        :param matrix2_entries: matrix 2
        """

        #elozo megoldasok torlese ha van
        if self.results is not None:
            self.results.destroy()

        # uj megoldashoz frame elokeszitese
        self.results=ttk.LabelFrame(tab, text="Összeszorzott mátrix")

        # elozo hiba torlese ha van
        if self.error_frame is not None:
            self.error_frame.destroy()

        # esetleges hibara elokeszules
        self.error_frame = ttk.LabelFrame(tab,text='Hiba:')


        # a ket matrix ertekeinek ellenorzese es kinyerese az entry-kbol
        matrix1_values=[[None] * len(row) for row in matrix1_entries]
        matrix2_values=[[None] * len(row) for row in matrix2_entries]
        for i in range(len(matrix1_entries)) :
            for j in range(len(matrix1_entries[i])):
                try:
                    value=float(matrix1_entries[i][j].get())
                except Exception as e:
                    ttk.Label(self.error_frame, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen matrix szorzas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False
                matrix1_values[i][j]=value

        for i in range(len(matrix2_entries)) :
            for j in range(len(matrix2_entries[i])):
                try:
                    value = float(matrix2_entries[i][j].get())
                except Exception as e:
                    ttk.Label(self.error_frame, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen matrix szorzas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False
                matrix2_values[i][j]=value

        # a ket matrix NumPy kompatibilissa tetele
        matrix1 = np.array(matrix1_values)
        matrix2 = np.array(matrix2_values)

        #osszeszorzas es utana vissza alakitas
        matrix_multed = np.matmul(matrix1, matrix2)

        #vissza alakitas listara, hogy tizedeseket eltudjuk hagyni, ha van
        matrix_mult=matrix_multed.tolist()

        # a ket matrix ellenorzese, ahol lehet INT-re alakitani
        for i in range(len(matrix_mult)):
            for j in range(len(matrix_mult[i])):
                if matrix_mult[i][j]==int(matrix_mult[i][j]):
                    matrix_mult[i][j]=int(matrix_mult[i][j])

        # osszeszorzott matrix kiiratasas a framere
        for i in range(len(matrix_mult)):
            for j in range(len(matrix_mult[i])):
                entry=ttk.Entry(self.results,width=5)
                entry.grid(row=i+1,column=j)
                entry.insert(0,str(matrix_mult[i][j]))

        # eredmenyek megjelenitese
        self.results.grid(row=0,column=0)
        tab.grid(row=5,column=0,columnspan=2)


    def matrix_transpose(self,tab,matrix_entries):
        """
        Matrix transzponalasa -> felcsereljuk a sorait az oszlopaival.
        Majd pedig ablakra kiiratasa
        :param tab:            a frame, amire az informaciokat kiiratjuk
        :param matrix_entries: a matrix amit transzponalunk
        """

        #elozo eredmenyek torlese ha van
        if self.results is not None:
            self.results.destroy()

        # eredmeny kiiratashoz frame elokeszitese
        self.results = ttk.LabelFrame(tab, text="Transzponált mátrix")

        # a matrix ertekeinek tarolasanak felkeszulese
        matrix_values = [[None] * len(row) for row in matrix_entries]

        #elozo hiba torlese ha van
        if self.error_frame is not None:
            self.error_frame.destroy()

        # esetleges hibara felkeszules
        self.error_frame = ttk.LabelFrame(tab,text='Hiba:')

        # ertekek ellenorzese
        for i in range(len(matrix_entries)):
            for j in range(len(matrix_entries[i])):
                try:

                    value = float(matrix_entries[i][j].get())

                except Exception as e:
                    ttk.Label(self.error_frame, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen matrix transzponalas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False

                matrix_values[i][j] = value

        #a mátrix numpy kompatibilisse alakítása
        transposable=np.array(matrix_values)

        #mátrix transzponálása
        matrix_transposed=np.transpose(transposable)

        #vissza alakitas listara
        matrix=matrix_transposed.tolist()

        # a  matrix ellenorzese, ahol lehet INT-re alakitani
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == int(matrix[i][j]):
                    matrix[i][j] = int(matrix[i][j])

        # a megoldas frame-re kiirni a transzponalt matrixot
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                entry = ttk.Entry(self.results, width=5)
                entry.grid(row=i + 1, column=j)
                entry.insert(0, str(matrix[i][j]))

        # frame kirajzolasa az ablakra
        self.results.grid(row=0, column=0)
        tab.grid(row=5, column=0, columnspan=2)

    def matrix_invert(self,tab,matrix_entries):
        """
        Ertekek ellenorzese, majd pedig a matrixot invertaljuk, es kiiratjuk az ablakras
        :param tab:            a frame amire informaciot adunk vissza
        :param matrix_entries: az invertalni kivant matrix
        """
        #elozo megoldas resetelese
        if self.results is not None:
            self.results.destroy()
        self.results = ttk.LabelFrame(tab, text='Invertált mátrix')

        # elozo hiba resetelese
        if self.error_frame is not None:
            self.error_frame.destroy()
        self.error_frame = ttk.LabelFrame(tab,text='Hiba:')

        # matrix ertekeinek kinyeresenek felkeszulese
        matrix_values = [[None] * len(row) for row in matrix_entries]

        # szamitas elott ertek ellenorzes es ertek kinyerese
        for i in range(len(matrix_entries)):
            for j in range(len(matrix_entries[i])):
                try:

                    value = float(matrix_entries[i][j].get())

                except Exception as e:
                    ttk.Label(self.error_frame, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen matrix generalas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False


                matrix_values[i][j] = value

        #előkészítés az invertálásra
        invertable = np.array(matrix_values)

        #mátrix invertálása
        #hiba esetén exception-t dob, és hibaüzenetet ír ki (determináns 0)
        if (np.linalg.det(invertable)!=0):
            try:
                result=np.linalg.inv(invertable)

            except Exception as e:
                ttk.Label(self.error_frame, text="Az alábbi mátrix nem invertálható ",style='Error.TLabel').grid(row=0, column=0)
                print(f"    \033[91m-> Sikertelen matrix invertalas\033[0m")
                self.error_frame.grid(row=0, column=0)
                tab.grid(row=5, column=0, columnspan=2)
                return False
        else:
            ttk.Label(self.error_frame, justify='left', wraplength=350, text="Az alábbi mátrix nem invertálható, mert a determináns nem lehet egyenlő 0-val ", style='Error.TLabel').grid(row=0,column=0)
            print(f"    \033[91m-> Sikertelen matrix invertalas -> determinans nem lehet 0\033[0m")
            self.error_frame.grid(row=0, column=0)
            tab.grid(row=5, column=0, columnspan=2)
            return False

        # eredmeny visszaalakitasa listara
        result_mx=result.tolist()

        # eredmeny formazasa
        for i in range(len(result_mx)):
            for j in range(len(result_mx[i])):
                if result[i][j]==int(result_mx[i][j]):
                    result_mx[i][j]= int(result_mx[i][j])

        # eredmeny kiiratasa
        for i in range(len(result_mx)):
            for j in range(len(result_mx[i])):
                entry = ttk.Entry(self.results, width=5)
                entry.grid(row=i + 1, column=j)
                entry.insert(0, round(result_mx[i][j],2))

        self.results.grid(row=0, column=0)
        tab.grid(row=5, column=0, columnspan=2)

    # matrix determinansanak kiszamolasa
    def matrix_determinant(self,tab,matrix_entries):
        """
        Egy matrix ertekinek ellenorzese, majd pedig determinans szamolasa, es ennek az erteket majd ablakra kiiratasa
        :param tab: frame amire majd az informaciokat iratjuk vissza
        :param matrix_entries: matrix aminek a determinansait kivanjuk kiszamolni
        """
        # elozo framek resetelese
        if self.results is not None:
            self.results.destroy()
        self.results = ttk.LabelFrame(tab,text='Eredmény')

        if self.error_frame is not None:
            self.error_frame.destroy()
        self.error_frame = ttk.LabelFrame(tab,text='Hiba:')

        # ertekek kinyeresenek felkeszulese
        matrix_values = [[None] * len(row) for row in matrix_entries]

        # szamolas elott ellenorzes
        for i in range(len(matrix_entries)):
            for j in range(len(matrix_entries[i])):
                try:

                    value = float(matrix_entries[i][j].get())

                except Exception as e:
                    ttk.Label(self.error_frame, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen determinans szamolas: {e}\033[0m")
                    self.error_frame.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False

                matrix_values[i][j] = value

        #mátrix determináns számításánal előkészítése
        matrix = np.array(matrix_values)
        try:
            # determinans szamolas, majd pedig eredmnény kerekítése kettes tizedes jegyig
            result=round(np.linalg.det(matrix),2)

        except Exception as e:
            ttk.Label(self.error_frame, text="Az alábbi mátrix determinánsa nem számítható ki! ",style='Error.TLabel').grid(row=0, column=0)
            print(f"    \033[91m-> Sikertelen determinans szamolas\033[0m")
            self.error_frame.grid(row=0, column=0)
            tab.grid(row=5, column=0, columnspan=2)
            return False

        # eredmeny kiirasa
        ttk.Label(self.results, text="A mátrix determinánsa: "+str(result)).grid(row=0, column=0)

        # eredmeny frame-jenek a kirajzolasa
        self.results.grid(row=0, column=0)
        tab.grid(row=5, column=0, columnspan=2)

    def matrix_cramer(self,tab,matrix_entries,vector):
        """
        Cramer-szabaly segitsegevel, egy matrix es egy oszlopvektorral kiszamoljuk az ismeretleneket.
        xj = Dj/D
        xj -> ismeretlen
        Dj -> kicserelt matrix determinansa
        D  -> eredeti matrix determinansa
        :param tab:            frame amire informaciokat adunk vissza
        :param matrix_entries: eredeti matrix
        :param vector:         oszlopvektor
        """

        #elozo megoldas vagy hiba resetelese
        if self.results is not None:
            self.results.destroy()

        self.results = ttk.LabelFrame(tab,text='Eredmény:')

        #informaciok kinyerese elotti felkeszules
        matrix_values = [[None] * len(row) for row in matrix_entries]
        vector_values = [[None] * len(row) for row in vector]

        #ellenorizzuk a matrix es vektor ertekeit es kinyerjuk oket
        for i in range(len(matrix_values)):
            for j in range(len(matrix_values[i])):
                try:
                    value = float(matrix_entries[i][j].get())
                except Exception as e:
                    ttk.Label(self.results, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen Cramer-szabaly szamolas: {e}\033[0m")
                    self.results.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False

                matrix_values[i][j] = value

        for i in range(len(vector_values)):
            for j in range(len(vector_values[i])):

                try:
                    value = float(vector[i][j].get())
                except Exception as e:
                    ttk.Label(self.results, text="Hibas értékeket adott meg, kérem ellenőrizze!",style='Error.TLabel').grid(row=4, column=0)
                    print(f"    \033[91m-> Sikertelen Cramer-szabaly szamolas: {e}\033[0m")
                    self.results.grid(row=0, column=0)
                    tab.grid(row=5, column=0, columnspan=2)
                    return False

                vector_values[i][j] = value

        # eredeti matrix determinans szamolasa
        matrix = np.array(matrix_values)
        try:
            matrix_det = round(np.linalg.det(matrix),2)

        except Exception as e:
            ttk.Label(self.results, text="Az alábbi mátrix determinánsa nem lehet egyenlő 0-val! ",style='Error.TLabel').grid(row=0, column=0)
            print(f"    \033[91m-> Sikertelen matrix generalas\033[0m")
            self.results.grid(row=0, column=0)
            tab.grid(row=5, column=0, columnspan=2)
            return False

        #oszloponként végigmegyünk az egységmátrixon és kicseréljük a vektorra
        #matrix_temp => kicserélt mátrix
        for column in range(len(matrix_values)):
            matrix_temp=[[None] * len(row) for row in matrix_entries]
            for i in range(len(matrix_values)):
                for j in range(len(matrix_values[i])):
                    if(column==j):
                        matrix_temp[i][j]=vector_values[0][i]
                    else:
                        matrix_temp[i][j]=matrix_values[i][j]

            #az ideiglenes mátrix felkészítése determináns számolásra
            temporary=np.array(matrix_temp)

            #ismeretlen számolás az xj = Dj/D képlet alapján
            result_cramer=round(np.linalg.det(temporary)/matrix_det,2)

            #ismeretlenek ablakba való kiíratása, a,b,c... nevekként
            ttk.Label(self.results, text=chr(97+column)+" = " + str(result_cramer)).grid(row=0+column, column=0,sticky='w')

        #eredmeny ablak kiiratasa
        self.results.grid(row=0, column=0)
        tab.grid(row=5, column=0, columnspan=2)