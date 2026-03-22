# 🔐 Configuración de Credenciales Firebase

## ⚠️ IMPORTANTE: Seguridad

**NUNCA** commitees el archivo `travelappformanagement-firebase-adminsdk-fbsvc-*.json` al repositorio. Contiene credenciales sensibles.

## Pasos de Configuración

### 1. Obtener las Credenciales
1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto
3. Ve a **Configuración del proyecto** → **Cuentas de servicio**
4. Haz clic en **Generar clave privada**
5. Guarda el archivo JSON descargado

### 2. Colocar el Archivo
```bash
# Coloca el archivo descargado en la raíz del proyecto:
cp ~/Downloads/travelappformanagement-firebase-adminsdk-*.json ./
```

### 3. Verificar .gitignore
El archivo está protegido en `.gitignore` - será ignorado automáticamente:
```
*-firebase-adminsdk-*.json
```

## Variables de Entorno (Opcional)

Si prefieres usar variables de entorno, crea un archivo `.env`:
```bash
FIREBASE_CONFIG_PATH=/path/to/your/serviceAccountKey.json
```

Luego actualiza `firebase_config.py` para usarlo:
```python
import os
config_path = os.getenv('FIREBASE_CONFIG_PATH', 'serviceAccountKey.json')
```

## Verificación

Para verificar que todo está configurado correctamente:
```bash
python -c "import firebase_admin; print('✅ Firebase configurado correctamente')"
```
