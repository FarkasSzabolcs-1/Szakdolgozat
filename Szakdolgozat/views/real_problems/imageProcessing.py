import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import filedialog
from PIL import Image,ImageTk
import numpy as np


class Imageprocessing(tk.Frame):
    def __init__(self, parent, controller,solver_handler):
        super().__init__(parent)
        self.controller = controller
        self.solver_handler=solver_handler
        self.create_screen()


    def create_screen(self):
        """
        ablak megnyitasakor az alap mezoket es cimeket betolti, letrehozza a tabokat es felkesziti a hasznalatra
        """
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Digitális képfeldolgozás", style='Title.TLabel').grid(row=0, column=0)
        ttk.Button(self, text="Vissza", style='Back.TButton',
                   command=lambda: self.controller.show_screen("Realproblemsmenu")).grid(row=1, column=0, sticky="w")
        title_frame.grid(row=0, column=0)
        # tabcontrol létrehozása a generálási módszerek, valamint a tulajdonságok elkülönítéséhez

        self.tabcontrol = ttk.Notebook(self)
        self.tabcontrol.grid(row=2, column=0,sticky='ew')

        # frame-k létrehozása a két generálási módszerhez
        self.pelda_adatok = ttk.Frame(self.tabcontrol)
        self.tulajdonsagok = ttk.Frame(self.tabcontrol)

        # tabcontrol-hoz hozzáadása ezeknek a frameknek
        self.tabcontrol.add(self.pelda_adatok, text="Ditigitális képfeldolgozás")
        self.tabcontrol.add(self.tulajdonsagok, text="Tulajdonságok")

        # meghívjuk mindketto tabot
        self.build_example_datas()
        self.show_rules()

        # editor frame elokeszitese
        self.editor = None

        # eredeti kep es egy masolat peldany elokeszitese
        self.original_image = None
        self.image = None

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
                  text=f'-Digitális képfeldolgozás: A program képfeldolgozó része').grid(row=0, column=0, sticky='we')
        ttk.Label(general_rules, justify='left', wraplength=800,
                  text=f'-A program csakis PNG, JPEG, és PNG formátumokat fogad el, valamint csakis PNG-ben lehet képeket lementeni módosítás után').grid(row=2, column=0, sticky='we')

        math_rules = ttk.LabelFrame(tab, text='Digitális képfeldolgozás')

        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A képek egy m x n mérettel rendelkező mátrixok, és minden elem egy színt tartalmaz (színes képek esetében 3-szor (RGB)), amik 0 és 255 között helyezkednek el.').grid(
            row=0, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'-A program a képet a következőképpen manipulálhatja:').grid(
            row=1, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -Negatívvá tétel: 255-ből kivonjuk a kép színeit.').grid(
            row=3, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -Szürkítés: A luminancia módszer alapján a képet fekete-fehérré változtatjuk (2.299*R + 0.587*G + 0.114*B)').grid(
            row=4, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -Vízszintes/Függőleges tükrözés: A kép mátrixának a sorainak/oszlopainak a sorrendjét megfordítjuk.').grid(
            row=5, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -RGB értékek hozzáadása: A pixelek RGB értékeihez hozzáadjuk a megfelelő értékeket.').grid(
            row=6, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -Szaturálás: Vesszük a fekete-fehér mását, ezután az eredeti színes és a szürke kép közötti különbséget kiszámoljuk, majd ezt a tiszta színinformációt megszorozzuk a kívánt szaturáció mértékével, és hozzáadjuk az alap szürke képhez.').grid(
            row=7, column=0, sticky='we')
        ttk.Label(math_rules, justify='left', wraplength=800,
                  text=f'   -Módosított kép lementése').grid(
            row=8, column=0, sticky='we')

        general_rules.grid(row=0, column=0, sticky='nsew')
        general_rules.columnconfigure(0, weight=1)
        math_rules.grid(row=1, column=0, sticky='nsew')
        math_rules.columnconfigure(0, weight=1)



    def build_example_datas(self):
        """
        Kep kivalasztasa ablak megjelenitese
        """
        tab = self.pelda_adatok
        tab.columnconfigure(0,weight=1)
        main_grid = ttk.Frame(tab, borderwidth=1, relief='solid')
        block1 = ttk.Frame(main_grid, borderwidth=1, relief='solid')
        ttk.Label(block1, text="Kép Feldolgozás").grid(row=0, column=0, columnspan=2)
        block1.grid(row=2, column=0,columnspan=2,sticky='n')

        main_grid.grid(row=0, column=0,columnspan=2)


        ttk.Button(block1, text="Kép feltöltése", width=25,
                   command=lambda: self.upload_image()).grid(row=8, column=0, columnspan=2)


    def upload_image(self):
        """
        A felhasznalo kivalasztja a kepet, majd utana az eleresi utvonal alapjan a kep megnyitodik
        RGB tipussa konvertaljuk, majd pedig meretet adunk neki.
        Lementjuk az eredeti kepet, es masolatot keszitunk, majd megnyilik az editor
        """

        #megengedett kep formatumok
        file_types = [('Image files','*.png;*.jpg;*.jpeg')]

        # kep eleresi utvonal kinyerese kep kivalasztasa utan
        path = tk.filedialog.askopenfilename(filetypes=file_types)

        # ha valasztottunk kepet akkor megnyitjuk, atkonvertaljuk es kimentjuk, valamint megnyitjuk az editort
        if path:

            # elozo kep torlese ha volt
            if self.image is not None:
                self.image = None

            # kep megnyitasa es RGB tipussa konvertalasa
            img = Image.open(path).convert("RGB")

            # kep meretenek beallitasa
            img.thumbnail((500,500))

            #eredeti kep kimentese (ezt modositjuk az eszkozokkel)
            self.original_image = img

            # masolat keszitese a biztonsagos editeleshez
            self.image = img.copy()

            #editor megnyitasa
            self.image_editor()


    def image_editor(self):
        """
        Kep valasztasa utan megnyilik az editor, ahol a bal oldalon szereplo kepet kepesek vagyunk manipulalni,
        a jobb oldalon talalhato eszkozokkel.
        A vegen pedig kepesek vagyunk kimenteni a kepet ahova szeretnenk
        :return:
        """

        # editor reset
        if self.editor is not None:
            self.editor.destroy()

        self.editor = ttk.Labelframe(self.pelda_adatok, text='Kép Szerkesztő')

        #eszkozok elokeszitese
        self.image_frame = ttk.Labelframe(self.editor, text='Kép előnézet')
        self.editor_tools = ttk.Labelframe(self.editor, text='Eszközök')

        invert_frame = ttk.Labelframe(self.editor_tools, text='Tükrözés')

        # kep elonezet
        self.image_panel = Label(self.image_frame)
        self.image_panel.grid(row=2,column=0)

        # kep negativva tetele gomb
        ttk.Button(self.editor_tools, text="Kép negatívvá tétele", width=25,
                   command=lambda: self.negative_image()).grid(row=1, column=0,columnspan=2)

        # vizszintes tukrozes gomb
        ttk.Button(invert_frame, text="Vízszintes tükrözés", width=12,
                   command=lambda: self.invert_image_horizontal()).grid(row=3, column=0)

        # fuggoleges tukrozes gomb
        ttk.Button(invert_frame, text="Függőleges tükrözés", width=12,
                   command=lambda: self.invert_image_vertical()).grid(row=3, column=1)


        # RGB ertek hozzaado skalak letrehozasa
        rgb_slide_frame = ttk.Labelframe(self.editor_tools,text = "RGB értékek változtatása")
        r_frame = ttk.Labelframe(rgb_slide_frame,text='Red')
        r_slider = (ttk.Scale(r_frame,from_=0,to=255))
        r_slider.grid(row=0,column=0)

        g_frame = ttk.Labelframe(rgb_slide_frame, text='Green')
        g_slider = ttk.Scale(g_frame, from_=0, to=255)
        g_slider.grid(row=1, column=0)


        b_frame = ttk.Labelframe(rgb_slide_frame, text='Blue')
        b_slider = ttk.Scale(b_frame, from_=0, to=255)
        b_slider.grid(row=2, column=0)

        # skalak beallitasa utan RGB ertekeket ad a kephez
        ttk.Button(rgb_slide_frame,text='RGB értékek cserélése',command = lambda :self.rgb_change(r_slider,g_slider,b_slider)).grid(row=4,column=0)

        # kep fekete-feherre valtoztatasa
        ttk.Button(self.editor_tools,text='Szürkítés',width=25,command=lambda:self.gray_scaling()).grid(row=4,column=0)

        # kep szaturalas
        saturation_frame = ttk.LabelFrame(self.editor_tools,text= 'Szaturáció')
        # szaturacio skala
        saturation_slider = ttk.Scale(saturation_frame,from_=0, to = 200)
        saturation_slider.grid(row=0,column=0)

        # a kepet szaturaljuk megnyomaskor
        ttk.Button(saturation_frame,text='Szaturálás',command=lambda:self.saturation(saturation_slider)).grid(row=1,column=0)

        saturation_frame.grid(row=5,column=0)

        # kep kimentese
        ttk.Button(self.editor_tools,text='Kép mentése',command=lambda:self.save_image()).grid(row=6,column=0)

        # kep manipulalo framek elhelyezese
        r_frame.grid(row=0,column=0)
        g_frame.grid(row=1, column=0)
        b_frame.grid(row=2, column=0)

        invert_frame.grid(row=2,column=0)
        rgb_slide_frame.grid(row=3, column=0)

        # kep megjelenitese az elonezetben
        self.display_img(self.image)

        # tovabbi eszkozok megjelenitese
        self.editor.grid(row=8,column=0,columnspan=3)
        self.image_frame.grid(row=0,column=0)
        self.editor_tools.grid(row=0,column=3,sticky='n')


    def display_img(self,img):
        """
        A program megkap egy kep verziot amit kicserel az aktualis kep valtozoval,
        majd pedig PhotoImage objektumma valtoztatjuk es kicsereljuk az elonezetben szereplo kepet
        :param img: kep
        """
        # aktualis kep mentese
        self.image = img
        #Tkinter kompatibilissa tesszuk a kepet
        self.pic = ImageTk.PhotoImage(self.image)
        #kicsereljuk az elonezetben szereplo kepet
        self.image_panel.configure(image = self.pic)

    def negative_image(self):
        """
        A program a kepet negativva teszi ugy, hogy matrix formara alakitja, majd pedig 255-bol kivonja a pixelek erteket,
        visszaalakitjuk keppe a matrixot es kirakjuk elonezetbe
        :return:
        """
        # manipulálhatóvá tenni a képet (matrix formara alakitas)
        data = np.array(self.image)

        # kivonunk 255-ből az adott pixel értékét (az összes pixelre)
        negative_data = 255 - data

        # kep visszaalakitasa, valamint biztosítjuk, hogy a kép formátuma ne sérüljön (0-255 közötti számok)
        negative_img = Image.fromarray(negative_data.astype('uint8'))

        #kép megjelenítése az előnézethez
        self.original_image = negative_img
        self.display_img(self.original_image)

    def invert_image_horizontal(self):
        """
        A program a kep matrixaban levo sorok sorrendjet megforditja, igy letrehozva a tukrozes effektjet,
        majd pedig vissza alakitja es elonezetbe helyezi
        """
        # manipulalhatova teves
        data = np.array(self.image)

        # kép vízszintes tükrözése
        horizontal_invert_data = np.flip(data,axis=1)

        # kep visszaalakitasa, valamint biztosítjuk, hogy a kép formátuma ne sérüljön (0-255 közötti számok)
        horizontal_invert = Image.fromarray(horizontal_invert_data.astype('uint8'))

        # az eredeti kepet amit editelunk kicsereljuk es megjelenitjuk elonezetben
        self.original_image = horizontal_invert
        self.display_img(self.original_image)

    def invert_image_vertical(self):
        """
        A program a kep matrixaban levo oszlopok sorrendjet megforditja, igy letrehozva a tukrozes effektjet,
        majd pedig vissza alakitja es elonezetbe helyezi
        """
        # manipulalhatova alakitas
        data = np.array(self.image)

        # oszlopok sorrendjenek megforditasa
        vertical_invert_data = np.flip(data,axis=0)

        # kep visszaalakitasa, valamint biztosítjuk, hogy a kép formátuma ne sérüljön (0-255 közötti számok)
        vertical_invert = Image.fromarray(vertical_invert_data.astype('uint8'))

        self.original_image = vertical_invert
        self.display_img(self.original_image)

    def rgb_change(self,r,g,b):
        """
        A program a kep osszes pixelehez a skalak kivalasztott ertekeinek megfeleloen megnoveli az erteket
        Ezutan a program visszaalakitja keppe es megjeleniti elonezetben
        :param r:   R skala erteke (piros)
        :param g:   G skala erteke (Zold)
        :param b:   B skala erteke (Kek)
        """

        # rgb szinek kinyerese
        red= float(r.get())
        green= float(g.get())
        blue= float(b.get())

        # kep modosithatova tevese
        # engedjuk hogy a kep 255-nel tobb legyen
        data = np.array(self.original_image).astype(np.float32)

        # RGB színcsatornákhoz szín hozzáadása
        data[:, :, 0] += red
        data[:, :, 1] += green
        data[:, :, 2] += blue

        # Ertekek rendbe rakasa
        new_data =np.clip(data,0,255).astype('uint8')

        #kep visszaallitasa matrixbol Pillow kep objektumma
        new_img = Image.fromarray(new_data)

        # kep elonezetbe helyezese
        self.display_img(new_img)

    def gray_scaling(self):
        """
        A program az aktualis kepet fekete-feher keppe alakitja a luminancia modszerevel,
        mivel az emberi szem kulonbozo szinekre kulonbozo erzekenyseggel reagal, ezert sulyozzuk oket
        BT.601 szabvany

        :return:
        """

        # kép manipulálhatóvá tétele
        # engedjuk hogy a kep 255-nel tobb legyen
        data = np.array(self.original_image).astype(np.float32)

        # luminancia módszerrel szürkítés 0.299*R + 0.587*G + 0.114*B
        gray_scale =  0.299 * data[:, :, 0] + 0.587 * data[:, :, 1] + 0.114 * data[:, :, 2]

        # a kapott szürkített értéket háromszorozzuk és egymásra pakoljuk RGB pixel formára
        grayed_data = np.stack([gray_scale] * 3, axis=-1)

        #visszaalakítjuk, levágjuk a határokon túli értékeket, és megjelenítjük
        new_data=np.clip(grayed_data,0,255).astype('uint8')
        new_img = Image.fromarray(new_data)

        self.display_img(new_img)


    def saturation(self,sat_slider):
        """
        A program a kepet szaturalja a szaturacio csuszka alapjan.
        A program eloszor szurkiti a kepet,masolatot csinal belole
        Ezutan manipulalhatova alakitjuk a kepet hiszen szurke kep nem RGB kompatibilis
        A szaturalt kepet kiszamoljuk ugy, hogy:
        szurke_kep + szaturalt_szazalekk * ( eredeti_kep - szurke kep)
                                           ( ez tiszta szin informacio)
        Ezutan a program vissza alakitja a matrixkot keppe es megjeleniti
        :param sat_slider:
        :return:
        """
        # élénkség csúszkából kapott érték
        sat_value = float(sat_slider.get()) /100

        # kép manipulálhatóvá tétele
        data = np.array(self.original_image).astype(np.float32)

        # luminancia módszerrel szürkítés 0.299*R + 0.587*G + 0.114*B
        gray_base = data[:, :, 0] * 0.299 + 0.587 * data[:, :, 1] + 0.114 *data[:, :, 2]

        # a szürke képet manipulálhatóvá alakítjuk
        gray_rgb_layers=np.stack([gray_base]*3,axis=-1)

        # az új élénkített képet kiszámoljuk gray_value + sat_value * (original_img - gray_value)
        saturated_data = gray_rgb_layers + sat_value * (data - gray_rgb_layers)

        # kép visszaalakítása és megjelenítése
        new_data = np.clip(saturated_data, 0, 255).astype('uint8')
        new_img = Image.fromarray(new_data)
        self.display_img(new_img)

    def save_image(self):
        """
        A gomb megnyomasaval megjelenik a Tkinter file navigalo es kivalasszuk hova szeretnenk a kepet lemeteni

        """
        # kep tipus beallitasa
        file_types = [('PNG Fájl', '*.png')]
        # kivalasztott mentesi utvonal megszerzese
        path = tk.filedialog.asksaveasfilename(defaultextension='.png',filetypes=file_types,title='Kép mentése másként')

        # ha kivalasztottuk akkor a kepet lementjuk es visszajelzesi uzenetet adunk
        if path:
            self.image.save(path)
            ttk.Label(self.editor_tools,text='Kép sikeresen lementve').grid(row=7,column=0)

