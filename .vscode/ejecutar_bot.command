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
# Esto borra cambios locales accidentales para evitar conflictos
git reset --hard HEAD --quiet
git pull origin main --quiet
echo "✔️ Actualizado."
echo ""

# 3. Iniciar el servidor de Appium en segundo plano
echo "📱 Iniciando servidor Appium..."
# Cierra cualquier proceso previo de node/appium para evitar errores de puerto ocupado
killall node 2>/dev/null
appium &
sleep 5 # Espera 5 segundos a que Appium inicie correctamente

# 4. Revisar, crear y activar el entorno virtual AUTOMÁTICAMENTE
if [ ! -d ".venv" ]; then
    echo "⚠️ Entorno nuevo detectado. Configurando la Mac (tardará un minuto)..."
    python3 -m venv .venv
    source .venv/bin/activate
    
    echo "📦 Instalando librerías necesarias..."
    pip install Appium-Python-Client selenium
    echo "✔️ Instalación completa."
else
    source .venv/bin/activate
fi

# 5. Configurar variables de Android para Appium
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools

echo ""
echo "🚀 Iniciando el proceso completo..."
echo "Por favor, no toques el teléfono..."
echo ""

# 6. Ejecutar el código principal
python3 main.py

# 7. Limpieza y cierre
echo ""
echo "🛑 Cerrando Appium..."
killall node 2>/dev/null

read -p "Proceso terminado. Presiona [Enter] para salir..."