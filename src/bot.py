from distutils.sysconfig import PREFIX
from enum import auto
from twitchio.ext import commands
from src.db_manager import *
from src.common_functions import *
import asyncio
from config.config import *

ArcadesBot = commands.Bot( 
    token=BOT_TOKEN, 
    prefix=BOT_PREFIX, 
    initial_channels= CHANNEL)

@ArcadesBot.event()   
async def event_ready():
    print(f"Logged in as {BOT_NICK} in {CHANNEL}.")

################################################################## COMANDOS ###############################################

# Comando de ayuda
@ArcadesBot.command()
async def help(ctx):
    MENSAJE = "Los comandos de uso son: !agregarfichas <usuario> <fichas> | !agregarxsub <usuario> | !agregarxdonacion <usuario> <monto> | !sacarfichas <usuario> <fichas> | !cantfichas <usuario> | !usuariotop | !vaciarfichas <usuario> | !repo"
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

    print(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################

# Comando para agregar fichas a un usuario
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

        #Reviso que el monto alcance para comprar una ficha.           
            if (int(bits) > PRECIO_BITS):
                fichas = int(bits) // PRECIO_BITS

            # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
                cantTotal=actualizar_fichas(lowuser,fichas)

            # Corrijo los plurales para el mensaje de chat.
                pluralTotal = Plurals(cantTotal)
                pluralAgregadas = Plurals(fichas)
                MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

            else:
                MENSAJE = "Oh no! Esos bits no son suficientes para comprar una ficha, te daremos una ficha por cada %d bits que dones!" % (PRECIO_BITS)

        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."
 
 #Si no tiene los privilegios lo notifico.
    else:
            MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    print(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################  

# Comando para agregar fichas a un usuario que se hizo sub (la idea es que el client lo haga solo pero se implementa por las dudas).
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
    print(MENSAJE)
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
                if (float(dinero) > PRECIO_FICHA):
                    fichas = float(dinero) // PRECIO_FICHA
                    
                # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
                    cantTotal=actualizar_fichas(lowuser,fichas)
                # Corrijo los plurales para el mensaje de chat.
                    pluralTotal = Plurals(cantTotal)
                    pluralAgregadas = Plurals(fichas)

                    MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)

                else:
                    MENSAJE = "Oh no! Ese monto no es suficiente para comprar una ficha, cada ficha cuesta %s dolares!" % (str(PRECIO_FICHA))
                
        else: 
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

# Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, No tenés los privilegios para usar este comando." % (ctx.author.name)

    await ctx.send(MENSAJE)
    print(MENSAJE)
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

                MENSAJE = "%s gastó %d %s. Le queda un total de %d %s." % (user, fichas, pluralSacadas, cantTotal, pluralTotal)
        # Si el usuario no tiene fichas suficientes lo notifico. 
            else:
                MENSAJE = ("Se ha intentado sacar %d %s, pero %s no tiene fichas suficientes") % (fichas, pluralSacadas, user)

        else:
            MENSAJE = "Los datos ingresados no son correctos, si tenes dudas de como usar el comando, usa el comando !help."

# Si no tiene los privilegios lo notifico.
    else:
        MENSAJE = "%s, no tenés los privilegios para usar este comando." % (ctx.author.name)
    
    print(MENSAJE)
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
    print(MENSAJE)
###########################################################################################################################

# Muestra el usuario con mas fichas.
@ArcadesBot.command()
async def usuariotop(ctx):
    
#Obtengo el usuario top de la base de datos.
    res = get_top_by_fichas()
    user = res[0]
    cantTotal = res[1]
#Chequeo si hay usuarios en la base y tienen fichas.
    if (res != None and cantTotal >= 0):

        pluralTotal = Plurals(cantTotal)
        MENSAJE = "El niño rico del canal es @%s con %d %s" % (user, cantTotal, pluralTotal)
    else:
        MENSAJE = "Nadie tiene fichas, este Arcade se va a la bancarrota!"  
    
    await ctx.send(MENSAJE)
    print(MENSAJE)
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

    print(MENSAJE)
    await ctx.send(MENSAJE)
###########################################################################################################################

# Comando que retorna el enlace del repositorio de este bot.
@ArcadesBot.command()
async def repo(ctx):
    MENSAJE = "Queres saber como esta hecho Arcadesbot? Aca tenes el repositorio: <Aca va un link>"
    await ctx.send(f"%s" % MENSAJE)
###########################################################################################################################

####################################################### MAIN ##############################################################

def run_BOT():
    ArcadesBot.run()

def main_BOT():
    asyncio.run(run_BOT())
