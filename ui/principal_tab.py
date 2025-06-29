"""
principal_tab.py - Pestaña principal con vista diaria y diagrama de Gantt semanal.

Esta vista permite al usuario alternar entre una visualización de tareas del día
y un gráfico tipo Gantt de las tareas de la semana, usando matplotlib.

Pertenece a la capa Vista en la arquitectura MVC.
"""

from tkinter import ttk
import tkinter as tk
from models import get_all_tasks
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PrincipalTab:
    """
    Clase que representa la pestaña 'Principal' de la aplicación.

    Permite al usuario visualizar tareas en modo diario o semanal (Gantt).
    Utiliza polimorfismo en `update_view` para cambiar el contenido mostrado.
    """

    def __init__(self, notebook):
        """
        Inicializa la pestaña y construye su interfaz.

        Args:
            notebook (ttk.Notebook): Contenedor de pestañas.
        """
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Principal")

        self.view_mode = tk.StringVar(value="día")  # Alterna entre 'día' y 'semana'
        self.build_ui()

    def build_ui(self):
        """
        Construye los elementos de la interfaz gráfica, incluyendo botones de modo de vista.
        """
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(top_frame, text="Ver por:").pack(side=tk.LEFT)
        ttk.Radiobutton(top_frame, text="Día", variable=self.view_mode, value="día", command=self.update_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(top_frame, text="Semana (Gantt)", variable=self.view_mode, value="semana", command=self.update_view).pack(side=tk.LEFT, padx=5)

        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.update_view()

    def update_view(self):
        """
        Cambia la vista entre 'día' y 'semana' dependiendo del valor de self.view_mode.

        Aplica polimorfismo: la lógica cambia dinámicamente según el valor del estado.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.view_mode.get() == "día":
            self.show_daily_view()
        else:
            self.show_weekly_gantt()

    def show_daily_view(self):
        """
        Muestra una tabla con las tareas del día actual.
        """
        label = ttk.Label(self.content_frame, text=f"Tareas del día: {datetime.today().strftime('%Y-%m-%d')}", font=("Segoe UI", 12, "bold"))
        label.pack(pady=(10, 0))

        columns = ("Título", "Inicio", "Entrega", "Hora", "Responsable")

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, bordercolor="#333", relief="solid")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), bordercolor="#333", relief="solid")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        tree.column("Título", anchor="w", width=250)
        tree.column("Inicio", anchor="center", width=100)
        tree.column("Entrega", anchor="center", width=100)
        tree.column("Hora", anchor="center", width=80)
        tree.column("Responsable", anchor="w", width=150)

        tree.tag_configure("even", background="#f0f0f0")
        tree.tag_configure("odd", background="#ffffff")

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tasks = get_all_tasks()
        for idx, task in enumerate(tasks):
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end", values=(
                task["titulo"],
                task["fecha_inicio"],
                task["fecha_entrega"],
                task["hora_entrega"],
                task["responsable"]
            ), tags=(tag,))

    def show_weekly_gantt(self):
        """
        Muestra las tareas en un gráfico tipo Gantt usando matplotlib.
        """
        tasks = get_all_tasks()
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Diagrama de Gantt - Semana")
        ax.set_xlabel("Fechas")
        ax.set_ylabel("Tareas")

        estado_color = {
            "Por hacer": "#ffcc00",
            "En revisión": "#00bfff",
            "Finalizado": "#32cd32"
        }

        y_labels = []
        today = datetime.today().date()

        for i, task in enumerate(tasks):
            try:
                inicio = datetime.strptime(str(task["fecha_inicio"]), "%Y-%m-%d").date()
                fin = datetime.strptime(str(task["fecha_entrega"]), "%Y-%m-%d").date()
                duracion = (fin - inicio).days + 1
                estado = task.get("estado", "")
                color = estado_color.get(estado, "#999999")

                ax.barh(i, duracion, left=inicio, height=0.5, color=color, edgecolor='black')
                y_labels.append(task["titulo"])
            except Exception as e:
                print(f"Error en fechas: {e}")

        ax.axvline(today, color='red', linestyle='--', label='Hoy')
        ax.legend()

        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
