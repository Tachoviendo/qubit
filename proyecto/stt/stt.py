
import os
import sys
import queue
import json
import numpy as np
import sounddevice as sd
import vosk
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
from scipy.spatial.distance import cdist
import soundfile as sf

class VozListener:
    def __init__(self, modelo_path=None, sample_rate=16000):
        if modelo_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            modelo_path = os.path.join(base_dir, "vosk-model-small-es-0.42")

        if not os.path.exists(modelo_path):
            print(f"Error: no se encontró el modelo en '{modelo_path}'")
            sys.exit(1)

        self.model = vosk.Model(modelo_path)
        self.sample_rate = sample_rate
        self.q = queue.Queue()
        self.encoder = VoiceEncoder()
        self.embeddings = self.cargar_perfiles(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../voice_profiles"))

    def _callback(self, indata, frames, time, status):
        if status:
            print("Status:", status, file=sys.stderr)
        self.q.put(bytes(indata))

    def cargar_perfiles(self, folder):
        perfiles = {}
        if not os.path.exists(folder):
            print(f"Advertencia: carpeta de perfiles '{folder}' no existe.")
            return perfiles

        for file in os.listdir(folder):
            if file.endswith(".wav"):
                name = file.replace(".wav", "")
                try:
                    wav_f = preprocess_wav(Path(folder) / file)
                    embed = self.encoder.embed_utterance(wav_f)
                    perfiles[name] = embed
                except Exception as e:
                    print(f"Error cargando perfil '{file}': {e}")
        return perfiles

    def identificar_hablante(self, nueva_voz):
        nueva_embedding = self.encoder.embed_utterance(nueva_voz)
        nombres = list(self.embeddings.keys())
        vectores = np.array(list(self.embeddings.values()))

        if len(vectores) == 0:
            return "desconocido", 0.0

        distancias = cdist([nueva_embedding], vectores, metric="cosine")[0]
        idx = np.argmin(distancias)
        confianza = 1 - distancias[idx]

        if confianza > 0.75:
            return nombres[idx], confianza
        else:
            return "desconocido", confianza

    def escuchar(self, tiempo_max=5):
        with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000, dtype='int16',
                               channels=1, callback=self._callback):
            rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
            print("Escuchando... hablá ahora")

            voz_data = b""
            tiempo_espera = tiempo_max * 10

            texto = ""
            while tiempo_espera > 0:
                if not self.q.empty():
                    data = self.q.get()
                    voz_data += data
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        texto = result.get("text", "")
                        if texto.strip():
                            break
                tiempo_espera -= 1
                sd.sleep(100)

            if not texto.strip():
                texto = json.loads(rec.FinalResult()).get("text", "")

            if not voz_data:
                print("No se capturó audio.")
                return "", "desconocido", 0.0

            temp_path = "temp_input.wav"
            sf.write(temp_path, np.frombuffer(voz_data, dtype=np.int16), self.sample_rate)

            try:
                wav = preprocess_wav(temp_path)
                hablante, confianza = self.identificar_hablante(wav)
            except Exception as e:
                print(f"Error al procesar la voz: {e}")
                hablante, confianza = "desconocido", 0.0

            try:
                os.remove(temp_path)
            except OSError:
                pass

            return texto.strip(), hablante, round(confianza, 2)

def recognize_worker(audio_queue, text_queue):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "vosk-model-small-es-0.42")
        model = vosk.Model(model_path)
        rec = vosk.KaldiRecognizer(model, 16000)
    except Exception as e:
        print(f"[Vosk] Error cargando el modelo: {e}")
        return

    while True:
        data = audio_queue.get()
        if rec.AcceptWaveform(data):
            try:
                result = json.loads(rec.Result())
                user_text = result.get("text", "").strip()
                if user_text:
                    print(f"[Vosk] Usuario dijo: {user_text}")
                    text_queue.put(user_text)
            except Exception as e:
                print(f"[Vosk] Error al procesar resultado: {e}")
