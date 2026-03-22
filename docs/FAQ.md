# ❓ Preguntas Frecuentes - Travel App

## Firebase & Credenciales

### P: ¿Dónde obtengo el archivo de credenciales?

**R:** En Firebase Console:
1. Abre [firebase.google.com](https://firebase.google.com)
2. Selecciona tu proyecto
3. Ve a **⚙️ Configuración** → **Cuentas de Servicio**
4. Haz clic en **"Generar clave privada"**
5. Se descargará automáticamente un JSON

### P: ¿Dónde coloco el archivo descargado?

**R:** En la raíz del proyecto (misma carpeta que `app.py`):
```
Travel-app-/
├── app.py
├── firebase_config.py
├── serviceAccountKey.json  ← AQUÍ o
├── travelappformanagement-firebase-adminsdk-*.json  ← O AQUÍ
└── ...
```

El código acepta **ambos nombres** automáticamente.

### P: ¿Es seguro subir el archivo al repositorio?

**R:** **NO**, nunca. El archivo está en `.gitignore` para protegerlo.
Contiene secretos sensibles que podrían comprometer tu cuenta.

### P: ¿Qué hago si cometí el error de subirlo?

**R:** Si ya subiste el archivo a Git:
```bash
# Eliminar del historio de Git (NO del disco)
git rm --cached serviceAccountKey.json

# Hacer commit
git commit -m "Remove Firebase credentials from history"

# Forzar actualizar el repositorio remoto
git push origin main --force

# Regenerar las credenciales en Firebase Console
```

### P: ¿Cómo funciona en producción (Streamlit Cloud)?

**R:** Usa Secrets Management:
1. En GitHub, sube el código sin credenciales
2. En Streamlit Cloud, ve a **Settings** → **Secrets**
3. Pega tu JSON descargado allí
4. Streamlit cargará automáticamente las variables de entorno

Ver [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md) para detalles.

---

## Desarrollo

### P: ¿Cómo ejecuto la aplicación?

**R:**
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (si es primera vez)
pip install -r requirements.txt

# Ejecutar la app
streamlit run src/app.py
```

Abre `http://localhost:8501` en tu navegador.

### P: ¿Qué Python debo usar?

**R:** Python 3.8 o superior. Verifica con:
```bash
python --version
# o
python3 --version
```

### P: ¿Cómo hago cambios a la base de datos?

**R:** Hay dos bases de datos:
- **SQLite** (`viajes.db`): Local, para desarrollo
- **Firebase Realtime DB**: En la nube, para producción

Puedes configurar cuál usar en `database_firebase.py` y `database.py`.

### P: ¿Qué paquetes necesito?

**R:** Ver `requirements.txt`:
```bash
pip install -r requirements.txt
```

O instalar uno por uno:
```bash
pip install streamlit pandas firebase-admin
```

---

## Solución de Problemas

### P: Error: "No se encontró archivo de credenciales"

**R:** 
1. ¿Descargaste el archivo desde Firebase?
2. ¿Lo copiaste a la raíz del proyecto?
3. ¿Está en formato `.json`?
4. ¿Recargaste la página (F5)?

### P: Error: "ModuleNotFoundError: No module named 'streamlit'"

**R:**
```bash
# Asegúrate de tener el entorno virtual activado
source venv/bin/activate

# Instala los paquetes
pip install -r requirements.txt
```

### P: La app carga pero no muestra datos

**R:** Probablemente sea un problema de conexión con Firebase:
1. ¿Tienes internet?
2. ¿Las credenciales son del proyecto correcto?
3. ¿Existe la base de datos en Firebase?
4. Revisa los logs en la consola

### P: ¿Cómo veo los logs/errores?

**R:** En la terminal donde ejecutaste `streamlit run app.py` verás los errores.
También puedes abrir la consola del navegador (F12).

---

## Colaboración

### P: Quiero contribuir al proyecto

**R:**
1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Haz cambios y commits
4. Sube tu rama: `git push origin feature/mi-feature`
5. Abre un Pull Request

### P: ¿Cuál es la estructura de carpetas?

**R:**
```
Travel-app-/
├── app.py                 # Aplicación principal
├── database_firebase.py   # Operaciones con Firebase
├── database.py            # Base de datos local (SQLite)
├── firebase_config.py     # Configuración Firebase
├── requirements.txt       # Dependencias Python
├── config/               # Archivos de configuración
├── data/                 # Datos locales/caché
├── .gitignore           # Archivos ignorados por Git
├── README.md            # Este archivo
├── SETUP_CREDENCIALES.md # Guía de credenciales
└── venv/                # Entorno virtual (no subir a Git)
```

---

## Performance & Optimización

### P: ¿La app se siente lenta?

**R:** Streamlit recarga todo cuando cambias código. Para desarrollo más rápido:
```bash
streamlit run app.py --logger.level=debug
```

O usa `@st.cache_data` para cachear datos costosos.

### P: ¿Cuál es el límite de datos en Firebase?

**R:** Firebase Realtime Database tiene límites por plan:
- **Spark (gratuito)**: 1 GB
- **Blaze (pay-as-you-go)**: Sin límite

Ve a Firebase Console para ver tu uso.

---

## Más Ayuda

- 📖 [Documentación Streamlit](https://docs.streamlit.io)
- 🔥 [Documentación Firebase](https://firebase.google.com/docs)
- 🐍 [Documentación Python](https://docs.python.org/3)
- 💬 Abre un issue en el repositorio
