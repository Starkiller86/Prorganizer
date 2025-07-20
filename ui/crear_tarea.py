import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from models import create_task, update_task


class CrearTareaWindow:
    def __init__(self, parent, on_save=None, task=None):
        """
        Ventana para crear o editar una tarea.

        Args:
            parent (tk.Widget): Ventana padre.
            on_save (callable, optional): Función que se ejecuta después de guardar.
            task (tuple/list, optional): Datos de la tarea a editar.
        """
        self.parent = parent
        self.on_save = on_save
        self.task = task
        self.color = "#2196F3"  # color por defecto

        self.window = tk.Toplevel(parent)
        self.window.title("Editar tarea" if task else "Crear tarea")
        self.window.grab_set()  # Modal
        self.window.iconbitmap("assets/progranizer.ico")
        

        self.build_ui()

        if task:
            self.fill_form()

    def build_ui(self):
        frame = ttk.Frame(self.window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.titulo = ttk.Entry(frame)
        self.titulo.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Materia:").grid(row=1, column=0, sticky=tk.W)
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

        self.color_btn = ttk.Button(frame, text=f"Color: {self.color}", command=self.seleccionar_color)
        self.color_btn.grid(row=7, column=0, columnspan=2, pady=5)

        btn_text = "Actualizar" if self.task else "Guardar"
        guardar_btn = ttk.Button(frame, text=btn_text, command=self.save_task)
        guardar_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def seleccionar_color(self):
        color = colorchooser.askcolor(title="Elige un color")
        if color[1]:
            self.color = color[1]
            self.color_btn.config(text=f"Color: {self.color}")

    def fill_form(self):
        try:
            self.titulo.insert(0, self.task[1])
            self.resumen.insert(0, self.task[2])
            self.estado.set(self.task[3])
            self.fecha_inicio.insert(0, self.task[4])
            self.fecha_entrega.insert(0, self.task[5])
            self.hora_entrega.insert(0, self.task[6])
            self.detalles.insert("1.0", self.task[7])
            if len(self.task) > 8 and self.task[8]:
                self.color = self.task[8]
                self.color_btn.config(text=f"Color: {self.color}")
        except IndexError:
            # Si faltan campos, muestra un error o asigna valores por defecto
            messagebox.showerror("Error", "Datos incompletos para editar la tarea.")
            self.window.destroy()


    def save_task(self):
        datos = (
            self.titulo.get(),
            self.resumen.get(),
            self.estado.get(),
            self.fecha_inicio.get(),
            self.fecha_entrega.get(),
            self.hora_entrega.get(),
            self.detalles.get("1.0", tk.END).strip(),
            self.color
        )
        try:
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
