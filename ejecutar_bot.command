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

echo "🚀 Iniciando el proceso completo..."
echo "Por favor, no toques el teléfono..."
echo ""

# 3. Activar el entorno virtual (En Mac la ruta es diferente a Windows)
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️ No se encontró el entorno virtual (.venv)."
    echo "Asegúrate de crearlo o revisa la ruta."
fi

# 4. Ejecutar el código principal (En Mac suele usarse python3)
python3 main.py

# 5. Pausa antes de cerrar la terminal (Equivalente al 'pause' de Windows)
echo ""
read -p "Proceso terminado. Presiona [Enter] para salir..."