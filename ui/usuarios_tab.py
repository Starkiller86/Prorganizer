"""
usuarios_tab.py - Pestaña de interfaz para gestionar usuarios.

Permite visualizar, agregar, editar y eliminar usuarios desde una tabla (Treeview).
Es parte de la capa Vista en la arquitectura MVC.
"""

from tkinter import ttk
from ui.crear_usuario import CrearUsuarioWindow
from models_usuarios import get_all_users, delete_user
import tkinter as tk
from tkinter import messagebox

class UsuariosTab:
    """
    Clase que representa la pestaña de 'Usuarios' dentro del sistema.
    Proporciona una vista para administrar usuarios mediante una interfaz gráfica.
    """

    def __init__(self, notebook):
        """
        Inicializa la pestaña de usuarios y construye la interfaz.

        Args:
            notebook (ttk.Notebook): Contenedor de pestañas de la aplicación.
        """
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Usuarios")
        self.build_ui()

    def build_ui(self):
        """
        Crea y configura todos los elementos gráficos de la pestaña.
        """
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        create_button = ttk.Button(top_frame, text="Agregar Usuario", command=self.open_create_window)
        create_button.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Nombre", "Apellido", "Teléfono", "Correo"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Menú contextual (clic derecho)
        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Editar", command=self.edit_user)
        self.menu.add_command(label="Eliminar", command=self.delete_user)
        self.tree.bind("<Button-3>", self.show_menu)

        self.load_users()

    def show_menu(self, event):
        """
        Muestra el menú contextual al hacer clic derecho sobre una fila.
        """
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.menu.post(event.x_root, event.y_root)

    def load_users(self):
        """
        Carga todos los usuarios desde la base de datos y los muestra en la tabla.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        for user in get_all_users():
            self.tree.insert("", "end", values=(user["id"], user["nombre"], user["apellido"], user["telefono"], user["correo"]))

    def open_create_window(self):
        """
        Abre la ventana para crear un nuevo usuario.
        """
        CrearUsuarioWindow(self.frame, on_save=self.load_users)

    def edit_user(self):
        """
        Abre la ventana de edición con los datos del usuario seleccionado.
        """
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        CrearUsuarioWindow(self.frame, on_save=self.load_users, user=values)

    def delete_user(self):
        """
        Elimina el usuario seleccionado después de confirmación.
        """
        selected = self.tree.selection()
        if not selected:
            return
        user_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirmar", "¿Deseas eliminar este usuario?")
        if confirm:
            delete_user(user_id)
            self.load_users()
