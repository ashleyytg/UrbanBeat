# geoapify.py

import requests
import json
import sys

# ==============================================================================
# 1. CONFIGURACIÓN ⚙️
# ==============================================================================
GEOAPIFY_API_KEY = "47c2c2bbc15a4fd1870556ba827063cf"
API_URL = "https://api.geoapify.com/v1/routing"

# Definimos los nombres de los archivos que vamos a leer y escribir
START_FILENAME = "mi_ubicacion.json"
DESTINATION_FILENAME = "destination.json"
OUTPUT_FILENAME = "ruta.json"

# ==============================================================================
# 2. FUNCIÓN PARA CALCULAR LA RUTA 🗺️
# ==============================================================================
def get_driving_route(api_key, start_lat, start_lon, end_lat, end_lon): 
    #esta función calcula la ruta en coche entre dos puntos dados por sus coordenadas de latitud y longitud.
    """
    Calcula una ruta en coche y devuelve el resultado JSON o None si hay error.
    """
    waypoints = f"{start_lat},{start_lon}|{end_lat},{end_lon}"
    # Esto crea una cadena que representa los puntos de inicio y destino
    # que se usarán para calcular la ruta.
    params = {
        "waypoints": waypoints,
        "mode": "drive",
        "apiKey": api_key,
        "details": "instruction_details"
    }# Esto es un diccionario que contiene los parámetros de la solicitud
    # que se enviarán a la API de Geoapify.
    print(f"🛰️  Solicitando ruta desde ({start_lat}, {start_lon}) hasta ({end_lat}, {end_lon})...", file=sys.stderr)
    try:
        response = requests.get(API_URL, params=params)# Aquí hacemos la solicitud a la API de Geoapify
        # usando la URL base y los parámetros definidos.
        response.raise_for_status() # Esto verifica si la solicitud fue exitosa (código 200).
        # Si hubo un error, se lanzará una excepción.
        return response.json()
    
        # Si la solicitud fue exitosa, convertimos la respuesta a formato JSON
        # y la devolvemos. Esto nos dará un diccionario de Python con los datos de la ruta.
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de Conexión o de API: {e}", file=sys.stderr)
        return None

# ==============================================================================
# 3. EJECUCIÓN PRINCIPAL DEL SCRIPT 🚀
# ==============================================================================
if __name__ == "__main__":
    
    # --- PASO 1: LEER EL PUNTO DE INICIO DESDE mi_ubicacion.json ---
    try:
        print(f"📖 Leyendo archivo de ORIGEN '{START_FILENAME}'...", file=sys.stderr)

        with open(START_FILENAME, 'r', encoding='utf-8') as f:
            start_data = json.load(f)
        # Aquí abrimos el archivo JSON que contiene las coordenadas de inicio

        start_lat = start_data['latitude']
        start_lon = start_data['longitude']
        # Extraemos las coordenadas de latitud y longitud del archivo
        # Esto nos da las coordenadas de inicio que usaremos para calcular la ruta

        # Imprimimos un mensaje de éxito
        print(f"   -> Punto de inicio extraído: ({start_lat}, {start_lon})", file=sys.stderr)

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        # Manejo de errores en caso de que el archivo no exista o esté corrupto.
        # Si hay un error al abrir o leer el archivo, mostramos un mensaje de error
        print(f"❌ Error con el archivo de origen '{START_FILENAME}': {e}", file=sys.stderr)
        print("   Asegúrate de que el archivo existe y es correcto.", file=sys.stderr)
        sys.exit(1)

    # --- PASO 2: LEER EL PUNTO DE DESTINO DESDE destination.json --- # Lo mismo pero pal destino xdd
    try:
        print(f"📖 Leyendo archivo de DESTINO '{DESTINATION_FILENAME}'...", file=sys.stderr)

        with open(DESTINATION_FILENAME, 'r', encoding='utf-8') as f:
            end_data = json.load(f)
        end_lat = end_data['latitude']
        end_lon = end_data['longitude']
        print(f"   -> Punto de destino extraído: ({end_lat}, {end_lon})", file=sys.stderr)
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"❌ Error con el archivo de destino '{DESTINATION_FILENAME}': {e}", file=sys.stderr)
        print("   Asegúrate de que el archivo existe y es correcto.", file=sys.stderr)
        sys.exit(1)

    # --- PASO 3: OBTENER LA RUTA USANDO AMBAS COORDENADAS ---
    route_data = get_driving_route(GEOAPIFY_API_KEY, start_lat, start_lon, end_lat, end_lon)

    # --- PASO 4: GUARDAR LA RUTA EN ruta.json ---
    if route_data:
        try:
            # Guardamos la información de la ruta en 'ruta.json'
            with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
                # Esto abre el archivo en modo escritura
                json.dump(route_data, f, ensure_ascii=False, indent=4)
            print(f"\n✅ ¡Éxito! La ruta ha sido guardada en el archivo '{OUTPUT_FILENAME}'", file=sys.stderr)
            # Esto convierte el diccionario de Python a formato JSON y lo escribe en el archivo
            # 'ensure_ascii=False' permite caracteres no ASCII, y 'indent=4' hace
        except IOError as e:
            print(f"\n❌ Error al escribir en el archivo: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\n❌ La operación falló. No se pudo generar el archivo de ruta.", file=sys.stderr)
        sys.exit(1)
