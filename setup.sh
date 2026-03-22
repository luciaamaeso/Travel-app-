#!/bin/bash

# Setup Script para Travel App
# Este script ayuda a configurar el entorno y las credenciales

set -e

echo "🌍 Travel App - Setup Script"
echo "============================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo "✓ Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 no encontrado${NC}"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} encontrado${NC}"
echo ""

# Crear entorno virtual
echo "✓ Configurando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi
echo ""

# Activar entorno
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"
echo ""

# Instalar dependencias
echo "✓ Instalando dependencias..."
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Verificar credenciales
echo "✓ Verificando credenciales Firebase..."
if ls *-firebase-adminsdk-*.json 1> /dev/null 2>&1 || [ -f "serviceAccountKey.json" ]; then
    echo -e "${GREEN}✓ Archivo de credenciales encontrado${NC}"
    echo ""
    echo -e "${GREEN}✓ Setup completado!${NC}"
    echo ""
    echo "Para iniciar la aplicación, ejecuta:"
    echo -e "${YELLOW}streamlit run src/app.py${NC}"
else
    echo -e "${YELLOW}⚠ No se encontró archivo de credenciales${NC}"
    echo ""
    echo "Pasos para obtener las credenciales:"
    echo "1. Ve a https://console.firebase.google.com"
    echo "2. Selecciona tu proyecto 'travel-app'"
    echo "3. Ve a ⚙️ Configuración → Cuentas de Servicio"
    echo "4. Haz clic en 'Generar clave privada'"
    echo "5. Guarda el archivo JSON en esta carpeta"
    echo ""
    echo "O ver: docs/SETUP_CREDENCIALES.md"
    echo ""
    echo "Una vez tengas el archivo, ejecuta:"
    echo -e "${YELLOW}streamlit run src/app.py${NC}"
fi
