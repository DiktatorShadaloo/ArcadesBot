# ArcadesBot
Sucesor espiritual de el Fichinbot empezado por mksh, Arcadesbot recicla partes de Fichinbot hechas por mi, el resto fue rehecho de 0.

Arcadesbot esta diseñado para usarse en un canal [Twitch](https://www.twitch.tv) y su fin es mantener un registro de "fichas arcade" que pueden ser agregadas o canjeadas a un usuario por medio de comandos, automaticamente con el evento de donación de bits o usando canjeo de recompensas, todo esto utilizando la libreria [TwitchIO](https://github.com/TwitchIO/TwitchIO).

Arcadesbot tambien es capaz de banear autoamticamente a usuarios que en el chat escriban frases o palabras que se incluyan en la seccion [BANNED_MESSAGES] util para banear bots que hagan spam.

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