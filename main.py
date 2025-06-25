import tkinter as tk
import ttkbootstrap as tb

from ui.principal_tab import PrincipalTab
from ui.lista_tab import ListaTab
from ui.usuarios_tab import UsuariosTab

class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Progranizer")
        self.root.geometry("1200x800")
        self.root.iconbitmap("assets/progranizer.ico")

        # Estilo bootstrap
        self.style = tb.Style(theme="flatly")

        # Crear el contenedor de pestañas
        self.tab_control = tb.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Agregar cada pestaña desde su clase
        PrincipalTab(self.tab_control)
        ListaTab(self.tab_control)
        UsuariosTab(self.tab_control)

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = GestorTareas(root)
    root.mainloop()
