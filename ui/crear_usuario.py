"""
crear_usuario.py - Ventana emergente para crear o editar usuarios.

Define la clase CrearUsuarioWindow que permite agregar o actualizar usuarios
mediante una interfaz gráfica. Forma parte del Controlador en la arquitectura MVC.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models_usuarios import create_user, update_user

class CrearUsuarioWindow:
    """
    Ventana modal para crear o editar usuarios.

    Utiliza herencia implícita de `tk.Toplevel`.
    Emplea polimorfismo en `save_user` para diferenciar entre creación y edición.
    """

    def __init__(self, parent, on_save, user=None):
        """
        Inicializa la ventana de creación o edición de usuario.

        Args:
            parent (tk.Widget): Ventana padre.
            on_save (function): Función a ejecutar al guardar.
            user (tuple, optional): Usuario existente a editar.
        """
        self.top = tk.Toplevel(parent)
        self.top.title("Editar Usuario" if user else "Agregar Usuario")
        self.top.grab_set()

        self.on_save = on_save
        self.user = user

        labels = ["Nombre", "Apellido", "Teléfono", "Correo"]
        self.entries = []

        for i, label in enumerate(labels):
            ttk.Label(self.top, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.top)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        if user:
            for i, val in enumerate(user[1:]):  # Saltar ID
                self.entries[i].insert(0, val)

        btn_text = "Actualizar" if user else "Crear"
        ttk.Button(self.top, text=btn_text, command=self.save_user).grid(row=5, column=0, columnspan=2, pady=10)

    def save_user(self):
        """
        Guarda el usuario nuevo o actualizado. Valida que el nombre no esté vacío.
        """
        data = [e.get().strip() for e in self.entries]
        if not data[0]:  # Validar nombre obligatorio
            messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
            return

        try:
            if self.user:
                update_user(self.user[0], data)
            else:
                create_user(data)
            self.on_save()
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
