#!/bin/bash

# Script de diagnóstico para Firebase
# Ayuda a verificar que todo está configurado correctamente

echo "🔍 Firebase Diagnostics"
echo "======================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar archivo de credenciales
echo -e "${BLUE}1. Buscando archivo de credenciales...${NC}"
if [ -f "serviceAccountKey.json" ]; then
    echo -e "${GREEN}✓ serviceAccountKey.json encontrado${NC}"
    
    # Verificar que es JSON válido
    if python3 -c "import json; json.load(open('serviceAccountKey.json'))" 2>/dev/null; then
        echo -e "${GREEN}✓ JSON válido${NC}"
        
        # Mostrar proyecto
        PROJECT=$(python3 -c "import json; print(json.load(open('serviceAccountKey.json')).get('project_id', 'Desconocido'))")
        echo -e "${GREEN}  Proyecto: $PROJECT${NC}"
    else
        echo -e "${RED}✗ JSON inválido o corrupto${NC}"
    fi
else
    # Buscar otros patrones
    FOUND=$(ls *-firebase-adminsdk-*.json 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
        echo -e "${YELLOW}⚠ Encontrado: $FOUND${NC}"
        echo -e "${YELLOW}  Renombra como serviceAccountKey.json para mayor compatibilidad${NC}"
    else
        echo -e "${RED}✗ No se encontró archivo de credenciales${NC}"
        echo -e "${RED}  Falta: serviceAccountKey.json${NC}"
        echo ""
        echo "Pasos para obtenerlo:"
        echo "1. Ve a https://console.firebase.google.com"
        echo "2. Selecciona tu proyecto"
        echo "3. ⚙️ Configuración → Cuentas de servicio"
        echo "4. Genera clave privada"
        echo "5. Guarda como serviceAccountKey.json aquí"
    fi
fi
echo ""

# 2. Verificar Python
echo -e "${BLUE}2. Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYVER=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYVER${NC}"
else
    echo -e "${RED}✗ Python 3 no encontrado${NC}"
fi
echo ""

# 3. Verificar entorno virtual
echo -e "${BLUE}3. Verificando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ venv/ existe${NC}"
else
    echo -e "${YELLOW}⚠ venv/ no existe. Ejecuta: python3 -m venv venv${NC}"
fi
echo ""

# 4. Verificar paquetes de Firebase
echo -e "${BLUE}4. Verificando paquetes necesarios...${NC}"
source venv/bin/activate 2>/dev/null || true

if python3 -c "import firebase_admin" 2>/dev/null; then
    echo -e "${GREEN}✓ firebase-admin instalado${NC}"
else
    echo -e "${RED}✗ firebase-admin no instalado${NC}"
    echo "  Ejecuta: pip install firebase-admin"
fi

if python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${GREEN}✓ streamlit instalado${NC}"
else
    echo -e "${RED}✗ streamlit no instalado${NC}"
    echo "  Ejecuta: pip install streamlit"
fi
echo ""

# 5. Verificar estructura de carpetas
echo -e "${BLUE}5. Verificando estructura de carpetas...${NC}"
[ -d "src" ] && echo -e "${GREEN}✓ src/${NC}" || echo -e "${RED}✗ src/${NC}"
[ -d "docs" ] && echo -e "${GREEN}✓ docs/${NC}" || echo -e "${RED}✗ docs/${NC}"
[ -f "src/app.py" ] && echo -e "${GREEN}✓ src/app.py${NC}" || echo -e "${RED}✗ src/app.py${NC}"
[ -f "src/firebase_config.py" ] && echo -e "${GREEN}✓ src/firebase_config.py${NC}" || echo -e "${RED}✗ src/firebase_config.py${NC}"
echo ""

# 6. Probar conexión a Firebase
echo -e "${BLUE}6. Probando conexión a Firebase...${NC}"
python3 << 'PYEOF'
import sys
import json
sys.path.insert(0, 'src')

try:
    # Verificar credenciales
    if not __import__('os').path.exists('serviceAccountKey.json'):
        print("✗ Archivo de credenciales no encontrado")
        sys.exit(1)
    
    # Cargar credenciales
    with open('serviceAccountKey.json') as f:
        creds = json.load(f)
    
    print("✓ Credenciales cargadas correctamente")
    print(f"  Proyecto: {creds.get('project_id', 'Desconocido')}")
    
    # Intentar inicializar Firebase
    import firebase_admin
    from firebase_admin import credentials, db
    
    # Verificar si ya está inicializado
    try:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://travelappformanagement-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("✓ Firebase inicializado correctamente")
    except ValueError as e:
        if "already exists" in str(e):
            print("✓ Firebase ya está inicializado")
        else:
            print(f"✗ Error al inicializar: {e}")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    sys.exit(1)

PYEOF
echo ""

# Resumen
echo -e "${BLUE}Resumen:${NC}"
echo "Si todo está verde (✓), la app debería funcionar:"
echo -e "  ${YELLOW}streamlit run src/app.py${NC}"
echo ""
echo "Si hay algo rojo (✗), sigue los pasos indicados arriba."
