# ui/crear_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
from models_usuarios import create_user, update_user

class CrearUsuarioWindow:
    def __init__(self, parent, on_save, user=None):
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
            for i, val in enumerate(user[1:]):  # skip ID
                self.entries[i].insert(0, val)

        btn_text = "Actualizar" if user else "Crear"
        ttk.Button(self.top, text=btn_text, command=self.save_user).grid(row=5, column=0, columnspan=2, pady=10)

    def save_user(self):
        data = [e.get().strip() for e in self.entries]
        if not data[0]:  # Nombre es obligatorio
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
