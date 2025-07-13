# find_destination.py

import requests # Esto es para hacer solicitudes HTTP
import json # Esto es para manejar archivos JSON
import sys # Esto es para manejar errores y salidas del sistema

# ==============================================================================
# 1. CONFIGURACIÓN
# ==============================================================================

# URL de la API de Nominatim (para buscar en OpenStreetMap)
#sirve para buscar lugares en OpenStreetMap
API_URL = "https://nominatim.openstreetmap.org/search"

OUTPUT_FILENAME = "destination.json" # El archivo de destino que generaremos

# ==============================================================================
# 2. PARÁMETROS DE BÚSQUEDA # Vamos a buscar un destino
# ==============================================================================

import sys

if len(sys.argv) != 3:
    print("❌ Uso: python 01_OpenStreetMap.py <query> <location>", file=sys.stderr)
    sys.exit(1)

QUERY = sys.argv[1]
LOCATION = sys.argv[2]



# ==============================================================================
# 3. FUNCIÓN PARA ENCONTRAR UN LUGAR 🗺️
# ==============================================================================
def find_place(query, location):
    """
    Busca un lugar usando Nominatim y devuelve el primer resultado.
    """
    # Formateamos la búsqueda completa
    full_query = f"{query} en {location}" 
    # Esto crea una cadena que combina la consulta y la ubicación
    
    # Esto es un diccionario que contiene los parámetros de la búsqueda
    params = {
        'q': full_query,
        'format': 'json',
        'limit': 1 # Solo queremos el primer resultado
    } 
    # Esto es para especificar el formato de la respuesta y limitar los resultados a uno

    # La política de Nominatim requiere un User-Agent personalizado.
    # Esto es como decirle "hola, soy una app, no un navegador malicioso".
    headers = {
        'User-Agent': 'UrbanBeatApp/1.0 (anderson.dev.contact@example.com)'
    }

    print(f"🛰️  Buscando '{full_query}' en OpenStreetMap...", file=sys.stderr)
    # Esto imprime un mensaje en la salida de error estándar (usualmente la consola)

    try:
        response = requests.get(API_URL, params=params, headers=headers)# Esto hace la solicitud a la API
        # Verificamos si la solicitud fue exitosa
        response.raise_for_status() #esto lanza un error si la respuesta no es exitosa (4xx, 5xx)
        results = response.json() #esto convierte la respuesta JSON en un diccionario de Python
        
        if results:
            return results[0] # Devolvemos solo el primer lugar encontrado
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de Conexión o de API: {e}", file=sys.stderr)
        return None

# ==============================================================================
# 4. EJECUCIÓN PRINCIPAL DEL SCRIPT 🚀
# ==============================================================================
if __name__ == "__main__": # Esto asegura que el código solo se ejecute si este archivo es el principal
    
    place_data = find_place(QUERY, LOCATION) # Llamamos a la función para buscar el lugar

    if place_data: # Verificamos si encontramos algún lugar
        # Extraemos los datos que nos interesan
        place_name = place_data.get('display_name', 'Nombre no disponible')
        place_lat = place_data.get('lat')
        place_lon = place_data.get('lon')

        # Verificamos que tengamos las coordenadas
        if place_lat and place_lon:
            # Creamos un diccionario limpio para nuestro archivo JSON
            destination_info = {
                "name": place_name,
                "latitude": float(place_lat),
                "longitude": float(place_lon)
            }
            
            try:
                # Guardamos la información del destino en 'destination.json'
                with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f: # Abrimos el archivo en modo escritura
                    # json.dump() convierte el diccionario de Python a formato JSON.
                    json.dump(destination_info, f, ensure_ascii=False, indent=4)
                    # Esto asegura que el JSON sea legible para humanos (indentado y sin caracteres ASCII no imprimibles)
                
                # Imprimimos un mensaje de éxito
                print(f"\n✅ ¡Éxito! Destino encontrado y guardado en '{OUTPUT_FILENAME}'", file=sys.stderr)
                print(f"   -> Lugar: {place_name[:50]}...", file=sys.stderr) # Imprime los primeros 50 caracteres del nombre

            except IOError as e:# Manejo de errores en caso de que no se pueda escribir el archivo.
                print(f"\n❌ Error al escribir en el archivo: {e}", file=sys.stderr)
                sys.exit(1)
        else: # Verificamos si las coordenadas están disponibles
            print("❌ Error: El resultado de la API no contenía coordenadas.", file=sys.stderr)
            sys.exit(1)
    else: # Si no encontramos ningún lugar
        # Imprimimos un mensaje de error
        print("\n❌ No se encontraron resultados para la búsqueda.", file=sys.stderr)
        sys.exit(1)
