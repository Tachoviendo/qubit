# Qubit: Tu Asistente Técnico por Voz Personalizado

¡Bienvenido a Qubit! Un innovador asistente técnico por voz diseñado para responder tus dudas básicas y, lo más sorprendente, ¡reconocerte por tu propia voz!

---

## Descripción

Qubit es un asistente de voz multifuncional que te permite interactuar de forma natural y manos libres. Utiliza una combinación de tecnologías avanzadas para procesar tu voz, entender tus preguntas, generar respuestas y comunicarlas vocalmente. Además, cuenta con una mascota virtual que acompaña visualmente la interacción, haciendo la experiencia más amigable e intuitiva.

### ¿Cómo funciona?

1. **Reconocimiento de Voz (STT):** Qubit escucha tus comandos y preguntas gracias a **Vosk**, que transforma tu voz en texto.  
2. **Identificación de Hablante:** Con **Resemblyzer**, Qubit determina si eres un usuario registrado para ofrecerte una experiencia personalizada.  
3. **Procesamiento de Lenguaje Natural (LLM):** Las preguntas se procesan mediante un modelo **Ollama**, que genera respuestas coherentes.  
4. **Síntesis de Voz (TTS):** **Tacotron2** convierte el texto generado en audio para que Qubit te responda hablando.  
5. **Mascota Virtual:** Una interfaz visual amigable acompaña la interacción, haciéndola más dinámica y atractiva.

---

## Instalación

### Requisitos previos

- Python 3.8 o superior.

### Pasos de instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/Qubit.git
   cd Qubit
   ```

   > Reemplaza `tu_usuario` con tu nombre de usuario de GitHub.

2. **Instala las dependencias:**

   Opción 1 – instalación automática:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Opción 2 – instalación manual:

   ```bash
   pip install -r requirements.txt
   ```

   > Nota: El script `install.sh` gestiona la descarga de los modelos requeridos. Asegúrate de estar conectado a internet.

---

## Grabación de Perfiles de Voz

Para que Qubit te reconozca, necesitas grabar un perfil de voz.

### ¿Cómo grabar un perfil?

Ejecuta el siguiente script en un entorno silencioso:

```bash
python record_profile.py
```

Sigue las instrucciones en pantalla para grabar tu voz.

### Nomenclatura de los archivos

Usa el siguiente formato para nombrar los archivos:

- `juan1.wav`
- `maria2.wav`
- `pedro3.wav`

> Sin espacios ni caracteres especiales.

### Ubicación

Los perfiles se guardan en la carpeta `profiles/`.

---

## Uso del Asistente

Una vez instalado y configurado:

### Iniciar Qubit

```bash
python main.py
```

### Interacción

Di "Qubit" para activarlo y luego formula tu pregunta. Qubit te responderá vocalmente.

---

## Estructura del Proyecto

```
.
├── main.py
├── requirements.txt
├── install.sh
├── record_profile.py
├── config.py
├── utils/
│   ├── audio_recorder.py
│   ├── stt_vosk.py
│   ├── tts_tacotron2.py
│   ├── speaker_recognizer.py
│   └── llm_ollama.py
├── models/
│   ├── vosk_model/
│   ├── tacotron2_model/
│   └── ollama_model/
├── profiles/
│   ├── your_profile1.wav
│   └── another_profile2.wav
└── assets/
    └── virtual_pet_sprites/
```

---

## Archivos Principales y Sus Funciones

| Archivo/Carpeta | Función Principal |
| :---------------------- | :---------------------------------------------------------------- |
| `main.py` | Orquestador principal del asistente. |
| `record_profile.py` | Permite grabar y guardar perfiles de voz para el reconocimiento. |
| `config.py` | Almacena configuraciones globales del proyecto. |
| `utils/audio_recorder.py` | Gestiona la grabación de audio desde el micrófono. |
| `utils/stt_vosk.py` | Módulo para la transcripción de voz a texto usando Vosk. |
| `utils/tts_tacotron2.py`| Módulo para la síntesis de texto a voz con Tacotron2. |
| `utils/speaker_recognizer.py`| Gestiona la identificación de hablantes con Resemblyzer. |
| `utils/llm_ollama.py` | Interactúa con el modelo Ollama para procesar preguntas. |
| `models/` | Contiene los modelos de Vosk, Tacotron2 y Ollama. |
| `profiles/` | Almacena los archivos de audio de los perfiles de voz de los usuarios. |
| `assets/` | Contiene recursos para la mascota virtual y otros elementos visuales. |

---

## Consejos para Mejor Uso

- **Usa auriculares:** Evita retroalimentación de audio.  
- **Ambiente silencioso:** Mejora la precisión del reconocimiento de voz.  
- **Revisa rutas:** Especialmente para el modelo de Vosk en `config.py`.  
- **Internet requerido:** Para la descarga inicial de modelos.  
- **Habla claro:** Mejora el rendimiento del STT y el reconocimiento de hablante.

---

## Contribuciones

¡Tu ayuda es bienvenida!  
Puedes:

- Abrir un `issue` para reportar errores o sugerencias.
- Enviar un `pull request` con mejoras o nuevas funciones.

---

## Licencia

Este proyecto está bajo una licencia que permite su uso personal y educativo. Para otros usos, contacta a los desarrolladores.

---

## Contacto

**Email:** soporte.qubit@example.com  
**GitHub Issues:** [https://github.com/tu_usuario/Qubit/issues](https://github.com/tu_usuario/Qubit/issues)
