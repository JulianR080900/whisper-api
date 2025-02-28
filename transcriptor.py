import sys
import json
import os
import whisper

if len(sys.argv) < 2:
    print(json.dumps({"error": "No se recibieron parámetros"}))
    sys.exit(1)

# Cargar modelo de Whisper
model = whisper.load_model("small")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar los parámetros JSON
params = json.loads(sys.argv[1])
audio_path = params.get("audio_path")
language = params.get("language", None)

try:
    # Verificar si el archivo existe
    if not os.path.exists(audio_path):
        print(json.dumps({"error": "El archivo de audio no existe"}))
        sys.exit(1)

    # Transcribir con Whisper
    result = model.transcribe(audio_path, language=language)

    # Borrar el archivo después de la transcripción
    os.remove(audio_path)

    # Devolver la transcripción
    print(json.dumps({"text": result["text"]}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
