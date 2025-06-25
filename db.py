# db.py
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="020614",
        database="gestor_tareas"
    )
