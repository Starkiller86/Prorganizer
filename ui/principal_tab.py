from tkinter import ttk
import tkinter as tk
from models import get_all_tasks
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

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
        label = ttk.Label(self.content_frame, text=f"Tareas del día: {datetime.today().strftime('%Y-%m-%d')}", font=("Segoe UI", 12, "bold"))
        label.pack(pady=(10, 0))

        columns = ("Materia","Título", "Inicio", "Entrega", "Hora")

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, bordercolor="#333", relief="solid")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), bordercolor="#333", relief="solid")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        tree.column("Materia",anchor="w", width=250)
        tree.column("Título", anchor="w", width=250)
        tree.column("Inicio", anchor="center", width=100)
        tree.column("Entrega", anchor="center", width=100)
        tree.column("Hora", anchor="center", width=80)

        tree.tag_configure("even", background="#f0f0f0")
        tree.tag_configure("odd", background="#ffffff")

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tasks = get_all_tasks()
        for idx, task in enumerate(tasks):
            tag = "even" if idx % 2 == 0 else "odd"
            tree.insert("", "end", values=(
                task["resumen"],
                task["titulo"],
                task["fecha_inicio"],
                task["fecha_entrega"],
                task["hora_entrega"]
            ), tags=(tag,))

    def show_weekly_gantt(self):
        tasks = get_all_tasks()

        # Crear figura y ajustar configuración
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.set_title("Diagrama de Gantt - Semana")
        ax.set_xlabel("Fechas")
        ax.set_ylabel("Tareas")

        # Mejora en formato de fechas (más precisión visual)
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b')) 

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
                duracion = (fin - inicio).days
                estado = task.get("estado", "")
                color = task.get("color") or estado_color.get(estado, "#999999")

                ax.barh(i, duracion, left=mdates.date2num(inicio), height=0.5, color=color, edgecolor='black')
                y_labels.append(task["titulo"])
            except Exception as e:
                print(f"Error en fechas: {e}")

        # Línea vertical para "hoy"
        ax.axvline(mdates.date2num(today), color='red', linestyle='--', label='Hoy')
        ax.legend()

        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels)
        fig.autofmt_xdate()

        # 📌 Contenedor nuevo para evitar conflictos al re-renderizar
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 🔧 Fuerza refresco correcto e inmediato
        canvas.draw()
        canvas_widget.update_idletasks()
        canvas_widget.update()
        canvas.flush_events()


