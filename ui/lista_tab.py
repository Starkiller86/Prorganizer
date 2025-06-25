from tkinter import ttk
import tkinter as tk
from ui.crear_tarea import CrearTareaWindow
from models import get_all_tasks, update_task, delete_task
from tkinter import messagebox

class ListaTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Lista")
        self.build_ui()

    def build_ui(self):
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        crear_btn = ttk.Button(top_frame, text="Crear Tarea", command=self.open_create_window)
        crear_btn.pack(side=tk.LEFT)

        columnas = ("ID", "Título", "Resumen", "Estado", "Fecha Inicio", "Fecha Entrega", "Hora Entrega", "Detalles", "Usuario ID", "Responsable")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Ocultar columnas que no quieres mostrar visualmente
        self.tree.column("Resumen", width=0, stretch=False)
        self.tree.column("Detalles", width=0, stretch=False)
        self.tree.column("Usuario ID", width=0, stretch=False)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Editar", command=self.edit_task)
        self.menu.add_command(label="Eliminar", command=self.delete_selected_task)
        self.menu.add_command(label="Marcar como Finalizado", command=self.mark_as_done)

        self.tree.bind("<Button-3>", self.show_menu)
        self.load_tasks()

    def show_menu(self, event):
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.menu.post(event.x_root, event.y_root)

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in get_all_tasks():
            self.tree.insert("", "end", values=(
                task["id"],
                task["titulo"],
                task["resumen"],
                task["estado"],
                task["fecha_inicio"],
                task["fecha_entrega"],
                task["hora_entrega"],
                task["detalles"],
                task["usuario_id"],
                task["responsable"]
            ))

    def open_create_window(self):
        CrearTareaWindow(self.frame, on_save=self.load_tasks)

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_data = self.tree.item(selected[0])["values"]
        CrearTareaWindow(self.frame, on_save=self.load_tasks, task=task_data)

    def delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirmar", "¿Deseas eliminar esta tarea?")
        if confirm:
            delete_task(task_id)
            self.load_tasks()

    def mark_as_done(self):
        selected = self.tree.selection()
        if not selected:
            return

        task_data = self.tree.item(selected[0])["values"]

        if len(task_data) < 9:
            messagebox.showerror("Error", f"Faltan datos. Se esperaban al menos 9 campos y se recibieron {len(task_data)}.")
            return

        updated = [
            task_data[1],  # Título
            task_data[2],  # Resumen
            "Finalizado",  # Estado modificado
            task_data[4],  # Fecha inicio
            task_data[5],  # Fecha entrega
            task_data[6],  # Hora
            task_data[7],  # Detalles
            task_data[8]   # Usuario ID
        ]

        try:
            update_task(task_data[0], updated)
            messagebox.showinfo("Tarea completada", "Tarea marcada como finalizada.")
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tarea:\n{e}")