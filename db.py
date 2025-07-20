import mysql.connector
import traceback
import mysql.connector
print(mysql.connector.__file__)


def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="020614",
            database="gestor_tareas",
            port=3306,
            use_pure=True  # ¡ESTO ES CLAVE!
        )
    except Exception as e:
        with open("db_connect_error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
