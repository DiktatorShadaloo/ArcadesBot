from dataclasses import replace
from datetime import datetime
from threading import Thread
from twitchio.ext import commands
from src.db_manager import *
from src.common_functions import *
import asyncio
from config.config import *

ArcadesBot = commands.Bot( 
    token=BOT_TOKEN, 
    prefix=BOT_PREFIX, 
    initial_channels= CHANNEL)

restBits={}

#Se implementa esto aca en vez de el cliente como solucion a que twitch aleatoreamente skipea la escritura de mensajes que se envian por medio del modulo IRC a pesar de ser correctamente enviados.
def insertarfichas(data):
     #Expresion regular para obtener el input del usuario
        input = re.search(r"PRIVMSG +#[\w]* +:[\w\W\s]*",data).group(0)
     #Expresion para obtener el usuario que canjeo la recompensa.
        user = re.search(r"[-\w_]*.tmi.twitch.tv",data).group(0).replace('.tmi.twitch.tv','')
        arrayinput = input.split(":", 1)[1].split(";",1)
        fichas_gastadas = (arrayinput[0]).replace(" ","")
     #Chequeo que la fichas sean un entero mayor a 0
        if fichas_gastadas.isdigit() and int(fichas_gastadas)>0 :
            fichas_gastadas = int(fichas_gastadas)

         #Chequeo que la fichas no superen al maximo definido por el dueño del canal.
            if fichas_gastadas <= FICHAS_MAXIMAS:
                if len (arrayinput) == 2:
                    juego = arrayinput[1]. replace("\r\n","") 
                 #Chequeo que el nombre del juego no sea vacio. 
                    if juego. replace(" ","") != "":
                    #Chequeo que el usuario tenga la cantidad de fichas suficientes y actualizo en la base de datos.
                        restantes = actualizar_fichas(user.lower(),-fichas_gastadas)
                        if (restantes>=0):
                            fecha = datetime.now().strftime("%H:%M:%S %d-%m-%y")
                            data = [user, juego, fichas_gastadas,fecha]
                            pluralFichas = Plurals(fichas_gastadas)
                            pluralRestantes = Plurals(restantes)
                            MENSAJE = "%s le puso %d %s al juego %s, ahora le quedan %d %s" % (user, fichas_gastadas, pluralFichas, juego, restantes, pluralRestantes)

                            insert_tablaCanjes(data)

                        #Se crean estos txt para utilizar en conjunto con Txt Trigger script para OBS.
                            with open('UltimoPedido.txt', 'w') as f:
                                f.write(fecha)
                            with open('Usuario.txt', 'w') as f:
                                f.write(("%s inserto %d %s")%(user, fichas_gastadas, pluralFichas))
                            with open('JuegoPedido.txt', 'w') as d:
                                d.write(data[1])
                        else:
                            MENSAJE = "¡%s no tiene fichas suficientes!" % (user)
                    else: 
                        MENSAJE = "¡No especificaste que juego jugar!"
                else: 
                    MENSAJE =  'Formato de pedido incorrecto, recuerda que el formato es <fichas ; nombre_del_juego>, por ejemplo " 3 ; Street Fighter 2 "'
            else:
                pluralFichas = Plurals(FICHAS_MAXIMAS)
                MENSAJE = "¡Esas son demasiadas fichas! No podes poner mas de %d %s a la vez" % (FICHAS_MAXIMAS, pluralFichas)
        else:
            MENSAJE = 'Formato de pedido incorrecto, recuerda que el formato es <fichas ; nombre_del_juego>, por ejemplo " 3 ; Street Fighter 2 "'
        printear(MENSAJE)
        return MENSAJE

def agregarxbits_Automaticamente(data):
    global restBits
 # Expresion regular para obtener el usuario.
    lowuser = re.search(r"[-\w_]*.tmi.twitch.tv",data).group(0).replace('.tmi.twitch.tv','')
 # Expresion regular para obtener el la cantidad de bits.
    bits= re.search (r"bits=[0-9]*", data.split('PRIVMSG',1)[0]).group(0).replace('bits=','')
 # Lo agrego al array de restos de bits.
    if not (lowuser in restBits):
        restBits[lowuser]=0

    fichas = int(bits) + restBits[lowuser] // PRECIO_BITS
    restBits[lowuser]= (int(bits) + restBits[lowuser]) % PRECIO_BITS

 # Reviso que haya obtenido fichas.
    if (fichas>0):
        # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
        cantTotal=actualizar_fichas(lowuser,fichas)

        # Corrijo los plurales para el mensaje de chat.
        pluralTotal = Plurals(cantTotal)
        pluralAgregadas = Plurals(fichas)
        MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (lowuser, fichas, pluralAgregadas, cantTotal, pluralTotal)

    else:
        MENSAJE = "Oh no! Esos bits no son suficientes para obtener una ficha, cada ficha cuesta %d bits, agrega %d en este stream para obtener una ficha!" % (PRECIO_BITS, PRECIO_BITS-restBits[lowuser])

    return MENSAJE

@ArcadesBot.event()   
async def event_ready():
    printear(f"Logged in as {BOT_NICK} in {CHANNEL}.")

@ArcadesBot.event()
async def event_raw_data(data):
    if 'custom-reward-id' in data and INSERT_COINS_ID in data:
        MENSAJE = insertarfichas(data)
        await ArcadesBot._connection.send(("PRIVMSG %s :") % CHANNEL[0].lower() +MENSAJE)
    elif 'bits=' in data.split('PRIVMSG',1)[0]:
        MENSAJE = agregarxbits_Automaticamente(data)
        await ArcadesBot._connection.send(("PRIVMSG %s :") % CHANNEL[0].lower() +MENSAJE)
################################################################## COMANDOS ###############################################

# Comando de ayuda
@ArcadesBot.command()
async def help(ctx):
    MENSAJE = "Los comandos solo para mods son: %sagregarfichas <usuario> <fichas> | %sagregarxsub <usuario> | %sagregarxbits <usuario> <bits> | %sagregarxgifts <usuario> <cantidad_regaladas> | %sagregarxdonacion <usuario> <monto> | %ssacarfichas <usuario> <fichas>|  %svaciarfichas <usuario>" % (BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX)
    await ctx.send(f"%s" % MENSAJE)
    MENSAJE = "Los comandos para mods y espectadores son: %scantfichas <usuario> | %scantgastadas <usuario> | %sgastadortop | %susuariotop | %stotalfichas" % (BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX,BOT_PREFIX)
    await ctx.send(f"%s" % MENSAJE)
###########################################################################################################################

# Comando para agregar fichas a un usuario
@ArcadesBot.command()
async def agregarfichas( ctx , user: str = None, fichas: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if ( autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","") ):

     # Convierto el user a minusculas y reviso la entrada. 
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit() and
            fichas.isdigit() and
            int(fichas) > 0
        ):
            fichas = int(fichas)

         # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
            cantTotal=actualizar_fichas(lowuser,fichas)

         # Corrijo los plurales para el mensaje de chat.
            pluralTotal = Plurals(cantTotal)
            pluralAgregadas = Plurals(fichas)

            MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."
    
     # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    printear(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################

# Comando para agregar fichas a un usuario que donó bits.
@ArcadesBot.command()
async def agregarxbits( ctx , user: str = None, bits: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if ( autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto user a minusculas y reviso la entrada. 
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit() and
            bits.isdigit()
        ):

            global restBits
            if not (lowuser in restBits):
                restBits[lowuser]=0
         #Reviso que el monto alcance para comprar una ficha.
            fichas = (int(bits) + restBits[lowuser]) // PRECIO_BITS
            restBits[lowuser]= (int(bits) + restBits[lowuser]) % PRECIO_BITS

            if (fichas >0):
             # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
                cantTotal=actualizar_fichas(lowuser,fichas)

             # Corrijo los plurales para el mensaje de chat.
                pluralTotal = Plurals(cantTotal)
                pluralAgregadas = Plurals(fichas)
                MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

            else:
                MENSAJE = "Oh no! Esos bits no son suficientes para obtener una ficha, cada ficha cuesta %d bits, agrega %d en este stream para obtener una ficha!" % (PRECIO_BITS, PRECIO_BITS-restBits[lowuser])

        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."
 
 #Si no tiene los privilegios lo notifico.
    else:
            MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    printear(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################  

# Comando para agregar fichas a un usuario que se hizo sub.
@ArcadesBot.command()
async def agregarxsub( ctx , user: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if ( autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto user a minusculas y reviso la entrada 
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit()
        ):
            fichas = FICHAS_X_SUB

         # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
            cantTotal=actualizar_fichas(lowuser,fichas)

         # Corrijo los plurales para el mensaje de chat.
            pluralTotal = Plurals(cantTotal)
            pluralAgregadas = Plurals(fichas)

            MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    await ctx.send(MENSAJE)
    printear(MENSAJE)
###########################################################################################################################

# Comando para agregar fichas a un usuario que regalo subs (si quieren darle fichas a quien recibio las subs de regalo, deberan agregarse a mano, twichio da error al recibir un evento de subcripcion y por eso no se implementa para hacerlo automatico, queda para mas adelante).
@ArcadesBot.command()
async def agregarxgifts( ctx , user: str = None, cantidad: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if ( autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto user a minusculas y reviso la entrada 
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit() and
            cantidad.isdigit()
        ):
            fichas = FICHAS_X_SUB * int(cantidad)

         # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
            cantTotal=actualizar_fichas(lowuser,fichas)

         # Corrijo los plurales para el mensaje de chat.
            pluralTotal = Plurals(cantTotal)
            pluralAgregadas = Plurals(fichas)

            MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    await ctx.send(MENSAJE)
    printear(MENSAJE)
###########################################################################################################################

# Comando para agregar fichas a un usuario que hizo una donacion, como divisa estandar se usa el dolar.
@ArcadesBot.command()
async def agregarxdonacion(ctx , user: str = None, dinero: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if ( autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto user a minusculas y reviso la entrada. 
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit() and
            dinero.isdecimal
        ):
        
             #Reviso que el monto alcance para comprar una ficha.
                if (float(dinero) >= PRECIO_FICHA):
                    fichas = float(dinero) // PRECIO_FICHA
                    
                 # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
                    cantTotal=actualizar_fichas(lowuser,fichas)
                 # Corrijo los plurales para el mensaje de chat.
                    pluralTotal = Plurals(cantTotal)
                    pluralAgregadas = Plurals(fichas)

                    MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

                else:
                    MENSAJE = "Oh no! Ese monto no es suficiente para obtener una ficha, cada ficha cuesta %s dolares!" % (str(PRECIO_FICHA))
                
        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    await ctx.send(MENSAJE)
    printear(MENSAJE)
###########################################################################################################################

# Comando para sacar fichas a un usuario
@ArcadesBot.command()
async def sacarfichas(ctx , user: str = None, fichas: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if (autor in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto user a minuscula y reviso la entrada.
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (
            allowed_chars(lowuser) and 
            not lowuser.isdigit() and
            fichas.isdigit() and
            int(fichas) > 0
        ):

         # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.
            fichas = int(fichas)
            cantTotal=actualizar_fichas(lowuser,- fichas)
            pluralSacadas = Plurals(fichas)

         # Si el usuario tenia las fichas suficientes notifico la cantidad gastada y las fichas restantes.
            if (cantTotal >=0 ):
                pluralTotal = Plurals(cantTotal)

                MENSAJE = " Se restaron %d %s a %s. Le queda un total de %d %s." % (fichas, pluralSacadas, user, cantTotal, pluralTotal)
         # Si el usuario no tiene fichas suficientes lo notifico. 
            else:
                MENSAJE = ("Se ha intentado sacar %d %s, pero %s no tiene fichas suficientes") % (fichas, pluralSacadas, user)

        else:
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, no tenés los privilegios para usar este comando." % (ctx.author.name)
    
    printear(MENSAJE)
    await ctx.send(MENSAJE)        
###########################################################################################################################
    

# Muestra la cantidad de fichas de un usuario
@ArcadesBot.command()
async def cantfichas(ctx, user: str = None):
    
 #Si no hay un user en la entrada, user sera el usuario que ejecuto el comando.
    autor = ctx.author.name.lower()
    if user == None:
        user = ctx.author.name
    lowuser = (user.lower()).replace("@","")

 # Reviso que el comando haya sido usado por el dueño del canal, un moderador o el usuario este consultando sus propias fichas y no la de otros.
    if (lowuser == autor or autor in [x.lower() for x in MODS ] or autor == CHANNEL[0].replace("#","")):

 # Valido la entrada.
        if ( allowed_chars(lowuser) ):
            cantTotal = get_fichas_by_user(lowuser)
            pluralTotal = Plurals(cantTotal)

         # Si no tiene fichas lo notifico.   
            if (cantTotal == None or cantTotal[0] == 0):
                MENSAJE = "El usuario %s no tiene fichas." % (user)

         # Si las tiene pongo la cantidad en el mensaje.
            else:
                MENSAJE = "%s tiene %d %s." % (user, cantTotal[0], pluralTotal)
                
        else:
            MENSAJE = "Nombre de usuario no valido, si tenes dudas de como usar el comando, usa el comando !help."
 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s no seas chusma! No tenes los privilegios para mirar las fichas de otros!" % (ctx.author.name)

    await ctx.send(MENSAJE)
    printear(MENSAJE)

###########################################################################################################################
    

# Muestra la cantidad de fichas de un usuario
@ArcadesBot.command()
async def cantgastadas(ctx, user: str = None):
    
 #Si no hay un user en la entrada, user sera el usuario que ejecuto el comando.
    autor = ctx.author.name.lower()
    if user == None:
        user = ctx.author.name
    lowuser = (user.lower()).replace("@","")

 # Reviso que el comando haya sido usado por el dueño del canal, un moderador o el usuario este consultando sus propias fichas y no la de otros.
    if (lowuser == autor or autor in [x.lower() for x in MODS ] or autor == CHANNEL[0].replace("#","")):

 # Valido la entrada.
        if ( allowed_chars(lowuser) ):
            cantTotal = get_gastadas_by_user(lowuser)
            pluralTotal = Plurals(cantTotal)

         # Si no hasto fichas lo notifico.   
            if (cantTotal == None or cantTotal[0] == 0):
                MENSAJE = "El usuario %s no gastó fichas." % (user)

         # Si gastó pongo la cantidad en el mensaje.
            else:
                MENSAJE = "%s gastó %d %s." % (user, cantTotal[0], pluralTotal)
                
        else:
            MENSAJE = "Nombre de usuario no valido, si tenes dudas de como usar el comando, usa el comando !help."
 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s no seas chusma! No tenes los privilegios para mirar las fichas gastadas de otros!" % (ctx.author.name)

    await ctx.send(MENSAJE)
    printear(MENSAJE)
###########################################################################################################################

# Muestra el usuario con mas fichas disponibles.
@ArcadesBot.command()
async def usuariotop(ctx):
    
 #Obtengo el usuario top de la base de datos.
    res = get_top_by_fichas()
 #Chequeo si hay usuarios en la base y tienen fichas.
    if (res != None and res[1] >= 0):
        user = res[0]
        cantTotal = res[1]
        pluralTotal = Plurals(cantTotal)
        MENSAJE = "El niño rico del canal es @%s con %d %s" % (user, cantTotal, pluralTotal)
    else:
        MENSAJE = "Nadie tiene fichas, este Arcade se va a la bancarrota!"  
    
    await ctx.send(MENSAJE)
    printear(MENSAJE)

###########################################################################################################################

# Muestra el usuario que mas fichas gastó.
@ArcadesBot.command()
async def gastadortop(ctx):
    
 #Obtengo el usuario top de la base de datos.
    res = get_top_gastadas()
    
 #Chequeo si hay usuarios en la base y tienen fichas.
    if (res != None and res[1] >= 0):
        user = res[0]
        cantTotal = res[1]
        pluralTotal = Plurals(cantTotal)
        MENSAJE = "El usuario que mas fichas se gasto es @%s con %d %s" % (user, cantTotal, pluralTotal)
    else:
        MENSAJE = "Nadie gasto fichas, ¿para que se las guardan? Solo sirven en este arcade!"
    
    await ctx.send(MENSAJE)
    printear(MENSAJE)
###########################################################################################################################

# Muestra el total de fichas disponibles para usar actualmente.
@ArcadesBot.command()
async def totalfichas(ctx):
    
 #Obtengo el total de fichas de la base de datos.
    res = total_fichas_disponibles()
    
 #Chequeo si hay resultados y tienen fichas.
    if (res != None and res[0] > 0):
        cantTotal = res[0]
        pluralTotal = Plurals(cantTotal)
        MENSAJE = "Los usuarios tienen un total de %d %s en sus bolsillos" % (cantTotal, pluralTotal)
    else:
        MENSAJE = "Nadie tiene fichas, este Arcade se va a la bancarrota!"  
    
    await ctx.send(MENSAJE)
    printear(MENSAJE)

###########################################################################################################################

# Deja la cantidad de fichas de un usuario en 0, el comando puede ser util si se banea a alguien con fichas.
@ArcadesBot.command()
async def vaciarfichas(ctx, user: str = None):

 # Reviso que el comando haya sido usado por un moderador o el dueño del canal.
    autor = ctx.author.name.lower()
    if (ctx.author.name.lower() in [x.lower() for x in MODS] or autor == CHANNEL[0].replace("#","")):

     # Convierto el user a minusculas y verifico la entrada.
     # Admito que el comando sea usado con @user para aprovechar el autocompletado, se le saca el @ para ser almacenado en la DB.
        lowuser = (user.lower()).replace("@","")
        if (allowed_chars(lowuser)):
    
         # Chequeo si el usuario tiene fichas.
            cantTotal = get_fichas_by_user(lowuser)

            if (cantTotal!= None and cantTotal[0] > 0):

                data = [lowuser, 0]

                update_fichas(data)

                MENSAJE = "%s fue despropiado de sus fichas!" % (user)

            else:
                MENSAJE = "%s no tenía ninguna ficha" % (user)

        else:
            MENSAJE = "Nombre de usuario no valido, si tenes dudas de como usar el comando, usa el comando !help."

 # Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, no tenés los privilegios para usar este comando." % (ctx.author.name)

    printear(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################

# Comando que retorna el enlace del repositorio de este bot.
@ArcadesBot.command()
async def repo(ctx):
    MENSAJE = "Queres saber como esta hecho Arcadesbot? Aca tenes el repositorio: https://github.com/DiktatorShadaloo/ArcadesBot"
    await ctx.send(f"%s" % MENSAJE)
###########################################################################################################################

####################################################### MAIN ##############################################################

def run_BOT():
    ArcadesBot.run()

def main_BOT():
    asyncio.run(run_BOT())
