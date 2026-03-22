# ⚙️ Setup Firebase para Travel App

## 🔧 Paso 1: Crear proyecto en Firebase

1. Ve a [firebase.google.com](https://firebase.google.com)
2. Inicia sesión con tu Gmail
3. Click en "Ir a consola"
4. **"Crear proyecto"**
   - Nombre: `travel-app`
   - Click en "Crear proyecto"
   - Espera a que se cree
5. Una vez creado, ve a **Realtime Database**:
   - Click izquierdo en menú > Build > Realtime Database
   - "Crear base de datos"
   - Ubicación: `europe-west1` (o la más cercana a ti)
   - Modo: **Comenzar en modo de prueba**
   - "Crear"

## 🔑 Paso 2: Obtener credenciales

1. Abre **Project Settings** (⚙️ en la esquina superior izquierda)
2. Ve a la pestaña **Service Accounts**
3. Click **"Generate New Private Key"**
4. Guarda el archivo descargado como `serviceAccountKey.json` en tu carpeta del proyecto

## 📍 Paso 3: Actualizar URL de Firebase

1. En Firebase Console, ve a **Realtime Database**
2. Copia la URL que ves en la parte superior (ej: `https://travel-app-abc123.firebaseio.com`)
3. Abre `firebase_config.py` en tu proyecto
4. Reemplaza `[YOUR_PROJECT_ID]` con tu ID de proyecto (la parte entre `https://` y `.firebaseio.com`)

Ejemplo:
```python
'databaseURL': 'https://travel-app-abc123.firebaseio.com'
```

## 💻 Paso 4: Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ya está sincronizado con Firebase. Los cambios se guardan en tiempo real.

## ☁️ Paso 5: Deployer en Streamlit Cloud

1. Sube todo a GitHub incluyendo `serviceAccountKey.json`:
```bash
git add .
git commit -m "Migración a Firebase"
git push origin main
```

2. En Streamlit Cloud, cuando deploys tu app:
   - Ve a **App menu** (⋮) → Settings
   - **Secrets** → **Add secret**
   - Key: `FIREBASE_CONFIG`
   - Value: Copia todo el contenido de `serviceAccountKey.json` como JSON

3. Streamlit usará automáticamente la variable de entorno en lugar del archivo local

## 🔒 Reglas de seguridad (opcional pero recomendado)

En Firebase Console > Realtime Database > Rules:

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

⚠️ Esto permite que cualquiera lea y escriba. Para producción, personaliza las reglas según necesites.

## ✅ Listo

¡Ya está! Ahora:
- Los datos se sincronizan en tiempo real
- Funciona desde móvil y ordenador
- Todos los usuarios comparten la misma BD
- Los datos persisten en la nube
