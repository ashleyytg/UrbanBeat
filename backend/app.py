# backend/app.py

# --- Importaciones de Librerías ---
# Flask es el microframework web que usaremos para crear el servidor.
from flask import Flask, jsonify, request
# Flask-CORS es una extensión de Flask que permite manejar las peticiones
# de "Cross-Origin Resource Sharing" (CORS). Esto es crucial para que
# el frontend (la página web que se sirve desde GitHub Pages o tu index.html local)
# pueda hacer peticiones a este backend que corre en un puerto diferente (5000).
from flask_cors import CORS
# Requests es una librería para hacer peticiones HTTP (GET, POST, etc.) a otras páginas web o APIs.
# La usaremos tanto para el scraping como para las llamadas a Nominatim.
import requests
# BeautifulSoup4 (bs4) es una librería para analizar documentos HTML y XML.
from bs4 import BeautifulSoup
import os
# python-dotenv es una librería para cargar variables de entorno desde un archivo .env.
# Esto es esencial para manejar claves API y otra información sensible de forma segura,
# sin subirla a GitHub.
from dotenv import load_dotenv

# --- Configuración Inicial de la Aplicación Flask ---

# Carga las variables de entorno desde el archivo .env.
load_dotenv()

# Crea una instancia de la aplicación Flask.
# "__name__" es una variable especial de Python que se refiere al nombre del módulo actual.
# Flask lo usa para saber dónde está tu aplicación y cómo encontrar recursos.
# NO NECESITAS CAMBIAR ESTO. Es una convención estándar.
app = Flask(__name__)

# Habilita CORS para toda la aplicación Flask.
# Esto permite que tu frontend (que se ejecuta en un "origen" diferente, ej. un archivo local o GitHub Pages)
# pueda hacer peticiones a este backend (que se ejecuta en localhost:5000).
CORS(app)

# --- RUTAS (Endpoints) de tu API Backend ---
# Cada función decorada con @app.route() es un "endpoint" de tu API.
# Cuando tu frontend haga una petición a esa URL, se ejecutará la función asociada.

@app.route('/')
def home():
    """
    Ruta de inicio del servidor.
    Simplemente devuelve un mensaje para confirmar que el servidor está funcionando.
    Acceso: http://localhost:5000/
    """
    return "Servidor UrbanBeat en funcionamiento. Accede a /scrape-municipalidad o /geocode."

@app.route('/scrape-municipalidad', methods=['GET'])
def scrape_municipalidad():
    """
    Ruta para realizar web scraping de noticias o eventos de una municipalidad.
    Acceso: http://localhost:5000/scrape-municipalidad
    Método HTTP: GET
    """
    # --- PARÁMETROS A PERSONALIZAR PARA EL SCRAPING ---
    # 1. URL de la página a scrapear:
    #    Cambia esta URL por la página específica de noticias, eventos o datos
    #    de la Municipalidad de Lima, Callao, etc., que quieras obtener.
    url_a_scrapear = "https://www.gob.pe/cultura" # <--- ¡CAMBIA ESTA URL!

    try:
        # Realiza una petición GET a la URL.
        # timeout=10: Espera un máximo de 10 segundos por la respuesta.
        response = requests.get(url_a_scrapear, timeout=10)
        # raise_for_status() lanza una excepción si la petición HTTP no fue exitosa (ej. 404, 500).
        response.raise_for_status()
        # Parsea el contenido HTML de la respuesta usando BeautifulSoup y el parser lxml (rápido).
        soup = BeautifulSoup(response.text, 'lxml')

        noticias = []
        # --- SELECTORES CSS A PERSONALIZAR ---
        # 2. Inspectores de Elementos (F12 en el navegador):
        #    Esta es la parte más CRÍTICA del scraping. Necesitas abrir la página
        #    que quieres scrapear en tu navegador, presionar F12 (o clic derecho -> Inspeccionar),
        #    y usar la herramienta de selección de elementos para encontrar los selectores CSS
        #    correctos que identifiquen los bloques de noticias/eventos, sus títulos, enlaces, etc.
        #    Los selectores '.item-noticia-simple', 'h3 a', 'p' son EJEMPLOS y
        #    probablemente NO funcionen en la página real de la municipalidad.

        # Itera sobre cada "item" que coincida con el selector CSS.
        # Este selector debe apuntar a un contenedor que agrupe una noticia/evento completa.
        for item in soup.select('.item-noticia-simple'): # <--- ¡CAMBIA ESTE SELECTOR!
            # Dentro de cada item, busca el título, enlace y resumen usando selectores más específicos.
            titulo_tag = item.select_one('h3 a') # <--- ¡CAMBIA ESTE SELECTOR (para el título/enlace)!
            enlace = titulo_tag['href'] if titulo_tag and 'href' in titulo_tag.attrs else None
            resumen_tag = item.select_one('p') # <--- ¡CAMBIA ESTE SELECTOR (para el resumen)!

            noticias.append({
                'titulo': titulo_tag.get_text(strip=True) if titulo_tag else 'N/A',
                'enlace': enlace,
                'resumen': resumen_tag.get_text(strip=True) if resumen_tag else 'N/A'
            })
        # Devuelve los datos como un JSON.
        return jsonify(noticias)

    except requests.exceptions.RequestException as e:
        # Manejo de errores si hay problemas al acceder a la URL (red, DNS, etc.)
        return jsonify({"error": f"Error al acceder o scrapear la URL: {e}"}), 500
    except Exception as e:
        # Manejo de errores si hay problemas al parsear el HTML o al extraer datos.
        return jsonify({"error": f"Error inesperado al parsear o extraer datos: {e}"}), 500

@app.route('/geocode', methods=['GET'])
def geocode_address():
    """
    Ruta para geocodificar una dirección (convertir dirección a coordenadas latitud/longitud).
    Utiliza la API de Nominatim (OpenStreetMap).
    Acceso: http://localhost:5000/geocode?address=TU_DIRECCION_AQUI
    Método HTTP: GET
    Parámetros de consulta: 'address' (obligatorio)
    """
    # Obtiene el valor del parámetro 'address' de la URL (ej. ?address=Av. Arequipa 123).
    address = request.args.get('address')
    if not address:
        # Si no se proporciona una dirección, devuelve un error 400 (Bad Request).
        return jsonify({"error": "Parámetro 'address' es requerido"}), 400

    # --- CONFIGURACIÓN DE NOMINATIM ---
    # Nominatim es una API gratuita de OpenStreetMap. Siempre revisa sus políticas de uso.
    # Es importante proporcionar un User-Agent que identifique tu aplicación.
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    # 3. User-Agent para Nominatim:
    #    Reemplaza 'tu_email@example.com' con un email de contacto real.
    #    Esto es una buena práctica y a veces un requisito para algunas APIs gratuitas.
    headers = {'User-Agent': 'UrbanBeatApp/1.0 (tu_email@example.com)'} # <--- ¡CAMBIA ESTE EMAIL!

    try:
        response = requests.get(nominatim_url, headers=headers)
        response.raise_for_status() # Lanza un error si la petición HTTP falla
        data = response.json() # Parsea la respuesta JSON de la API

        if data:
            # Si se encontraron resultados, devuelve la dirección, latitud y longitud del primer resultado.
            return jsonify({
                "address": data[0].get("display_name"), # Nombre completo de la dirección
                "lat": data[0].get("lat"),             # Latitud
                "lon": data[0].get("lon")              # Longitud
            })
        else:
            # Si la API no encontró la dirección.
            return jsonify({"error": "Dirección no encontrada"}), 404
    except requests.exceptions.RequestException as e:
        # Manejo de errores si hay problemas al llamar a la API de Nominatim.
        return jsonify({"error": f"Error al geocodificar con Nominatim: {e}"}), 500
    except Exception as e:
        # Manejo de errores inesperados.
        return jsonify({"error": f"Error inesperado al procesar geocodificación: {e}"}), 500

# --- Ejecución del Servidor Flask ---
# Esto asegura que el servidor solo se ejecute cuando el script se inicia directamente
# (no cuando se importa como un módulo en otro script).
if __name__ == '__main__':
    # app.run(): Inicia el servidor de desarrollo de Flask.
    # debug=True: Habilita el modo de depuración. Esto recarga el servidor automáticamente
    #             cuando detecta cambios en el código y proporciona mensajes de error detallados.
    # port=5000: El servidor escuchará en el puerto 5000.
    app.run(debug=True, port=5000)
