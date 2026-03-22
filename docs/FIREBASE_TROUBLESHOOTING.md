# 🔧 Solución de Problemas - Firebase

## ❌ "No hay conexión con Firebase"

Este es el error más común. Aquí está cómo solucionarlo.

---

## 🚨 Paso 1: Diagnosticar

Ejecuta el script de diagnóstico:
```bash
bash firebase-diagnose.sh
```

Este script verificará:
✓ Archivo de credenciales  
✓ Python y paquetes  
✓ Estructura de carpetas  
✓ Conexión a Firebase  

**Todos deben estar en verde (✓).**

---

## 📋 Paso 2: Verificar Archivo de Credenciales

### ¿Dónde debe estar el archivo?

```
Travel-app-/
├── serviceAccountKey.json  ← DEBE ESTAR AQUÍ (raíz)
├── src/
│   ├── app.py
│   └── firebase_config.py
├── docs/
└── ...
```

**NO aquí:**
```
Travel-app-/
├── src/
│   └── serviceAccountKey.json  ← ❌ INCORRECTO
```

### Mover el archivo a la ubicación correcta

Si lo colocaste en la carpeta equivocada:
```bash
# Mover desde src/ a raíz
mv src/serviceAccountKey.json ./serviceAccountKey.json

# Mover desde docs/ a raíz
mv docs/serviceAccountKey.json ./serviceAccountKey.json
```

---

## 🔐 Paso 3: Verificar Contenido del Archivo

El archivo debe ser un JSON válido y contener:
```json
{
  "type": "service_account",
  "project_id": "travelappformanagement",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "...",
  ...
}
```

**Verificar que es válido:**
```bash
python3 -c "import json; json.load(open('serviceAccountKey.json')); print('✓ JSON válido')"
```

---

## 🔄 Paso 4: Descargar Nuevas Credenciales

Si el archivo está corrupto o falta, descargalo nuevamente:

1. Ve a [🔗 Firebase Console](https://console.firebase.google.com)
2. Selecciona proyecto **travel-app**
3. ⚙️ **Configuración del Proyecto** → **Cuentas de servicio**
4. En la tabla, busca tu cuenta de servicio
5. Haz clic en el **menú (⋯)** → **Generar clave privada**
6. Se descargará automáticamente
7. Guarda en la raíz con nombre: `serviceAccountKey.json`

---

## 🌐 Paso 5: Verificar Conexión a Internet

```bash
# Prueba conexión
ping google.com

# Si no funciona, comprueba tu wifi/ethernet
```

---

## 🏗️ Paso 6: Verificar Proyecto Firebase

1. Abre [Firebase Console](https://console.firebase.google.com)
2. Verifica que el proyecto **travel-app** existe
3. Comprueba que está **activo** (no suspendido)
4. Entra a **Realtime Database** → Verifica que existe

---

## 🚀 Paso 7: Reiniciar Todo

Después de cualquier cambio:

```bash
# Opción A: Recargar en navegador
# Presiona F5 si la app ya está corriendo

# Opción B: Reiniciar Streamlit
# Presiona Ctrl+C en la terminal
# Luego ejecuta:
streamlit run src/app.py
```

---

## 📊 Checklist Completo

- [ ] ¿`serviceAccountKey.json` está en la raíz?
- [ ] ¿El archivo es JSON válido?
- [ ] ¿Tienes internet?
- [ ] ¿El proyecto existe en Firebase?
- [ ] ¿Reiniciaste Streamlit (F5)?
- [ ] ¿El proyecto_id en el JSON es "travelappformanagement"?

Si todo está OK pero aún falla:

```bash
# Ejecuta diagnóstico nuevamente
bash firebase-diagnose.sh

# Ver logs detallados
streamlit run src/app.py --logger.level=debug
```

---

## 🆘 Errores Específicos

### "Firebase app is already initialized"
Normal en desarrollo. Reinicia Streamlit:
```bash
# Presiona Ctrl+C
# Luego: streamlit run src/app.py
```

### "Invalid service account"
El JSON es inválido o de otro proyecto:
1. Descarga nuevas credenciales
2. Verifica que sea del proyecto correcto
3. Reemplaza el archivo

### "Database not found"
La Realtime Database no existe en Firebase:
1. Ve a Firebase Console
2. Ve a **Realtime Database**
3. Crea una si no existe

### "Permission denied"
Las reglas de seguridad de Firebase te lo impiden:
1. Ve a Firebase Console
2. **Realtime Database** → **Reglas**
3. Asegúrate de que permiten lectura/escritura (para desarrollo)

---

## 💡 Tips

- **Problema persiste?** Descarga credenciales nuevamente
- **Desarrollo local?** Las reglas pueden ser más permisivas
- **Producción?** Usa variables de entorno (ver [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md))

---

## 📚 Más recursos

- [Firebase Troubleshooting](https://firebase.google.com/docs/database/connectivity)
- [Firebase Admin SDK](https://firebase.google.com/docs/database/admin/start)
- [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md)
- [FAQ.md](./FAQ.md)
