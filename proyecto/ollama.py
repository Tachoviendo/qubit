
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL_NAME = "gemma3:1b"

def ollama_worker(text_queue, response_queue, conversation_history, speaker_name_queue):
    while True:
        prompt = text_queue.get()
        speaker_name = speaker_name_queue.get()

        # Limpiar nombre (sacar números, espacios extras)
        speaker_name_clean = ''.join(filter(str.isalpha, speaker_name)).strip()
        if not speaker_name_clean:
            speaker_name_clean = "Usuario"

        # Agregar nombre al prompt para personalizar respuesta
        prompt_con_nombre = f"[{speaker_name_clean}] {prompt}"

        conversation_history.append({"role": "user", "content": prompt_con_nombre})

        payload = {
            "model": OLLAMA_MODEL_NAME,
            "messages": conversation_history,
            "stream": False
        }
        try:
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data.get("message", {}).get("content", "").strip()
            conversation_history.append({"role": "assistant", "content": reply})
            print(f"[Ollama] Respuesta: {reply}")
            response_queue.put(reply)
        except Exception as e:
            print(f"[Ollama] Error: {e}")
            response_queue.put("Lo siento, hubo un problema con la respuesta.")
