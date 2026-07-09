from controllers.solutionController import Solutioncontroller
class ScreenController:

    def __init__(self,container_frame):
        # a fo ablak frame-je
        self.container=container_frame

        # ahol az ablakok objektumjait fogjuk tarolni
        self.screens={}

        #jelenlegi ablak
        self.current_screen=None
        #root kinyerese a fo framebol
        self.root=container_frame.winfo_toplevel()

        #solver_handler letrehozasa, ami majd a problemak megoldasaban segit
        self.solver_handler=Solutioncontroller()

        #elemek kozepre igazitasa
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def load_screens(self, screen_class,type):
        """
        Betoltuk az ablakok osztalyait egy self.screens[] listába gyors eléréshez
        Megadjuk a framet amihez kapcsolodik es amin megkell jelenjen, valamint a controllert, es tipustol fuggoen, akar a solver_handler-t
        :param screen_class: Az ablak file-ban szereplo osztaly neve
        :param type: problem-> problema ablak
                     menu   -> navigacios menu
        """
        # az osztaly neve
        name =screen_class.__name__

        # ablak letrehozasa tipustol fuggoen
        if type=='problem':
            screen = screen_class(parent=self.container, controller=self,solver_handler=self.solver_handler)
        else:
            screen = screen_class(parent=self.container, controller=self)

        # ablak ideiglenes elhelyezese
        screen.grid(row=0, column=0, sticky="nsew")
        screen.grid_remove()

        # ablak feltoltese a listaba
        self.screens[name] = screen

        # console feedback
        print(f"    \033[92m-> {name} sikeresen betoltve\033[0m")

    def show_screen(self, screen_name):
        """
        Ablak megjelenitese nev alapjan. Ablakcimet cserel, eltunteni az aktualis ablakot, majd pedig megjeleniti az ujat
        :param screen_name: ablak neve (pl. "Matrixmenu")
        """

        #cim cserelese
        self.change_title(screen_name)

        #aktualis ablak eltuntetese
        if self.current_screen:
            self.current_screen.grid_remove()

        #uj ablak megjelenitese, es aktualis ablakka tevese
        screen = self.screens[screen_name]
        screen.grid()
        self.current_screen = screen

    def change_title(self,screen_name):
        """
        ablak címek cserélése új ablak megnyitása esetén, nev alapjan

        :param screen_name: pl. ("Matrixmenu")
        """
        match(screen_name):
            case"Mainmenu":
                self.root.title("Főmenü")
            case "Problemsmenu":
                self.root.title("Probléma navigáció")
            # matrixok
            case "Matrixmenu":
                self.root.title("Mátrix problémák bemutatása")
            case "Matrixsum":
                self.root.title("Mátrixok összeadás")
            case "Matrixmult":
                self.root.title("Mátrixok szorzása")
            case "Matrixtranspose":
                self.root.title("Mátrix transzponálása")
            case "Matrixidentity":
                self.root.title("Egységmátrix")
            case "Matrixtriangle":
                self.root.title("Háromszögmátrix")
            case "Matrixdeterminant":
                self.root.title("Mátrix determinánsa")
            case "Matrixinvert":
                self.root.title("Inverz mátrix")
            case "Matrixcramer":
                self.root.title("Cramer-szabály")

            # vektorok
            case "Vectormenu":
                self.root.title("Vektor problémák bemutatása")
            case "Vectorlenght":
                self.root.title("Vektor normája")
            case "Vectorsum":
                self.root.title("Vektorok összeadása")
            case "Vectormult":
                self.root.title("Skalárral való szorzás")
            case "Vectorlinearcombination":
                self.root.title("Lineáris kombináció")
            case "Vectorscalarmult":
                self.root.title("Két vektor skaláris szorzata")
            case "Vectorialmult":
                self.root.title("Vektorok vektoriális szorzata")
            case "Trianglesolution":
                self.root.title("Háromszög megoldás")

            # vektor terek
            case "Vectorspacemenu":
                self.root.title("Vektorterek bemutatása")
            case "Vectorspaces":
                self.root.title("Vektorterek")
            case "Vectorsubspaces":
                self.root.title("Alterek")
            case "Linearindependence":
                self.root.title("Lineáris függetlenség")
            case "Bases":
                self.root.title("Bázis")
            case "Basetransformation":
                self.root.title("Bázis transzformáció")
            case "Matrixrank":
                self.root.title("Mátrix rangja")
            case "Linearequations":
                self.root.title("Lineáris egyenletrendszerek")

            # linearis algebra a mindennapokban
            case "Realproblemsmenu":
                self.root.title("Lineáris algebra a mindennapokban")
            case "Imageprocessing":
                self.root.title("Digitális képfeldolgozás")
            case "Linearprogramming":
                self.root.title("Lineáris programozás")
            case "Portfoliooptimization":
                self.root.title("Portfólió optimalizálás")

