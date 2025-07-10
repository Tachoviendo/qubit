
#!/bin/bash

# setup.sh - Script para preparar entorno y dependencias

echo "Creando entorno virtual..."
python3 -m venv venv

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Actualizando pip..."
pip install --upgrade pip

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "¡Listo! Para activar el entorno virtual usa:"
echo "  source venv/bin/activate"
echo "Y para ejecutar el proyecto:"
echo "  python main.py"
