Ok, entiendo. Aquí tienes el contenido completo del `README.md` en texto plano, sin ningún formato Markdown visible (sin `#`, `*`, `---`, \`\`\`\`bash\`, etc.). Es simplemente el texto crudo.

```
# Qubit: Tu Asistente Técnico por Voz Personalizado

¡Bienvenido a Qubit! Un innovador asistente técnico por voz diseñado para responder tus dudas básicas y, lo más sorprendente, ¡reconocerte por tu propia voz!

---

## Descripción

Qubit es un asistente de voz multifuncional que te permite interactuar de forma natural y manos libres. Utiliza una combinación de tecnologías avanzadas para procesar tu voz, entender tus preguntas, generar respuestas y comunicarlas vocalmente. Además, cuenta con una mascota virtual que acompaña visualmente la interacción, haciendo la experiencia más amigable e intuitiva.

### ¿Cómo funciona?

1.  **Reconocimiento de Voz (STT):** Qubit escucha tus comandos y preguntas gracias a **Vosk**, que transforma tu voz en texto.
2.  **Identificación de Hablante:** Para una experiencia personalizada, **Resemblyzer** analiza tu voz y determina si eres un usuario registrado, permitiendo a Qubit reconocerte.
3.  **Procesamiento de Lenguaje Natural (LLM):** Las preguntas son procesadas por un modelo **Ollama** que interpreta tu intención y genera respuestas coherentes.
4.  **Síntesis de Voz (TTS):** Finalmente, **Tacotron2** convierte la respuesta generada en voz, permitiendo que Qubit te hable.
5.  **Mascota Virtual:** Una interfaz visual acompaña la interacción, brindando una experiencia más dinámica y atractiva.

---

## Instalación

Sigue estos pasos para poner Qubit en funcionamiento en tu máquina.

### Requisitos previos

Asegúrate de tener Python 3.8 o superior instalado.

### Pasos de instalación

1.  **Clona el repositorio:**

    git clone [https://github.com/tu_usuario/Qubit.git](https://github.com/tu_usuario/Qubit.git)
    cd Qubit

    *(Reemplaza `tu_usuario` con el nombre de usuario de GitHub donde tengas alojado el repositorio)*

2.  **Instala las dependencias:**

    Para una instalación rápida y sencilla, puedes usar el script de instalación:

    chmod +x install.sh
    ./install.sh

    Alternativamente, puedes instalar las dependencias manualmente:

    pip install -r requirements.txt

    **Nota:** La instalación de los modelos de Vosk, Ollama y Tacotron2 puede requerir descargas adicionales que el script `install.sh` debería gestionar. Asegúrate de tener conexión a internet durante la instalación.

---

## Grabación de Perfiles de Voz

Para que Qubit te reconozca, necesitas grabar un perfil de voz. Este proceso es sencillo y solo lo tienes que hacer una vez por usuario.

### ¿Cómo grabar un perfil de voz?

Utiliza el script `record_profile.py` para grabar tu voz. Asegúrate de estar en un ambiente tranquilo para obtener la mejor calidad de perfil.

python record_profile.py

Al ejecutar el script, se te pedirá que hables durante unos segundos. Sigue las instrucciones en pantalla.

### Nomenclatura de los archivos

Es crucial nombrar los archivos de perfil de voz de manera correcta para que Qubit pueda identificarlos. El formato debe ser [nombre_usuario][numero], sin espacios ni caracteres especiales.

**Ejemplos válidos:**
* juan1.wav
* maria2.wav
* pedro3.wav

### Dónde se guardan los archivos

Los perfiles de voz grabados se guardarán automáticamente en la carpeta `profiles/`.

---

## Uso del Asistente

Una vez que hayas instalado Qubit y grabado tu perfil de voz, ¡estás listo para interactuar!

### Iniciar Qubit

Ejecuta el archivo principal para iniciar el asistente:

python main.py

### Interacción

Una vez iniciado, Qubit estará a la escucha. Simplemente di "Qubit" para activarlo, y luego formula tu pregunta. Qubit te responderá vocalmente.

---

## Estructura del Proyecto

Aquí te mostramos una visión general de la estructura principal de Qubit:

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

* **`main.py`**: Punto de entrada principal del asistente.
* **`requirements.txt`**: Lista de todas las dependencias de Python.
* **`install.sh`**: Script para la instalación rápida.
* **`record_profile.py`**: Script para grabar nuevos perfiles de voz.
* **`config.py`**: Archivo de configuración para rutas de modelos, sensibilidades, etc.
* **`utils/`**: Contiene módulos con funcionalidades específicas (grabación, STT, TTS, reconocimiento de hablante, LLM).
* **`models/`**: Carpeta para almacenar los modelos de Vosk, Tacotron2 y Ollama.
* **`profiles/`**: Almacena los perfiles de voz de los usuarios.
* **`assets/`**: Contiene recursos gráficos para la mascota virtual u otros elementos visuales.

---

## Consejos para Mejor Uso

Para una experiencia óptima con Qubit, ten en cuenta las siguientes recomendaciones:

* **Usa auriculares:** Esto ayuda a evitar la autoescucha o feedback de audio, lo que puede interferir con el reconocimiento de voz.
* **Ambiente silencioso:** Graba tus perfiles de voz y usa Qubit en un entorno lo más silencioso posible para mejorar la precisión del STT y el reconocimiento de hablante.
* **Verifica la ruta del modelo Vosk:** Asegúrate de que la ruta al modelo de Vosk en `config.py` sea correcta y que el modelo esté completamente descargado.
* **Conexión a internet:** Para la descarga inicial de modelos (especialmente Ollama y Vosk, si no se incluyen preinstalados), necesitarás una conexión a internet estable.
* **Habla claro:** Pronuncia tus palabras de forma clara y a un ritmo natural.

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

## Contribuciones

¡Tu ayuda es bienvenida! Si encuentras un error, tienes una idea para una nueva característica o simplemente quieres mejorar el código, no dudes en:

* Abrir un `issue` para reportar un problema o sugerir una mejora.
* Enviar un `pull request` con tus contribuciones.

Agradecemos cualquier tipo de colaboración para hacer de Qubit un proyecto aún mejor.

---

## Licencia

Este proyecto está bajo una licencia que permite su uso personal y educativo. Para otros usos, por favor, contacta a los desarrolladores.

---

## Contacto

Para cualquier consulta, soporte o sugerencia, no dudes en contactarnos:

* **Email:** soporte.qubit@example.com
* **GitHub Issues:** [Enlace a Issues de tu repositorio](https://github.com/tu_usuario/Qubit/issues)
```
