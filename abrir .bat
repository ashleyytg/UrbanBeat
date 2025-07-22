:: Este script .bat es una herramienta de automatización para simplificar el proceso de ejecutar tu aplicación.
::En lugar de abrir varias ventanas de terminal y escribir comandos manualmente, este script lo hace todo por ti.
@echo off
:: Desactiva la visualización de los comandos en la consola. Esto hace que la ejecución sea más limpia,
:: mostrando solo la salida de los programas y no los comandos que se están ejecutando.

set PYTHONUTF8=1
:: Configura una variable de entorno para Python. Esto asegura que Python maneje correctamente
:: caracteres UTF-8 (como acentos o caracteres especiales) al interactuar con el sistema,
:: lo cual es importante para evitar problemas de codificación.

title UrbanBeat Launcher 🚀
:: Establece el título de la ventana de la consola. Esto ayuda a identificar fácilmente
:: la ventana de nuestro lanzador entre otras ventanas de terminal abiertas.

:: Ejecutar backend Flask en nueva ventana
start cmd /k "cd /d %~dp0 && python backend.py"
:: Este comando es crucial para iniciar el servidor Flask (tu backend) en una nueva ventana de consola.
:: - `start cmd /k`: Abre una nueva ventana de comandos (`cmd`) y ejecuta el comando especificado,
::                   manteniendo la ventana abierta (`/k`) después de la ejecución.
:: - `cd /d %~dp0`: Cambia el directorio actual (`cd`) a la ubicación donde se encuentra este script `.bat`.
::                  `%~dp0` es una variable especial que representa la ruta completa del directorio del script.
:: - `&&`: Es un operador que encadena comandos; el segundo comando se ejecuta solo si el primero fue exitoso.
:: - `python backend.py`: Ejecuta tu script de backend Flask.

:: Esperar 2 segundos para que arranque Flask
timeout /t 2 > nul
:: Este comando introduce una pausa de 2 segundos. Es una "espera estratégica" para dar tiempo a que el servidor Flask
:: se inicie completamente antes de que el navegador intente conectarse a él.
:: - `timeout /t 2`: Espera 2 segundos.
:: - `> nul`: Redirige la salida del comando `timeout` (el conteo regresivo) a la nada,
::            manteniendo la consola limpia.

:: Abrir visualizador en navegador
start http://localhost:8000/visualizador.html
:: Este comando abre automáticamente tu archivo HTML principal en el navegador web predeterminado.
:: - `start`: Abre el archivo o URL especificado.
:: - `http://localhost:8000/visualizador.html`: Es la dirección local de tu archivo HTML, servido por el servidor web.

:: Ejecutar servidor web para HTML
start cmd /k "cd /d %~dp0 && python -m http.server 8000"
:: Este comando inicia un servidor web simple de Python para servir tus archivos HTML.
:: Es necesario porque los navegadores modernos tienen restricciones de seguridad (CORS) que impiden
:: que los archivos HTML locales hagan solicitudes a APIs (como tu backend Flask) directamente.
:: - `python -m http.server 8000`: Inicia un servidor HTTP en el puerto 8000, sirviendo los archivos del directorio actual.

echo Todo listo 🟢
:: Muestra un mensaje en la consola del lanzador, indicando que todos los servicios se han iniciado con éxito.

exit
:: Cierra la ventana de la consola del lanzador una vez que todos los comandos han sido ejecutados.
