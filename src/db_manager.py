import sqlite3
from pathlib import Path
#Conecto con la base y creo las tablas si no existen.

project_path = str(Path(__file__).parents[1])
con = sqlite3.connect( project_path + "/db/arcadesDB")

cur = con.cursor()
cur.execute(
        "CREATE TABLE IF NOT EXISTS tabla_fichas (user TEXT NOT NULL PRIMARY KEY UNIQUE, fichas INTEGER NOT NULL)"
    )
cur.execute(
        "CREATE TABLE IF NOT EXISTS tabla_canjes (user TEXT NOT NULL, juego TEXT NOT NULL, timestamp TEXT NOT NULL)"
    )

# Funcion para insertar datos en una tabla cualquiera de la base.

def insert(SQL_text,data):
     cur.execute(
        SQL_text, data
     )
     con.commit()

# Funcion para actualizar el tabla_fichas.
def update_fichas(data):
    cur.execute(
        "REPLACE INTO tabla_fichas (user, fichas) VALUES (?, ?)",
            data,
                )
    con.commit()

# Funcion para actualizar la tabla de canjes.

def insert_tablaCanjes(data):
     cur.execute(
        "INSERT INTO tabla_canjes VALUES (?, ?, ?)", data
     )
     con.commit()

# Devuelve el usuario con mas fichas.

def get_top_by_fichas():
    return list(
         cur.execute(
            "SELECT *, MAX(fichas) FROM tabla_fichas"
            ).fetchone())

def get_fichas_by_user(user):
    return cur.execute(
            "SELECT fichas FROM tabla_fichas WHERE user = '%s'" % (user)
        ).fetchone()

def runSQL(SQL_text):
    cur.execute(
        SQL_text
    )
    con.commit()
