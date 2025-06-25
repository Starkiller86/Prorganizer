from tkinter import ttk
import tkinter as tk
from models import get_all_tasks
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PrincipalTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Principal")

        self.view_mode = tk.StringVar(value="día")
        self.build_ui()

    def build_ui(self):
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, pady=10, padx=10)

        ttk.Label(top_frame, text="Ver por:").pack(side=tk.LEFT)
        ttk.Radiobutton(top_frame, text="Día", variable=self.view_mode, value="día", command=self.update_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(top_frame, text="Semana (Gantt)", variable=self.view_mode, value="semana", command=self.update_view).pack(side=tk.LEFT, padx=5)

        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.update_view()

    def update_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.view_mode.get() == "día":
            self.show_daily_view()
        else:
            self.show_weekly_gantt()

    def show_daily_view(self):
        tree = ttk.Treeview(self.content_frame, columns=("Título", "Inicio", "Entrega", "Hora", "Responsable"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tasks = get_all_tasks()
        for task in tasks:
            tree.insert("", "end", values=(
                task["titulo"], task["fecha_inicio"],
                task["fecha_entrega"], task["hora_entrega"],
                task["responsable"]
            ))

    def show_weekly_gantt(self):
        tasks = get_all_tasks()
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Diagrama de Gantt - Semana")
        ax.set_xlabel("Fechas")
        ax.set_ylabel("Tareas")

        estado_color = {
            "Por hacer": "#ffcc00",      # amarillo
            "En revisión": "#00bfff",    # azul claro
            "Finalizado": "#32cd32"      # verde
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

                ax.barh(i, duracion, left=inicio, height=0.5, color=color)
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