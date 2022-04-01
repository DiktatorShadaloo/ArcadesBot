from random import randint
import socket
import re
from datetime import datetime
from config.config import *
import asyncio
from threading import Thread
from time import sleep
from src.common_functions import printear

# the twitch irc server to send a chat message.
NICK= BOT_NICK.lower()
PASS = "oauth:" + BOT_TOKEN
HOST = "irc.chat.twitch.tv"
PORT = 6667

def connect():
     sock = socket.socket()
     sock.connect((HOST, PORT))
     sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
     sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
     sock.send("JOIN {}\r\n".format(CHANNEL[0].lower()).encode("utf-8"))
     return sock


def reconnect():
     it =0
     connected = False
     sock = socket.socket()
     printear( "Conexion del cliente perdida, intentando reconectar..." ) 
     while connected == False and it <= 15:   
          try:  
               sock = socket.socket()
               sock.connect((HOST, PORT))
               sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
               sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
               sock.send("JOIN {}\r\n".format(CHANNEL[0].lower()).encode("utf-8"))
               connected = True  
               printear( "reconexion exitosa" )  
               return sock
          except socket.error:  
               sleep(1)
               it = it + 1
     if it >15:
          printear ("No se pudo reconectar, revisa tu conexion a internet e intenta reiniciar el programa.")

# Envia un mensaje al chat
def chat(MENSAJE):
     sock2 = connect()
     try:
          sock2.send(("PRIVMSG %s :" % CHANNEL[0].lower() + MENSAJE +"\r\n").encode("utf-8"))
     except socket.error:
          sock2 = reconnect()
          sock2.send(("PRIVMSG %s :" % CHANNEL[0].lower() + MENSAJE +"\r\n").encode("utf-8"))

# Banea a un usuario
def ban(USER):
     MENSAJE = "/ban " + USER
     chat(MENSAJE)
     ''' try:
          sock.send(("PRIVMSG %s :" % CHANNEL[0].lower() + "/ban " + USER +"\r\n").encode("utf-8"))
     except socket.error:
          reconnect()
          ban(USER)
     '''
def mensajeProgramado(tiempo):
     it= randint(0, len(AUTOMATIC_MESSAGES)-1)
     starting_time = datetime.now()
     while True:
          difference = datetime.now() - starting_time
          if difference.total_seconds() > tiempo:
               MENSAJE = AUTOMATIC_MESSAGES[it]
               chat(MENSAJE)
               it= (it+1) % len(AUTOMATIC_MESSAGES)
               starting_time = datetime.now()

# Funcion concurrente para hacer homenaje al caido Fichinbot U_U
def RIP ():
     RIP_time = datetime.now()
     while True:
          difference = datetime.now() - RIP_time
          if difference.total_seconds() > 7800:
               MENSAJE = "Descansa en paz Fichinbot riPepperonis"
               chat(MENSAJE)
               RIP_time = datetime.now()

# Funcion concurrente para compartir el repositorio.
def repo():
     REPO_time  =  datetime.now()
     while True:
          difference =  datetime.now() - REPO_time
          if difference.total_seconds() > 5400:
               MENSAJE = "Queres saber como esta hecho Arcadesbot? Aca tenes el repositorio: https://github.com/DiktatorShadaloo/ArcadesBot"
               chat(MENSAJE)
               REPO_time = datetime.now()

# Funcion concurrente para enviar PING al servidor y asi evitar desconexiones o intentar reconectar mas frecuentemente.
def PING():
     global sock
     PING_time = datetime.now()
     while True:
          difference = datetime.now() - PING_time
          if difference.total_seconds() > 600:
               try:
                    sock.send("PING :tmi.twitch.tv\r\n".encode("utf-8"))
                    PING_time = datetime.now()
               except socket.error:
                   sock = reconnect()

sock = connect()

def run_IRC():
     global sock
     RIPthread = Thread(target = RIP, args = ())
     RIPthread.start()
     #REPOthread = Thread(target = repo, args = ())
     #REPOthread.start()
     PINGthread = Thread(target = PING, args = ())
     PINGthread.start()
     if len (AUTOMATIC_MESSAGES) >0:
          #Cada cuantos segundos se enviara un mensaje automatico.
          tiempo = 3600
          MENSAJESthread = Thread(target = mensajeProgramado, args = (tiempo,))
          MENSAJESthread.start()
     while True:
          try:
               response = sock.recv(1024).decode("utf-8")
               if response == "PING :tmi.twitch.tv\r\n":
                    sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
               else:
                    username = re.search(r"\w+", response).group(0)
               
                    for x in BANNED_MESSAGES:
                         if x.lower() in response.lower():
                              ban(username)
                              msg = "%s, agarra todo eso, hace un rollito y metetelo bien por el ****" % username
                              chat(msg)
                              break
          except socket.error:
               sock = reconnect()


def main_IRC():
    asyncio.run(run_IRC())