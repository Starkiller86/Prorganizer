"""
crear_tarea.py - Ventana emergente para crear o editar tareas.

Este módulo define la clase CrearTareaWindow, que se utiliza para gestionar
la interfaz de usuario y la lógica para crear o editar una tarea en el sistema.

Forma parte de la capa Controlador en la arquitectura MVC.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models import create_task, update_task
from models_usuarios import get_all_users

class CrearTareaWindow:
    """
    Ventana modal que permite al usuario crear o editar una tarea.

    Aplica herencia implícita al usar `tk.Toplevel` como ventana secundaria.
    Utiliza polimorfismo en `save_task`, donde el comportamiento depende de si se trata
    de una tarea nueva o existente.
    """

    def __init__(self, parent, on_save=None, task=None):
        """
        Constructor de la ventana.

        Args:
            parent (tk.Widget): Ventana padre.
            on_save (function, optional): Función a ejecutar al guardar.
            task (tuple, optional): Datos de la tarea si se está editando.
        """
        self.task = task
        self.on_save = on_save
        self.window = tk.Toplevel(parent)
        self.window.title("Crear/Editar Tarea")
        self.window.geometry("500x500")
        self.window.iconbitmap("assets/progranizer.ico")

        self.build_ui()

        if self.task:
            self.fill_form()

    def build_ui(self):
        """
        Crea y organiza todos los widgets del formulario.
        """
        frame = ttk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.titulo = ttk.Entry(frame)
        self.titulo.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Resumen:").grid(row=1, column=0, sticky=tk.W)
        self.resumen = ttk.Entry(frame)
        self.resumen.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Estado:").grid(row=2, column=0, sticky=tk.W)
        self.estado = ttk.Combobox(frame, values=["Por hacer", "En revisión", "Finalizado"], state="readonly")
        self.estado.grid(row=2, column=1, pady=5)
        self.estado.set("Por hacer")

        ttk.Label(frame, text="Fecha Inicio (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W)
        self.fecha_inicio = ttk.Entry(frame)
        self.fecha_inicio.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Fecha Entrega (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W)
        self.fecha_entrega = ttk.Entry(frame)
        self.fecha_entrega.grid(row=4, column=1, pady=5)

        ttk.Label(frame, text="Hora Entrega (HH:MM):").grid(row=5, column=0, sticky=tk.W)
        self.hora_entrega = ttk.Entry(frame)
        self.hora_entrega.grid(row=5, column=1, pady=5)

        ttk.Label(frame, text="Detalles:").grid(row=6, column=0, sticky=tk.W)
        self.detalles = tk.Text(frame, height=4, width=30)
        self.detalles.grid(row=6, column=1, pady=5)

        ttk.Label(frame, text="Responsable:").grid(row=7, column=0, sticky=tk.W)
        self.usuarios = get_all_users()
        self.usuarios_dict = {f"{u['nombre']} {u['apellido']}": u["id"] for u in self.usuarios}
        self.responsable = ttk.Combobox(frame, values=list(self.usuarios_dict.keys()), state="readonly")
        self.responsable.grid(row=7, column=1, pady=5)

        btn_text = "Actualizar" if self.task else "Guardar"
        guardar_btn = ttk.Button(frame, text=btn_text, command=self.save_task)
        guardar_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def fill_form(self):
        """
        Llena el formulario con los datos de una tarea existente (modo edición).
        """
        self.titulo.insert(0, self.task[1])
        self.resumen.insert(0, self.task[2])
        self.estado.set(self.task[3])
        self.fecha_inicio.insert(0, self.task[4])
        self.fecha_entrega.insert(0, self.task[5])
        self.hora_entrega.insert(0, self.task[6])
        self.detalles.insert("1.0", self.task[7])

        usuario_id = self.task[8]
        for nombre, uid in self.usuarios_dict.items():
            if uid == usuario_id:
                self.responsable.set(nombre)
                break

    def save_task(self):
        """
        Guarda los datos de la tarea, sea nueva o modificada.

        Muestra un mensaje en caso de éxito o error. Llama a `on_save` si se proporciona.
        """
        try:
            responsable_nombre = self.responsable.get()
            usuario_id = self.usuarios_dict.get(responsable_nombre)

            if not usuario_id:
                messagebox.showerror("Error", "Debes seleccionar un responsable válido.")
                return

            datos = (
                self.titulo.get(),
                self.resumen.get(),
                self.estado.get(),
                self.fecha_inicio.get(),
                self.fecha_entrega.get(),
                self.hora_entrega.get(),
                self.detalles.get("1.0", tk.END).strip(),
                usuario_id
            )

            if self.task:
                update_task(self.task[0], datos)
                messagebox.showinfo("Actualizado", "Tarea actualizada correctamente.")
            else:
                create_task(datos)
                messagebox.showinfo("Creado", "Tarea creada correctamente.")

            if self.on_save:
                self.on_save()

            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la tarea:\n{e}")
