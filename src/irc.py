import socket
import re
from datetime import datetime
from config.config import *
import asyncio
from threading import Thread

# the twitch irc server to send a chat message.
NICK= BOT_NICK.lower()
PASS = "oauth:" + BOT_TOKEN
HOST = "irc.chat.twitch.tv"
PORT = 6667

sock = socket.socket()
sock.connect((HOST, PORT))
sock.send("PASS {}\r\n".format(PASS).encode("utf-8"))
sock.send("NICK {}\r\n".format(NICK).encode("utf-8"))
sock.send("JOIN {}\r\n".format(CHANNEL[0].lower()).encode("utf-8"))

# Envia un mensaje al chat
def chat(MENSAJE):
    sock.send(("PRIVMSG %s :" % CHANNEL[0].lower() + MENSAJE +"\r\n").encode("utf-8"))

# Banea a un usuario
def ban(USER):
    '''
    Ban a user from the current channel.
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    '''
    sock.send(("PRIVMSG %s :" % CHANNEL[0].lower() + "/ban " + USER +"\r\n").encode("utf-8"))

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
               MENSAJE = "Queres saber como esta hecho Arcadesbot? Aca tenes el repositorio: <Aca va un link>"
               chat(MENSAJE)
               REPO_time = datetime.now()

def run_IRC():
     RIPthread = Thread(target = RIP, args = ())
     REPOthread = Thread(target = repo, args = ())
     RIPthread.start()
     REPOthread.start()
     while True:
          response = sock.recv(1024).decode("utf-8")
          print(response)
          if response == "PING :tmi.twitch.tv\r\n":
               print ('PONG')
               sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
          else:
               username = re.search(r"\w+", response).group(0)  
               if "Buy followers, primes and viewers on" in response:
                    ban(username)
                    msg = "%s, agarra todo eso, hace un rollito y metetelo bien por el ****" % username
                    chat(msg)
                    
               
               print(username)

          


def main_IRC():
    asyncio.run(run_IRC())