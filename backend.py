from flask import Flask, request, jsonify  # Importar Flask, request para obtener datos y jsonify para respuestas JSON
from flask_cors import CORS                # Importar CORS para permitir peticiones desde otros orígenes
import subprocess                          # Para ejecutar scripts de Python como procesos externos
import os                                  # Para manejar archivos del sistema (como eliminar archivos antiguos)
import json                                # Para leer archivos JSON

# Inicializar la aplicación Flask
app = Flask(__name__)

# Habilita CORS para que el frontend (por ejemplo, en otro puerto como localhost:8000) pueda comunicarse con este backend
CORS(app)

# Ruta de la API que se activa con una petición POST
@app.route('/api/ejecutar', methods=['POST'])
def ejecutar_scripts():
    # Obtener los datos del JSON enviado desde el frontend
    data = request.get_json(force=True)
    query = data.get('query', '').strip()        # Lugar de destino que busca el usuario
    location = data.get('location', '').strip()  # Punto de partida del usuario

    # Validación básica: si no se recibe 'query' o 'location', devuelve error 400
    if not query or not location:
        return jsonify({'success': False, 'message': 'Faltan datos de entrada'}), 400

    print(f"\n🔍 Parámetros recibidos -> QUERY: {query} | LOCATION: {location}")

    # Lista de archivos que podrían haber sido generados previamente y deben eliminarse antes de una nueva ejecución
    archivos_a_borrar = ["destination.json", "mi_ubicacion.json", "ruta.json"]
    for archivo in archivos_a_borrar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"🧹 Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"❌ Error al eliminar {archivo}: {e}")

    # Lista de scripts a ejecutar y los argumentos que recibirán
    scripts = [
        ["python", "01_OpenStreetMap.py", query, location],  # Obtiene coordenadas del destino
        ["python", "02_ubicacion_actual.py"],                # Obtiene la ubicación actual (simulada o real)
        ["python", "03_GeoApify.py"]                         # Calcula la ruta entre origen y destino
    ]

    # Ejecutar cada script secuencialmente
    for script_cmd in scripts:
        script_name = script_cmd[1]
        print(f"⚙️  Ejecutando {script_name}...")
        try:
            # Ejecutar el script como subproceso, capturando la salida
            result = subprocess.run(script_cmd, check=True, capture_output=True, text=True)
            print(result.stdout)  # Mostrar en consola la salida del script
            print(f"✅ {script_name} ejecutado correctamente")

            # Verificación especial después del primer script
            if script_name == "01_OpenStreetMap.py":
                if not os.path.exists("destination.json"):
                    print("❌ No se creó destination.json. El lugar no fue encontrado.")
                    return jsonify({'success': False, 'message': 'No se encontró ningún lugar con esos datos'}), 400
                else:
                    # Leer el archivo JSON generado para asegurar que contiene coordenadas válidas
                    with open("destination.json", "r", encoding="utf-8") as f:
                        destino = json.load(f)
                        lat = destino.get("latitude")
                        lon = destino.get("longitude")
                        if not lat or not lon:
                            print("❌ destination.json no contiene coordenadas válidas.")
                            return jsonify({'success': False, 'message': 'No se encontró un destino válido'}), 400

        except subprocess.CalledProcessError as e:
            # Si hay error al ejecutar cualquier script, devolver error 500 con detalles
            print(f"❌ Error en {script_name}:\n{e.stderr}")
            return jsonify({'success': False, 'message': f'Error en {script_name}: {e.stderr}'}), 500

    # Verificar si al final se generó correctamente el archivo con la ruta final
    if os.path.exists("ruta.json"):
        print("📦 Archivo 'ruta.json' generado correctamente.")
        return jsonify({'success': True})  # Todo fue exitoso
    else:
        print("❌ No se generó 'ruta.json'.")
        return jsonify({'success': False, 'message': 'No se generó el archivo de ruta'}), 500

# Iniciar el servidor Flask si este archivo se ejecuta directamente
if __name__ == "__main__":
    print("🚀 Servidor Flask iniciado correctamente en http://localhost:5000")
    app.run(debug=True)  # Ejecutar el servidor con modo debug activado para ver errores y logs

