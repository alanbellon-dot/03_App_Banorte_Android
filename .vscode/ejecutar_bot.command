#!/bin/bash

# 1. Asegura que la terminal se ubique en la carpeta donde está este archivo
cd "$(dirname "$0")"

clear
echo "=============================================="
echo "      AUTOMATIZACIÓN DE SINIESTROS (MAC)      "
echo "=============================================="
echo ""

# 2. Jalar los últimos cambios de GitHub de forma automática
echo "🔄 Buscando actualizaciones en la nube..."
git pull origin main --quiet
echo "✔️ Actualizado."
echo ""

# 3. Revisar, crear y activar el entorno virtual AUTOMÁTICAMENTE
if [ ! -d ".venv" ]; then
    echo "⚠️ Entorno nuevo detectado. Configurando la Mac automáticamente (esto tardará un minuto)..."
    python3 -m venv .venv
    source .venv/bin/activate
    
    echo "📦 Instalando Appium y librerías..."
    # Si tienes un requirements.txt usa: pip install -r requirements.txt
    pip install Appium-Python-Client
    echo "✔️ Instalación completa."
else
    # Si ya existe, solo lo activa rápido
    source .venv/bin/activate
fi

echo ""
echo "🚀 Iniciando el proceso completo..."
echo "Por favor, no toques el teléfono..."
echo ""

# 4. Ejecutar el código principal
python3 main.py

# 5. Pausa antes de cerrar
echo ""
read -p "Proceso terminado. Presiona [Enter] para salir..."