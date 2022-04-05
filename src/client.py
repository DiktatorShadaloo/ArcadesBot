from twitchio.ext import pubsub
from config.config import *
from datetime import datetime
from src.db_manager import *
from src.common_functions import *
import twitchio
import asyncio
from src.irc import chat

users_oauth_token = CHANNEL_TOKEN
users_channel_id = CHANNEL_ID

client = twitchio.Client(token=CHANNEL_TOKEN)
client.pubsub = pubsub.PubSubPool(client)

@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    '''
    if event.reward.title == REWARD_INSERT_COINS:
     #Obtengo el user que canjeo la recompensa y las fichas 
        user  = event.user.name.lower()
        arrayinput = event.input.title().split(";", 1)
        fichas_gastadas = (arrayinput[0]).replace(" ","")
     #Chequeo que la fichas sean un entero mayor a 0
        if fichas_gastadas.isdigit() and int(fichas_gastadas)>0 :
            fichas_gastadas = int(fichas_gastadas)

         #Chequeo que la fichas no superen al maximo definido por el dueño del canal.
            if fichas_gastadas <= FICHAS_MAXIMAS:
                if len (arrayinput) == 2:
                    juego = event.input.title().split(";", 1)[1]
                 #Chequeo que el nombre del juego no sea vacio. 
                    if juego. replace(" ","") != "":
                    #Chequeo que el usuario tenga la cantidad de fichas suficientes y actualizo en la base de datos.
                        restantes = actualizar_fichas(event.user.name.lower(),-fichas_gastadas)
                        if (restantes>=0):
                            fecha = datetime.strptime(str(event.timestamp).split("+", 4)[0], '%Y-%m-%d %H:%M:%S.%f').strftime("%H:%M:%S %d-%m-%y")
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
                            MENSAJE = "El usuario %s no tiene fichas suficientes!" % (user)
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
       # chat(MENSAJE)
        '''
    if (REWARD_BUY_COIN != "" and event.reward.title == REWARD_BUY_COIN):
        fichas = 1
        user  = event.user.name.lower()
     # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
        cantTotal = actualizar_fichas(user,fichas)
     # Corrijo los plurales para el mensaje de chat.
        pluralTotal = Plurals(cantTotal)
        pluralAgregadas = Plurals(fichas)
        fecha = datetime.now().strftime("%H:%M:%S %d-%m-%y")
        with open('UltimaFichaAdquirida.txt', 'w') as f:
            f.write(fecha)
        
        MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (user, fichas, pluralAgregadas, cantTotal, pluralTotal)
        printear(MENSAJE)
        chat(MENSAJE)
        # await client._connection.send(("PRIVMSG %s :") % CHANNEL[0].lower() +MENSAJE)

@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
 # Convierto user a minusculas y reviso la entrada. 
    lowuser = event.user.name.lower()
    bits = event.bits_used
 #Reviso que el monto alcance para comprar una ficha.           
    if (bits >= PRECIO_BITS):
        fichas = bits // PRECIO_BITS
     # Actualizo la cantidad de fichas y obtengo el total para devolverlo en un mensaje de chat.            
        cantTotal=actualizar_fichas(lowuser,fichas)
     # Corrijo los plurales para el mensaje de chat.
        pluralTotal = Plurals(cantTotal)
        pluralAgregadas = Plurals(fichas)
        MENSAJE = "%s recibió %d %s. Ahora tiene un total de %d %s." % (lowuser, fichas, pluralAgregadas, cantTotal, pluralTotal)

    else:
        MENSAJE = "¡Oh no! Esos bits no son suficientes para comprar una ficha, cada ficha cuesta %d bits." % (PRECIO_BITS)

    printear(MENSAJE)
    chat(MENSAJE)
    
async def listener():
    topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id],
        pubsub.bits(users_oauth_token)[users_channel_id]
    ]
    await client.pubsub.subscribe_topics(topics)
    # await client.start()

def run_CLIENT():
    printear("Comienza el cliente")
    client.loop.create_task(listener())
    #client.loop.run_until_complete(listener())
    client.run()

def main_CLIENT():
 asyncio.run(run_CLIENT())