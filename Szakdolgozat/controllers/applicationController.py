from configs import styles
from controllers.screenController import ScreenController
import importlib
from pathlib import Path
import tkinter as tk

class ApplicationController:
    def __init__(self):
        # a root létrehozása a tkinter ablakokhoz
        self.root = tk.Tk()

        # meretezes beallitasa
        self.root.resizable(False, False)
        self.root.minsize(800, 500)

        # fo container letrehozasa -> majd oroklodik az osszes ablakhoz
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        #a screencontroller letrehozasa, ami majd ezeket fogja kezelni
        self.screen_controller = ScreenController(self.container)

        #ablakok betoltese a rendszerbe
        self.auto_load_screens()
        self.auto_load_problems()

    #alap ablakok betoltese gyors elereshez
    def auto_load_screens(self):
        """
        views mappaban levo osszes Python file betoltese (az osszes ablak kell legyen).
        A program vegignezi a views mappat, es megkeresi az osszes .py kiterjesztesu file-t.
        Majd a file nevet kicsit alakitva (pl. matrixCramer -> Matrixcramer) kulon megjegyezzuk.
        Ezutan a program megprobalja be importalni dinamiukusan az adott filebol a benne szereplo osztalyt.
        (pl. from views.matrixCramer import Matrixcramer)

        Ha betudja importalni es letezik a filen belul az adott osztaly, akkor ezt az osztalyt mint egy objektum megfogjuk,
        es tovabb adjuk a screencontrollernek, hogy betoltse gyors eleresre.

        """
        # console feedback
        print(f"->Alap menük betöltése")
        # views mappa eleresi utvonala
        view_dir = "views"
        view_path = Path(view_dir)

        # views mappan belul minden .py filet megnezni
        for file_path in view_path.glob("*.py"):
            # file nevenek kinyerese (kiterjesztes nelkul), es egy nev modositas class kereseshez
            module_name = file_path.stem
            class_name = module_name.capitalize()

            #megprobaljuk beimportalni az adott filet
            try:
                module = importlib.import_module(f"{view_dir}.{module_name}")

                #ha letezik az adott beimportalt fileban az osztaly, akkor objektumkent tovabbadjuk a screen_controllernek hogy betoltse
                if (hasattr(module, class_name)):
                    screen_class = getattr(module, class_name)
                    self.screen_controller.load_screens(screen_class,'menu')
            except Exception as e:
                print(f"    \033[91m-> {class_name} sikertelenül betoltve: {e}\033[0m")

    def auto_load_problems(self):
        """
        pontosan ugyanazt a feladatot latja el mint az auto_load_screens(), csak nem a views mappan van a hangsuly, hanem a benne szereplo almappakon,
        amikben a problemak rendszerezve vannak.
        """

        # a problemak ketegorizalt mappai
        problem_folders = ['matrix', 'vector','vector_spaces','real_problems']
        base_folder = "views"

        # minden mappat atnezunk
        for problem_folder in problem_folders:

            #console feedback
            print(f"-> {problem_folder} problémák betöltése")

            # belelepunk ezekbe az almappakba
            problems_folder = f"{base_folder}.{problem_folder}"
            view_dir = Path(base_folder) / problem_folder

            # megnezzuk az adott mappa .py filejait
            for file_path in view_dir.glob("*.py"):

                #kinyerjuk a nevet, csinalunk egy modositott masolatot
                module_name = file_path.stem
                class_name = module_name.capitalize()

                #beimportalashoz osszefuzzuk a mappa nevet a file nevevel
                full_name = f"{problems_folder}.{module_name}"
                try:
                    # megprobaljuk beimportalni az adott filet
                    module = importlib.import_module(full_name)

                    #ha letezik az adott fileon belul az osztaly, akkor objektumkent tovabbadjuk a screen_controller-nek
                    if (hasattr(module, class_name)):
                        screen_class = getattr(module, class_name)
                        self.screen_controller.load_screens(screen_class,'problem')
                except Exception as e:
                    print(f"    \033[91m-> {class_name} sikertelenül betoltve: {e}\033[0m")

    def start(self):
        """
        Program indulasakor megjelenitjuk a fomenut (mar bevan toltve gyors elereshez)
        Betolti a stilusokat a ttk elemekhez, majd elinditja az ablakot amig a felhasznalo be nem zarja
        """
        self.screen_controller.show_screen("Mainmenu")
        styles.loadConfigs()
        self.root.mainloop()
