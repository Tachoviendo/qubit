
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
import re

class VozListener:
    def __init__(self, modelo_path=None, sample_rate=16000):
        # Ruta base de este archivo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Modelo default si no se pasa ninguno
        if modelo_path is None:
            modelo_path = os.path.join(base_dir, "vosk-model-small-es-0.42")
        
        if not os.path.exists(modelo_path):
            print(f"Error: no se encontró el modelo en '{modelo_path}'")
            sys.exit(1)

        self.model = vosk.Model(modelo_path)
        self.sample_rate = sample_rate
        self.q = queue.Queue()
        self.encoder = VoiceEncoder()
        
        # Ruta a carpeta wavs con perfiles
        perfiles_path = os.path.join(base_dir, "../voice_profiles/wavs")
        self.embeddings = self.cargar_perfiles(perfiles_path)

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
            # Quitar números del nombre para usar sólo texto
            nombre = re.sub(r'\d+', '', nombres[idx])
            return nombre, confianza
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
