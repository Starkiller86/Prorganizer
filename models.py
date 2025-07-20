"""
models.py - Lógica de datos para la gestión de tareas.

Contiene funciones que se encargan del acceso y manipulación de los datos
relacionados con las tareas almacenadas en la base de datos MySQL.
Forma parte del modelo en la arquitectura MVC.
"""

from db import connect_db

def create_task(data):
    """
    Inserta una nueva tarea en la base de datos.

    Args:
        data (tuple): Contiene los siguientes datos en orden:
            (titulo, resumen, estado, fecha_inicio, fecha_entrega,
            hora_entrega, detalles, color)
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tareas 
        (titulo, resumen, estado, fecha_inicio, fecha_entrega, hora_entrega, detalles, color)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    cursor.close()
    conn.close()


def update_task(task_id, data):
    """
    Actualiza una tarea existente en la base de datos.

    Args:
        task_id (int): ID de la tarea a actualizar.
        data (tuple): Nuevos datos de la tarea. Debe tener 8 elementos.
    Raises:
        ValueError: Si la tupla de datos no tiene exactamente 8 elementos.
    """
    if len(data) != 8:
        raise ValueError(f"Faltan datos. Se esperaban 8 campos y se recibieron {len(data)}")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas SET
            titulo=%s,
            resumen=%s,
            estado=%s,
            fecha_inicio=%s,
            fecha_entrega=%s,
            hora_entrega=%s,
            detalles=%s,
            color=%s
        WHERE id=%s
    """, (*data, task_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_task(task_id):
    """
    Elimina una tarea de la base de datos.

    Args:
        task_id (int): ID de la tarea a eliminar.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_tasks():
    """
    Recupera todas las tareas de la base de datos, ordenadas por fecha de entrega.

    Returns:
        list[dict]: Lista de tareas.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            id,
            titulo,
            resumen,
            estado,
            fecha_inicio,
            fecha_entrega,
            hora_entrega,
            detalles,
            color
        FROM tareas
        ORDER BY fecha_entrega ASC
    """)
    tareas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tareas
