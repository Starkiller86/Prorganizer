"""
models_usuarios.py - Lógica de datos para la gestión de usuarios.

Contiene funciones para acceder, crear, actualizar y eliminar registros
de usuarios desde la base de datos MySQL. Forma parte del modelo en la arquitectura MVC.
"""

from db import connect_db

def get_all_users():
    """
    Recupera todos los usuarios almacenados en la base de datos.

    Returns:
        list[dict]: Lista de usuarios con campos id, nombre, apellido, teléfono y correo.
    """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(data):
    """
    Inserta un nuevo usuario en la base de datos.

    Args:
        data (tuple): Contiene los campos (nombre, apellido, telefono, correo).
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo) VALUES (%s, %s, %s, %s)", data)
    conn.commit()
    conn.close()

def update_user(user_id, data):
    """
    Actualiza la información de un usuario existente.

    Args:
        user_id (int): ID del usuario a actualizar.
        data (tuple): Nuevos valores para (nombre, apellido, telefono, correo).
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre=%s, apellido=%s, telefono=%s, correo=%s WHERE id=%s",
        (*data, user_id)
    )
    conn.commit()
    conn.close()

def delete_user(user_id):
    """
    Elimina un usuario de la base de datos.

    Args:
        user_id (int): ID del usuario a eliminar.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
