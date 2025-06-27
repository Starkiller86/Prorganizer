"""
main.py - Punto de entrada de la aplicación Progranizer.

Este módulo inicia la interfaz principal del sistema de gestión de tareas.
Utiliza ttkbootstrap para estilizar la GUI y organiza las vistas en pestañas.

Pertenece al Controlador en la arquitectura MVC.
"""

import tkinter as tk
import ttkbootstrap as tb

from ui.principal_tab import PrincipalTab
from ui.lista_tab import ListaTab
from ui.usuarios_tab import UsuariosTab

class GestorTareas:
    """
    Clase principal de la aplicación. Construye la ventana base
    y agrega las pestañas de navegación: Principal, Lista y Usuarios.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal con estilo y navegación por pestañas.

        Args:
            root (tk.Tk): Ventana principal del sistema.
        """
        self.root = root
        self.root.title("Progranizer")
        self.root.geometry("1200x800")
        self.root.iconbitmap("assets/progranizer.ico")

        # Estilo bootstrap
        self.style = tb.Style(theme="minty")

        # Crear el contenedor de pestañas
        self.tab_control = tb.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")

        # Agregar cada pestaña desde su clase correspondiente (Vista)
        PrincipalTab(self.tab_control)
        ListaTab(self.tab_control)
        UsuariosTab(self.tab_control)

if __name__ == "__main__":
    """
    Inicia la aplicación con el tema 'flatly' y crea una instancia de GestorTareas.
    """
    root = tb.Window(themename="flatly")
    app = GestorTareas(root)
    root.mainloop()
