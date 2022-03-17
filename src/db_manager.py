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
        "CREATE TABLE IF NOT EXISTS tabla_canjes (user TEXT NOT NULL, juego TEXT NOT NULL, fichas_gastadas INTEGER NOT NULL, timestamp TEXT NOT NULL)"
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
        "INSERT INTO tabla_canjes VALUES (?, ?, ?, ?)", data
     )
     con.commit()

# Devuelve el usuario con mas fichas.
def get_top_by_fichas():
    return list(
         cur.execute(
            "SELECT *, MAX(fichas) FROM tabla_fichas"
            ).fetchone())

# Devuelve el usuario que mas fichas gastó.
def get_top_gastadas():
    return cur.execute(
            "SELECT user, SUM (fichas_gastadas) FROM tabla_canjes GROUP BY user ORDER BY SUM (fichas_gastadas) DESC"
        ).fetchone()

# Devuelve las fichas que tiene un usuario.
def get_fichas_by_user(user):
    return cur.execute(
            "SELECT fichas FROM tabla_fichas WHERE user = '%s'" % (user)
        ).fetchone()
# Devuelve el total de fichas que un usuario lleva gastando.
def get_gastadas_by_user(user):
    return cur.execute(
            "SELECT SUM (fichas_gastadas) FROM tabla_canjes WHERE user = '%s'" % (user)
        ).fetchone()
# Devuelve el total de fichas disponibles entre todos los usuarios.
def total_fichas_disponibles():
    return cur.execute(
             "SELECT SUM(fichas) FROM tabla_fichas"
        ).fetchone()

#Funcion para correr una consulta SQL cualquiera.
def runSQL(SQL_text):
    cur.execute(
        SQL_text
    )
    con.commit()
