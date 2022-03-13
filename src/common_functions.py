from src.db_manager import *
import re

# Aqui se agregan funciones en comun que usan tanto el bot como el client para no repetir codigo.


#Pequeña funcion para manejar plurales en los mensajes que devuelve el bot.
def Plurals(fichas):
    if fichas == 1:
        return "ficha"
    else:
        return "fichas"

# Actualiza la cantidad de fichas de un usuario
def actualizar_fichas(user,fichas):
    cantTotal = get_fichas_by_user(user)
    cantActualizada = -1
    if (not cantTotal and fichas > 0):
        cantActualizada = fichas
        datainsertion = [user, cantActualizada]
        update_fichas(datainsertion)
    elif(cantTotal):
        cantActualizada = int(cantTotal[0]) + fichas
        if cantActualizada >= 0:
            datainsertion = [user, cantActualizada]
            update_fichas(datainsertion)
    return cantActualizada

# Expresion regular para controlar que el username sea valido
def allowed_chars(username):
   return re.match("^[A-Za-z0-9_-]*$", username)
