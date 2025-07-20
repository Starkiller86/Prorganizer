"""
main.py - Punto de entrada de la aplicación Progranizer.

Este módulo inicia la interfaz principal del sistema de gestión de tareas.
Utiliza ttkbootstrap para estilizar la GUI y organiza las vistas en pestañas.

Pertenece al Controlador en la arquitectura MVC.
"""

import tkinter as tk
import ttkbootstrap as tb

from ui.principal_tab import PrincipalTab
from ui.lista_tab import ListaTab
from db import connect_db

def main():
    app = tb.Window(themename="sandstone")  # Puedes cambiar el tema a tu gusto
    app.title("Progranizer - Gestor de Tareas")
    app.geometry("900x600")
    app.iconbitmap("assets/progranizer.ico")
    app.state('zoomed')  # Windows

    notebook = tb.Notebook(app)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Inicializa las pestañas
    PrincipalTab(notebook)
    ListaTab(notebook)

    app.mainloop()

if __name__ == "__main__":
    main()

def create_task(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tareas 
        (titulo, resumen, estado, fecha_inicio, fecha_entrega, hora_entrega, detalles, color)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            id, titulo, resumen, estado, fecha_inicio,
            fecha_entrega, hora_entrega, detalles, color
        FROM tareas
        ORDER BY fecha_entrega ASC
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, data):
    if len(data) != 8:
        raise ValueError(f"Se esperaban 8 campos y se recibieron {len(data)}")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas SET
            titulo=%s, resumen=%s, estado=%s,
            fecha_inicio=%s, fecha_entrega=%s,
            hora_entrega=%s, detalles=%s, color=%s
        WHERE id=%s
    """, (*data, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

