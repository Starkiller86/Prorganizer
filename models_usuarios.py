# models_usuarios.py
from db import connect_db

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo) VALUES (%s, %s, %s, %s)", data)
    conn.commit()
    conn.close()

def update_user(user_id, data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nombre=%s, apellido=%s, telefono=%s, correo=%s WHERE id=%s", (*data, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
