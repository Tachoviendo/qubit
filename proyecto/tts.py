
from TTS.api import TTS
import numpy as np
import simpleaudio as sa
import re
import time

def clean_text(text):
    text = text.replace('¿', '').replace('¡', '')
    text = re.sub(r'[^\w\s.,!?áéíóúÁÉÍÓÚñÑ]', '', text)
    return text

def tts_and_play_worker(response_queue, can_listen, capybara=None):
    try:
        tts = TTS("tts_models/es/mai/tacotron2-DDC")
    except Exception as e:
        print(f"[TTS] Error cargando modelo TTS: {e}")
        return

    while True:
        text = response_queue.get()
        text = clean_text(text)
        try:
            print(f"[TTS] Sintetizando...")
            can_listen.clear()  # Pausar escucha para no capturar el audio que reproduce
            if capybara:
                capybara.say(text)
            wav = tts.tts(text=text)
            wav = np.array(wav)
            wav = (wav * 32767).astype(np.int16)
            sa.play_buffer(wav, 1, 2, 22050).wait_done()
            time.sleep(0.5)
            print("[TTS] Reproducción terminada, listo para escuchar.")
            if capybara:
                capybara.stop_saying()
        except Exception as e:
            print(f"[TTS] Error al sintetizar o reproducir: {e}")
        finally:
            can_listen.set()  # Volver a activar escucha
            time.sleep(0.1)  # Evitar saturación
