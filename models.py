from db import connect_db

def create_task(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tareas 
        (titulo, resumen, estado, fecha_inicio, fecha_entrega, hora_entrega, detalles, usuario_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        tareas.id,
        tareas.titulo,
        tareas.resumen,
        tareas.estado,
        tareas.fecha_inicio,
        tareas.fecha_entrega,
        tareas.hora_entrega,
        tareas.detalles,
        tareas.usuario_id,
        usuarios.nombre AS responsable
    FROM tareas
    LEFT JOIN usuarios ON tareas.usuario_id = usuarios.id
    """
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, data):
    conn = connect_db()
    cursor = conn.cursor()
    if len(data) != 8:
        raise ValueError(f"Faltan datos. Se esperaban 8 campos y se recibieron {len(data)}")

    cursor.execute("""
        UPDATE tareas SET
            titulo=%s,
            resumen=%s,
            estado=%s,
            fecha_inicio=%s,
            fecha_entrega=%s,
            hora_entrega=%s,
            detalles=%s,
            usuario_id=%s
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
