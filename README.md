# Honeybee Inc.

#Flujo del programa:
El programa se desarrolla desde el archivo "app.py" donde se encuentran las app.route y sus respectivos templates en .HTML para su funcionamiento.
Se tiene un archivo "funciones.py" donde se guardan las funciones que el programa utiliza para cada busqueda requerida.
Cada ruta de los app.route tiene su propio codigo y templates, las rutas que requieren un valor para su funcionamiento tienen un pedido del parametro.

#Estructuras utilizadas
Principalmente tenemos un archivo con formato .CSV que es la informacion necesaria para ser procesada por los archivos .PY y asi enviarlas a los distintos templates .HTML para la visualizacion del usuario.

#¿Como se usa el programa?
Al acceder a la pagina principal nos muestra un saludo, en caso de que el archivo "ventas.csv" contenga algun error este mismo va a aparecer en la pantalla en vez del saludo, impidiendo que se realice cualquier tarea hasta que se solucione el error correspondiente.


Si no se encuentra error alguno se ofrecen las opciones "Saludar", "Ingresar", "Registrarse":
-Saludar: Se ingresa un nombre y devuelve un saludo.

-Ingresar: Permite iniciar sesion mediante un usuario y contraseña para poder utilizar las funciones del programa, estos valores estan guardados en el archivo llamado "usuarios".

-Registrarse: Permite el registro de un usuario nuevo.


Una vez ingresado con un usuario y contraseñas validos, la pantalla nos va a saludar y nos muestras las ultimas 10 ventas que se realizaron y en una barra de navegacion tenemos varias opciones "Ultimas Ventas", "Productos por Cliente", "Clientes por Producto", "Productos mas vendidos", "Mejores clientes":
-Ultimas ventas: Nos muestra las ultimas 20 ventas realizadas.

-Productos por cliente: Ingresamos el nombre del cliente, o al menos 3 caracteres para la busqueda, si en el sistema solo se encuentra 1 coincidencia a la busqueda nos mostrara directamente la tabla con los productos comprados por el cliente, en caso de que se hayan encontrado mas coincidencias no mostrara un listado de los clientes, al hacer click sobre alguno nos mostrara la tabla de compras del mismo.

-Clientes por producto: Ingresamos el nombre del producto, o al menos 3 caracteres para la busqueda, tiene el mismo funcionamiento que para los Clientes, si se encuentra mas de 1 producto nos muestra un listado sino directamente nos dirige a la tabla de los clientes que compraron dicho producto.

-Productos mas vendidos: Nos muestra un listado de los 10 productos mas vendidos.

-Mejores clientes: Nos muestra un listado con los 10 clientes que mas gastaron.