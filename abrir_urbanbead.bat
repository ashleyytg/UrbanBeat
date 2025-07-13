@echo off
set PYTHONUTF8=1
title UrbanBeat Launcher 🚀

:: Ejecutar backend Flask en nueva ventana
start cmd /k "cd /d %~dp0 && python backend.py"

:: Esperar 2 segundos para que arranque Flask
timeout /t 2 > nul

:: Abrir visualizador en navegador
start http://localhost:8000/visualizador.html

:: Ejecutar servidor web para HTML
start cmd /k "cd /d %~dp0 && python -m http.server 8000"

echo Todo listo 🟢
exit
