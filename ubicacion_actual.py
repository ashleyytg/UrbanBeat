# create_location_file.py
# ==============================================================================
# Este script crea un archivo JSON con una ubicación específica.
# Su único propósito es generar el archivo 'mi_ubicacion.json' que
# servirá como punto de partida para el script de enrutamiento (geoapify.py).
# ==============================================================================

import json
import sys

# ==============================================================================
# 1. CONFIGURACIÓN 📍
# ==============================================================================
# El nombre del archivo que vamos a crear.
OUTPUT_FILENAME = "mi_ubicacion.json"

# ¡Aquí pones las coordenadas que quieras usar como tu punto de inicio!
# Estas son las que me proporcionaste.
LATITUDE = -12.0817244
LONGITUDE = -76.9468910

# ==============================================================================
# 2. EJECUCIÓN DEL SCRIPT 🚀
# ==============================================================================
if __name__ == "__main__":
    
    print(f"⚙️  Creando archivo de ubicación con las coordenadas: ({LATITUDE}, {LONGITUDE})")

    # Creamos un diccionario de Python con la estructura deseada.
    # Esto asegura que el JSON tenga las claves 'latitude' y 'longitude'.
    location_data = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "source": "Ubicación definida por el usuario"
    }

    try:
        # Abrimos el archivo en modo escritura ('w') y guardamos el diccionario.
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            # json.dump() convierte el diccionario de Python a formato JSON.
            # indent=4 hace que el archivo sea fácil de leer para los humanos.
            json.dump(location_data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ ¡Éxito! La ubicación ha sido guardada en '{OUTPUT_FILENAME}'")

    except IOError as e:
        # Manejo de errores en caso de que no se pueda escribir el archivo.
        print(f"\n❌ Error al escribir en el archivo: {e}", file=sys.stderr)
        sys.exit(1)
