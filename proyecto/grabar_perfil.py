
import sounddevice as sd
import sounddevice as sd
import soundfile as sf
import os
import argparse
import sys

def grabar_audio(nombre="Nacho", carpeta="voice_profiles", duracion=5, sample_rate=16000):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    archivo_salida = os.path.join(carpeta, f"{nombre}.wav")

    print(f"\n🎙️ Grabando voz para: {nombre} ({duracion} segundos)...")
    print("🟢 Hablá normalmente durante la grabación...")

    try:
        grabacion = sd.rec(int(duracion * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        sf.write(archivo_salida, grabacion, sample_rate)
        print(f"✅ Voz guardada exitosamente en: {archivo_salida}")
    except Exception as e:
        print(f"❌ Error durante la grabación o guardado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graba una muestra de voz para reconocimiento de hablante.")
    parser.add_argument("--nombre", help="Nombre del hablante (usado como nombre del archivo WAV)")
    parser.add_argument("--duracion", type=int, default=5, help="Duración de la grabación en segundos")

    args = parser.parse_args()

    # Si no pasa nombre, lo pedimos por consola
    if not args.nombre:
        args.nombre = input("Ingresá el nombre del hablante: ").strip()

    grabar_audio(args.nombre, duracion=args.duracion)
import soundfile as sf
import os
import argparse
import sys

def grabar_audio(nombre="Nacho", carpeta="voice_profiles", duracion=5, sample_rate=16000):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    archivo_salida = os.path.join(carpeta, f"{nombre}.wav")

    print(f"\n🎙️ Grabando voz para: {nombre} ({duracion} segundos)...")
    print("🟢 Hablá normalmente durante la grabación...")

    try:
        grabacion = sd.rec(int(duracion * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        sf.write(archivo_salida, grabacion, sample_rate)
        print(f"✅ Voz guardada exitosamente en: {archivo_salida}")
    except Exception as e:
        print(f"❌ Error durante la grabación o guardado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graba una muestra de voz para reconocimiento de hablante.")
    parser.add_argument("--nombre", help="Nombre del hablante (usado como nombre del archivo WAV)")
    parser.add_argument("--duracion", type=int, default=5, help="Duración de la grabación en segundos")

    args = parser.parse_args()

    # Si no pasa nombre, lo pedimos por consola
    if not args.nombre:
        args.nombre = input("Ingresá el nombre del hablante: ").strip()

    grabar_audio(args.nombre, duracion=args.duracion)
