# Qubit: Tu Asistente Técnico por Voz Personalizado

¡Bienvenido a Qubit! Un innovador asistente técnico por voz diseñado para responder tus dudas básicas y, lo más sorprendente, ¡reconocerte por tu propia voz!

---

## Descripción

Qubit es un asistente de voz multifuncional que te permite interactuar de forma natural y manos libres. Utiliza una combinación de tecnologías avanzadas para procesar tu voz, entender tus preguntas, generar respuestas y comunicarlas vocalmente. Además, cuenta con una mascota virtual que acompaña visualmente la interacción, haciendo la experiencia más amigable e intuitiva.

### ¿Cómo funciona?

1. **Reconocimiento de Voz (STT):** Qubit escucha tus comandos y preguntas gracias a **Vosk**, que transforma tu voz en texto.  
2. **Identificación de Hablante:** Para una experiencia personalizada, se analiza tu voz para determinar si eres un usuario registrado.  
3. **Procesamiento de Lenguaje Natural (LLM):** Las preguntas son procesadas por un modelo **Ollama** que interpreta tu intención y genera respuestas coherentes.  
4. **Síntesis de Voz (TTS):** Se convierte la respuesta generada en voz.  
5. **Mascota Virtual:** Una interfaz visual acompaña la interacción.  

---

## Instalación

### Requisitos previos

- Python 3.8 o superior  
- Conexión a internet para descargar modelos  

### Instalación 

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/Qubit.git
cd Qubit
```
Instalación Manual:
1. Crea un entorno virtual (opcional pero recomendado): 

```bash
python -m venv venv
venv\Scripts\activate  # Para Windows
source venv/bin/activate  # Para Linux/macOS
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Asegúrate de tener pip actualizado:

```bash
python -m pip install --upgrade pip
```

Intralación automática
1. Ejecuta el script de instalación de modelos y dependencias adicionales:

- **Linux:**
  
```bash
./install(linux).sh
```

- **Windows (PowerShell como administrador):**

```powershell
.\install(windows).ps1
```

---
Listo!

## Grabación de Perfiles de Voz

Para que Qubit te reconozca, necesitas grabar un perfil de voz.

### ¿Cómo grabar un perfil?

```bash
python voice_profiles/grabar_perfil.py
```

Sigue las instrucciones en pantalla.

### Nomenclatura de los archivos

Formato: `[nombre_usuario][numero].wav`  
Ejemplos válidos: `juan1.wav`, `maria2.wav`  

Los perfiles se guardan en la carpeta `voice_profiles/wavs/`.

---

## Uso del Asistente

### Iniciar Qubit

```bash
python main.py
```

### Interacción

Di "Qubit" para activarlo y luego formula tu pregunta.

---

## Estructura del Proyecto

```
.
├── main.py
├── ollama.py
├── tts.py
├── voz_listener.py
├── README.md
├── install(linux).sh
├── install(windows).ps1
├── requirements.txt
├── proyecto/
│   ├── __pycache__/
│   └── capybara/
│       ├── __pycache__/
│       ├── capybara.py
│       ├── happy.png
│       ├── sad.png
│       ├── sleep.png
│       └── surprise.png
├── stt/
│   ├── __pycache__/
│   ├── vosk-model-small-es-0.42/
│   └── stt.py
└── voice_profiles/
    ├── wavs/
    └── grabar_perfil.py
```

---

## Consejos para Mejor Uso

- Usa auriculares para evitar retroalimentación.  
- Utiliza Qubit en un ambiente silencioso.  
- Habla claro y a ritmo natural.  

---

## Archivos Principales y Sus Funciones

| Archivo/Carpeta | Función Principal |
|-----------------------------|-------------------------------|
| `main.py` | Orquestador principal del asistente |
| `ollama.py` | Interfaz para el procesamiento de lenguaje con Ollama |
| `tts.py` | Módulo para la síntesis de voz (Text-to-Speech) |
| `voz_listener.py` | Módulo principal para escuchar el activador y comandos |
| `stt/stt.py` | Transcripción de voz a texto usando Vosk |
| `proyecto/capybara/capybara.py` | Lógica de la mascota virtual |
| `voice_profiles/grabar_perfil.py` | Grabación de perfiles de voz de usuario |
| `voice_profiles/wavs/` | Almacena los perfiles de voz grabados |
| `stt/vosk-model-small-es-0.42/` | Carpeta que contiene el modelo Vosk |
| `proyecto/capybara/` | Recursos visuales de la mascota virtual |

---

## Contribuciones

¡Tu ayuda es bienvenida!

- Abre un issue para reportar errores o sugerencias.  
- Envía un pull request con tus mejoras.

---

## Licencia

Uso personal y educativo. Para otros usos, contactar a los desarrolladores.
