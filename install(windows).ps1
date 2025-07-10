
# Verifica si hay python instalado
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python no está instalado o no está en el PATH. Instálalo primero." -ForegroundColor Red
    exit
}

Write-Host "Creando entorno virtual..."
python -m venv venv

Write-Host "Activando entorno virtual..."
# Para PowerShell
. .\venv\Scripts\Activate.ps1

Write-Host "Actualizando pip..."
pip install --upgrade pip

Write-Host "Instalando dependencias..."
pip install -r requirements.txt

Write-Host "¡Listo! Para activar el entorno virtual usa:"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "Y para ejecutar el proyecto:"
Write-Host "  python main.py"
