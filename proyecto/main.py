
import sys
import time
import queue
import threading
import sounddevice as sd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread

from capybara.capybara import CapybaraMascot
from stt.stt import VozListener
from ollama import ollama_worker
from tts import tts_and_play_worker

SAMPLE_RATE = 16000
BUFFER_SIZE = 4000

class AssistantThread(QThread):
    def __init__(self, capybara, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capybara = capybara

    def run(self):
        audio_queue = queue.Queue()
        text_queue = queue.Queue()
        response_queue = queue.Queue()
        speaker_name_queue = queue.Queue()

        can_listen = threading.Event()
        can_listen.set()  # Permite escuchar inicialmente

        conversation_history = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte técnico especializado en ayudar a personas con poca experiencia en computadoras. "
                    "Explica todo de forma muy sencilla, paso a paso, sin tecnicismos, y responde siempre con un máximo de 50 palabras."
                )
            }
        ]

        voz_listener = VozListener()

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"[Audio] Estado: {status}")
            if can_listen.is_set():
                audio_queue.put(bytes(indata))
            else:
                # Cuando el asistente habla, no captura audio
                pass

        try:
            stream = sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BUFFER_SIZE,
                dtype='int16',
                channels=1,
                callback=audio_callback
            )
            stream.start()
        except Exception as e:
            print(f"[Audio] Error inicializando stream: {e}")
            return

        def stt_thread_func():
            while True:
                if can_listen.is_set() and not audio_queue.empty():
                    texto, hablante, _ = voz_listener.escuchar(tiempo_max=5)
                    if texto:
                        nombre_limpio = ''.join(filter(str.isalpha, hablante))
                        if not nombre_limpio:
                            nombre_limpio = "Usuario"
                        print(f"[STT] Texto: {texto}, Hablante: {nombre_limpio}")
                        text_queue.put(texto)
                        speaker_name_queue.put(nombre_limpio)
                else:
                    time.sleep(0.1)

        threading.Thread(target=stt_thread_func, daemon=True).start()
        threading.Thread(target=ollama_worker, args=(text_queue, response_queue, conversation_history, speaker_name_queue), daemon=True).start()
        threading.Thread(target=tts_and_play_worker, args=(response_queue, can_listen, self.capybara), daemon=True).start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Terminando el asistente de voz...")

def main():
    app = QApplication(sys.argv)

    mascota = CapybaraMascot()

    assistant_thread = AssistantThread(mascota)
    assistant_thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
