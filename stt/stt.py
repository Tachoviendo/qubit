import vosk
import sounddevice as sd
import numpy as np
import queue
import json
import time
import requests

# --- Configuración de Vosk ---
MODEL_PATH = "/home/tacho/Documents/qubit/stt/vosk-model-small-es-0.42" # ¡Verifica tu ruta!
SAMPLE_RATE = 16000
BUFFER_SIZE = 4000

# Cola para almacenar los fragmentos de audio
q = queue.Queue()

# --- Configuración de Ollama (Gemma 1B) ---
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL_NAME = "gemma3:1b" # Asegúrate de que este sea el nombre del modelo que descargaste. ¡Cambio: eliminé el "3" si no lo necesitas!

# Historial de conversación para mantener el contexto
# Es una buena práctica inicializar con un mensaje de sistema para dar contexto a la IA
conversation_history = [
    {"role": "system", "content": "Eres un asistente de IA útil y amigable que responde de forma concisa."}
]

def callback(indata, frames, time, status):
    """Este callback se llama cada vez que sounddevice recibe un nuevo bloque de audio."""
    if status:
        print(status)
    q.put(bytes(indata))

def get_gemma_response(prompt):
    """
    Envía un prompt a la API de Ollama (usando /api/chat) y devuelve la respuesta de Gemma 1B.
    Mantiene el historial de conversación para contexto.
    """
    global conversation_history # Accede a la variable global

    # Agrega el prompt del usuario al historial
    conversation_history.append({"role": "user", "content": prompt})

    # --- CAMBIO CRÍTICO AQUÍ: Usamos "messages" en lugar de "prompt" ---
    payload = {
        "model": OLLAMA_MODEL_NAME,
        "messages": conversation_history, # <-- ¡Esto es lo que necesita el endpoint /api/chat!
        "stream": False # Queremos la respuesta completa de una vez
    }
    # --- FIN DEL CAMBIO ---

    # Limpiamos la línea actual antes de imprimir el mensaje de envío
    # Esto asegura que "Enviando a Gemma 1B..." aparezca limpio
    print("\r" + " " * 80 + "\r", end="") # Limpia la línea actual
    print(f"--- Enviando a Gemma 1B: '{prompt}' ---")

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status() # Lanza un error para códigos de estado HTTP 4xx/5xx

        # La respuesta de Ollama para /api/chat es un JSON con el mensaje del asistente
        data = response.json()
        # Accedemos al contenido del mensaje del asistente
        gemma_text_response = data.get("message", {}).get("content", "").strip()

        # Agrega la respuesta de Gemma al historial
        conversation_history.append({"role": "assistant", "content": gemma_text_response})

        return gemma_text_response

    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar a Ollama. Asegúrate de que 'ollama serve' esté ejecutándose y el puerto 11434 esté disponible.")
        return "Lo siento, no pude conectar con mi cerebro en este momento."
    except requests.exceptions.RequestException as e:
        print(f"\nError al obtener respuesta de Ollama: {e}")
        # Si el error es 404, podría ser que el modelo no existe o el endpoint es incorrecto
        if response.status_code == 404:
            print(f"Posible causa: El modelo '{OLLAMA_MODEL_NAME}' no existe o el endpoint /api/chat no es válido para tu versión de Ollama.")
            print("Asegúrate de que el modelo esté descargado y de que Ollama esté actualizado.")
        return "Hubo un problema al procesar tu solicitud."


def recognize_from_mic():
    """
    Captura audio del micrófono, lo transcribe con Vosk y envía la transcripción a Gemma 1B.
    """
    try:
        model = vosk.Model(MODEL_PATH)
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    except Exception as e:
        print(f"Error al cargar el modelo de Vosk: {e}")
        print(f"Asegúrate de que la ruta del modelo '{MODEL_PATH}' es correcta y el modelo está descomprimido.")
        return

    print("Escuchando... Di algo (Ctrl+C para salir)")

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE,
                                dtype='int16', channels=1, callback=callback):
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    user_text = result.get("text", "").strip()

                    if user_text:
                        # Aseguramos que la transcripción final aparezca en una nueva línea limpia
                        print("\r" + " " * 80 + "\r", end="") # Limpia la línea actual antes de imprimir
                        print(f"--- Transcripción (Usuario): {user_text} ---")

                        gemma_response = get_gemma_response(user_text)

                        # Aseguramos que la respuesta de Gemma aparezca en una nueva línea limpia
                        print(f"--- Respuesta (Gemma 1B): {gemma_response} ---")
                        print("\nEscuchando de nuevo... (Di algo o Ctrl+C para salir)") # Indicador para el siguiente turno

                else:
                    # Desactiva la impresión de parciales por ahora para evitar sobreescritura.
                    # Si quieres verlos, puedes descomentar la siguiente sección.
                    # partial_result = json.loads(rec.PartialResult())
                    # partial_text = partial_result.get("partial", "")
                    # if partial_text:
                    #     print(f"Vosk (Parcial): {partial_text}", end='\r')
                    pass

    except KeyboardInterrupt:
        print("\nDeteniendo la escucha.")
        final_result = json.loads(rec.FinalResult())
        user_text = final_result.get("text", "").strip()
        if user_text:
            print(f"--- Transcripción Final (Usuario): {user_text} ---")
            gemma_response = get_gemma_response(user_text)
            print(f"--- Respuesta Final (Gemma 1B): {gemma_response} ---")
    except Exception as e:
        print(f"Se produjo un error inesperado durante la escucha o procesamiento: {e}")

if __name__ == "__main__":
    recognize_from_mic()
