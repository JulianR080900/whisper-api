from flask import Flask, request, jsonify
import subprocess
import json
import os
from flask_cors import CORS
import sys
python_executable = sys.executable  # Obtiene la ruta del Python en el entorno virtual

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/transcripcionAudio', methods=['POST'])
def transcribir_audio():
    try:
        script_name = "transcriptor.py"

        if 'file' not in request.files:
            return jsonify({"error": "No se encontró ningún archivo"}), 400

        audio_file = request.files['file']
        language = request.form.get('language', None)

        # Guardar el archivo temporalmente
        file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
        audio_file.save(file_path)

        # Crear un diccionario de parámetros
        params = json.dumps({"audio_path": file_path, "language": language})

        python_executable = sys.executable  # Obtiene la ruta del Python en el entorno virtual

        result = subprocess.run([python_executable, script_name, params], capture_output=True, text=True)

        # Retornar la respuesta procesada por Whisper
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
