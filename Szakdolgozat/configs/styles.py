from tkinter import ttk

def loadConfigs():
    """
    A rendszer induláskor betölti a style-okat a különböző ttk elemekhez
    """
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 11), padding=0)
    style.configure("Title.TLabel",font=("Segoe UI", 25),padding=0)
    style.configure("TLabel", font=("Segoe UI", 11), padding=0)
    style.configure('Back.TButton',font=("Segoe UI", 11,),foreground='red')
    style.configure('Error.TLabel', font=("Segoe UI", 11,), foreground='red',anchor='center')
