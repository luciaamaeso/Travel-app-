# 🔐 Configuración de Credenciales Firebase

## ⚠️ IMPORTANTE: Seguridad

**NUNCA** commitees archivos de credenciales al repositorio. Contienen secretos sensibles y están protegidos en `.gitignore`:
```
*-firebase-adminsdk-*.json
serviceAccountKey.json
```

---

## 🚀 Configuración Rápida (Local)

### Paso 1: Obtener las Credenciales

1. Ve a [🔗 Firebase Console](https://console.firebase.google.com)
2. Selecciona tu proyecto **travel-app**
3. Abre **⚙️ Configuración del proyecto** → **Cuentas de servicio**
4. Haz clic en **"Generar clave privada"**
5. Se descargará un archivo JSON automáticamente

### Paso 2: Colocar el Archivo en el Proyecto

Simplemente copia el archivo descargado a la raíz del proyecto:
```bash
cp ~/Downloads/travelappformanagement-firebase-adminsdk-*.json ./
```

**El código aceptará automáticamente cualquiera de estos nombres:**
- ✅ `serviceAccountKey.json`
- ✅ `travelappformanagement-firebase-adminsdk-*.json` (cualquier variante)

### Paso 3: Recargar la Aplicación

```bash
# Recarga la app en el navegador (F5)
# o reinicia Streamlit:
streamlit run app.py
```

---

## 🌩️ Despliegue en Streamlit Cloud (Producción)

Para evitar subir el archivo al repositorio en producción:

### Opción 1: Usar Secrets (Recomendado)

1. En tu repo, crea `.streamlit/secrets.toml`:
```toml
[firebase]
type = "service_account"
project_id = "travelappformanagement"
private_key_id = "..."
private_key = "..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

2. En `.gitignore`:
```
.streamlit/secrets.toml
```

3. En Streamlit Cloud:
   - Ve a tu app → **Settings** → **Secrets**
   - Copia el contenido de `.streamlit/secrets.toml`
   - Pega en el editor de secrets

### Opción 2: Variable de Entorno

Establece una variable de entorno `FIREBASE_CONFIG` con el JSON como string:

```bash
export FIREBASE_CONFIG='{"type":"service_account",...}'
```

---

## ✅ Verificación

Para verificar que Firebase está configurado correctamente:

```bash
python -c "import firebase_config; print('✅ Firebase configurado!' if firebase_config.ref else '❌ Error en Firebase')"
```

O simplemente corre la app:
```bash
streamlit run src/app.py
```

Si todo está bien, no verás errores de Firebase al inicio.

---

## 🐛 Solucionar Problemas

### Error: "No se encontró archivo de credenciales"
- ✅ Descargaste el archivo desde Firebase?
- ✅ Está en la carpeta raíz del proyecto?
- ✅ Recargaste la página (F5)?

### Error: "Error al leer archivo JSON"
- ✅ El archivo no está corrompido?
- ✅ Está en formato JSON válido?
- ✅ No lo editaste accidentalmente?

### Error: "No hay conexión con Firebase"
- ✅ ¿Tienes internet?
- ✅ ¿El proyecto existe en Firebase Console?
- ✅ ¿Las credenciales son del proyecto correcto?

---

## 📚 Referencias

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK (Python)](https://firebase.google.com/docs/database/admin/start)
- [Streamlit Secrets Management](https://docs.streamlit.io/deploy/streamlit-cloud/deploy-your-app/secrets-management)

