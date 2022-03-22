# ArcadesBot
Sucesor espiritual de el Fichinbot empezado por mksh, Arcadesbot recicla partes de Fichinbot hechas por mi, el resto fue rehecho de 0.

Arcadesbot esta diseñado para usarse en un canal [Twitch](https://www.twitch.tv) y su fin es mantener un registro de "fichas arcade" que pueden ser agregadas o canjeadas a un usuario por medio de comandos, automaticamente con el evento de donación de bits o usando canjeo de recompensas, todo esto utilizando la libreria [TwitchIO](https://github.com/TwitchIO/TwitchIO).

Arcadesbot tambien es capaz de banear automaticamente a usuarios que en el chat escriban frases o palabras que se incluyan en la seccion [BANNED_MESSAGES] util para banear bots que hagan spam.

## Comandos Disponibles

### Comandos solo para usuarios con privilegios:

Comando para agregar fichas a un usuario: 

`!agregarfichas <usuario> <fichas>`   

Comando para agregar fichas a un usuario que se hizo sub:

 `!agregarxsub <usuario>`

Comando para agregar fichas a un usuario que regalo subs:

 `!agregarxgifts <usuario> <cantidad_regaladas> `

 Comando para agregar fichas a un usuario que hizo una donacion, como divisa estandar se usa el dolar:
 
  `!agregarxdonacion <usuario>  <monto>`

Comando para agregar fichas a un usuario que donó bits:

`!agregarxbits <usuario>  <bits> `

Comando para sacar fichas a un usuario:

`!sacarfichas<usuario> <fichas>`

Deja la cantidad de fichas de un usuario en 0, el comando puede ser util si se banea a alguien con fichas:

`!vaciarfichas <usuario>`

Muestra la cantidad de fichas de un usuario :

`!cantfichas <usuario>`

Muestra la cantidad de fichas que gastó un usuario :

`!cantgastadas <usuario>`


### Comandos que pueden usar usuarios sin necesidad de privilegios:

Comando  para mostrar los comandos disponibles en el chat :

`!help`.

Muestra la cantidad de fichas propias :

`!cantfichas`

Muestra la cantidad de fichas propias que gastó un usuario :

`!cantgastadas`

Muestra el usuario con mas fichas disponibles. :

`!usuariotop`

Muestra el usuario con mas fichas gastadas:

 `!gastadortop​​​​​​​​​​​​​​ `

Muestra el total de fichas disponibles para usar actualmente. (La sumatoria de fichas entre todos los usuarios) :

`!totalfichas​​​​​​​​​​​​​​​​​​​​​ `

## Base de Datos
La base de datos es creada automaticamente dentro de la carpeta ArcadesBot/db

## Configuración 
Una vez descargado ArcadesBot, debemos renombrar "config example.ini" a "config.ini" y empezar a completar todas las variables.

```ini
; Estos campos deben ser completados con tus valores antes de utilizar Arcadesbot, de lo contrario no funcionará.
[BOT]
bot_nick = Diktabot

;Token de autenticacion OATH del bot para poder conectarse automaticamente a twitch. Para mas info de como obtenerlo leer el README.
bot_token = po09x0geme2hro817tznfd9tnlmlop
; Simbolo que se utilizara como prefijo para invocar comandos, ! es el utilizado por defecto.
bot_prefix = !

; Lista de mods que podran usar el bot incluyendo al propio bot como moderador, cada mod debe agregarse en una linea nueva, estos son solo de ejemplo, sustituyelos por los tuyos. 
[MODS]
Jung3MOD
AUTO__KRATISCHER_mod
Fehlender180222MOD
Diktabot

[CHANNEL]
; Canal en el que se utilizara el bot, por ejemplo "#arcades_ushuaia".
channel_name = #arcades_ushuaia

;Token de autenticacion OATH del canal en el que se utilizara el bot para que el cliente se conecte automaticamente a twitch. Para mas info de como obtenerlo leer el README.
channel_token = tyuimys1uo39qfz3be2jxea9874j0f

; ID del canal necesario para la deteccion de eventos como uso de recompensas o donaciones. Para mas info de como obtenerlo leer el README.
channel_id = 561985295

; Cantidad de fichas que se consiguen por comprar una subscripcion.
fichas_x_sub = 5

; Costo en dolares de una ficha, cada donacion debe ser igual o mayor a este monto para obtener fichas.
precio_ficha = 0.25

; Costo en bits de una ficha. cada donacion debe ser igual o mayor a estos bits para obtener fichas.
precio_bits = 25

; Nombre de la recompensa que se utilizara para poner fichas a un juego, el formato de entrada debe ser "fichas; juego", por ejemplo " 2; Street fighter 2".
reward_insert_coins = InsertarFichas

; Nombre de la recompensa que se utilizara para comprar una ficha, podes dejar este campo vacio si no queres que se compren fichas con puntos.
reward_buy_coin = ComprarFicha

; Cantidad de fichas maximas que un usuario pueda ponerle a un juego.
fichas_maximas = 3

; Lista de mensajes o palabras para que el bot banee al usuario automaticamente, util contra bots haciendo spam.
[BANNED_MESSAGES]
Buy followers, primes and viewers on
```