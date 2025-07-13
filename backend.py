from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir llamadas desde otro puerto (como localhost:8000)

@app.route('/api/ejecutar', methods=['POST'])
def ejecutar_scripts():
    data = request.get_json(force=True)
    query = data.get('query', '').strip()
    location = data.get('location', '').strip()

    if not query or not location:
        return jsonify({'success': False, 'message': 'Faltan datos de entrada'}), 400

    print(f"\n🔍 Parámetros recibidos -> QUERY: {query} | LOCATION: {location}")

    # Limpiar archivos previos antes de ejecutar nuevos scripts
    archivos_a_borrar = ["destination.json", "mi_ubicacion.json", "ruta.json"]
    for archivo in archivos_a_borrar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"🧹 Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"❌ Error al eliminar {archivo}: {e}")

    # Lista de scripts y cómo ejecutarlos
    scripts = [
        ["python", "01_OpenStreetMap.py", query, location],
        ["python", "02_ubicacion_actual.py"],
        ["python", "03_GeoApify.py"]
    ]

    for script_cmd in scripts:
        script_name = script_cmd[1]
        print(f"⚙️  Ejecutando {script_name}...")
        try:
            result = subprocess.run(script_cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"✅ {script_name} ejecutado correctamente")

            # Verificar que destination.json se haya creado correctamente
            if script_name == "01_OpenStreetMap.py":
                if not os.path.exists("destination.json"):
                    print("❌ No se creó destination.json. El lugar no fue encontrado.")
                    return jsonify({'success': False, 'message': 'No se encontró ningún lugar con esos datos'}), 400
                else:
                    with open("destination.json", "r", encoding="utf-8") as f:
                        destino = json.load(f)
                        lat = destino.get("latitude")
                        lon = destino.get("longitude")
                        if not lat or not lon:
                            print("❌ destination.json no contiene coordenadas válidas.")
                            return jsonify({'success': False, 'message': 'No se encontró un destino válido'}), 400

        except subprocess.CalledProcessError as e:
            print(f"❌ Error en {script_name}:\n{e.stderr}")
            return jsonify({'success': False, 'message': f'Error en {script_name}: {e.stderr}'}), 500

    if os.path.exists("ruta.json"):
        print("📦 Archivo 'ruta.json' generado correctamente.")
        return jsonify({'success': True})
    else:
        print("❌ No se generó 'ruta.json'.")
        return jsonify({'success': False, 'message': 'No se generó el archivo de ruta'}), 500

if __name__ == "__main__":
    print("🚀 Servidor Flask iniciado correctamente en http://localhost:5000")
    app.run(debug=True)
