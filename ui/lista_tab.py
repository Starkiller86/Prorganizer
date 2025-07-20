from tkinter import ttk
import tkinter as tk
from ui.crear_tarea import CrearTareaWindow
from models import get_all_tasks, update_task, delete_task
from tkinter import messagebox

class ListaTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Lista")
        self.color_icons = {}  # Guardar referencias a imágenes para colores
        self.build_ui()

    def build_ui(self):
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        crear_btn = ttk.Button(top_frame, text="Crear Tarea", command=self.open_create_window)
        crear_btn.pack(side=tk.LEFT)

        columnas = ("Título", "Materia", "Estado", "Fecha Inicio", "Fecha Entrega", "Hora Entrega", "Detalles")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")

        # Configura encabezados y columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.column("Fecha Inicio", width=0, stretch=False)
        self.tree.column("Detalles", width=0, stretch=False)

        # Columna #0 para el color
        self.tree["show"] = "headings"  # ocultar #0 por defecto
        # Cambiar a mostrar la columna #0 para la imagen de color
        self.tree["show"] = "tree headings"
        self.tree.column("#0", width=20, stretch=False)
        self.tree.heading("#0", text="")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Editar", command=self.edit_task)
        self.menu.add_command(label="Eliminar", command=self.delete_selected_task)
        self.menu.add_command(label="Marcar como Finalizado", command=self.mark_as_done)

        self.tree.bind("<Button-3>", self.show_menu)
        self.load_tasks()

    def crear_icono_color(self, color, size=16):
        img = tk.PhotoImage(width=size, height=size)
        img.put(color, to=(0, 0, size, size))
        return img

    def load_tasks(self):
        # Limpia el treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        for task in get_all_tasks():
            color = task["color"]
            if color not in self.color_icons:
                self.color_icons[color] = self.crear_icono_color(color)
            icono = self.color_icons[color]

            # Usa el id como iid para luego referenciarlo fácilmente
            self.tree.insert(
                "",
                "end",
                iid=str(task["id"]),
                text="",      # Texto para columna #0, dejamos vacío porque mostramos solo imagen
                image=icono,
                values=(
                    task["titulo"],
                    task["resumen"],
                    task["estado"],
                    task["fecha_inicio"],
                    task["fecha_entrega"],
                    task["hora_entrega"],
                    task["detalles"]
                )
            )

    def show_menu(self, event):
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.menu.post(event.x_root, event.y_root)

    def open_create_window(self):
        CrearTareaWindow(self.frame, on_save=self.load_tasks)

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        task_data = self.tree.item(task_id)["values"]
        # Construimos tuple con id al inicio para que coincida con CrearTareaWindow
        CrearTareaWindow(self.frame, on_save=self.load_tasks, task=(task_id, *task_data))

    def delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        confirm = messagebox.askyesno("Confirmar", "¿Deseas eliminar esta tarea?")
        if confirm:
            delete_task(task_id)
            self.load_tasks()

    def mark_as_done(self):
        selected = self.tree.selection()
        if not selected:
            return
    
        task_id = selected[0]
        task_data = self.tree.item(task_id)["values"]
        estado_actual = task_data[2]
    
        if estado_actual == "Finalizado":
            confirm = messagebox.askyesno("Confirmar", "¿La tarea ya está finalizada. ¿Eliminarla?")
            if confirm:
                try:
                    delete_task(task_id)
                    messagebox.showinfo("Tarea eliminada", "La tarea finalizada fue eliminada.")
                    self.load_tasks()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la tarea:\n{e}")
        else:
            # Solo marcar como Finalizado
            updated = list(task_data)
            updated[2] = "Finalizado"  # Cambiar estado
            tasks = get_all_tasks()
            color = next((t["color"] for t in tasks if str(t["id"]) == task_id), None)
            if color is None:
                messagebox.showerror("Error", "No se encontró el color de la tarea.")
                return
            updated.append(color)
    
            try:
                update_task(task_id, updated)
                messagebox.showinfo("Tarea actualizada", "Tarea marcada como finalizada.")
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la tarea:\n{e}")

