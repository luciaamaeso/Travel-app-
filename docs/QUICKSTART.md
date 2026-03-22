# 🚀 GUÍA RÁPIDA DE INICIO

Bienvenido a **Travel App**. Aquí está todo lo que necesitas para empezar.

---

## ⚡ 3 pasos para ejecutar

### 1️⃣ Descargar credenciales Firebase (3 min)

```
https://console.firebase.google.com
  ↓
Selecciona proyecto "travel-app"
  ↓
⚙️ Configuración → Cuentas de Servicio
  ↓
"Generar clave privada" (botón)
  ↓
Guarda el archivo JSON aquí ↓
```

**El archivo se verá así:**
```
travelappformanagement-firebase-adminsdk-fbsvc-XXXXXXXX.json
```

### 2️⃣ Copiar archivo a la carpeta (1 min)

```bash
# Opción A: Arrastra el archivo a esta carpeta en tu explorador

# Opción B: Terminal
cp ~/Downloads/travelappformanagement-firebase-adminsdk-*.json ./
```

### 3️⃣ Ejecutar la app (1 min)

**Opción A - Script automático (recomendado):**
```bash
bash setup.sh
```

**Opción B - Manual:**
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run src/app.py
```

**Abre tu navegador en:** `http://localhost:8501`

---

## 📚 Documentación

| Documento | Para... |
|-----------|---------|
| [README.md](./README.md) | Descripción completa del proyecto |
| [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md) | Configurar Firebase en detalle |
| [FAQ.md](./FAQ.md) | Preguntas frecuentes y troubleshooting |
| [SETUP_FIREBASE.md](./SETUP_FIREBASE.md) | Información de Firebase |

---

## ❌ Si algo falla...

### Error: "No se encontró archivo de credenciales"
✅ ¿Descargaste el JSON desde Firebase Console?
✅ ¿Lo copiaste a **esta carpeta** (raíz)?
✅ ¿Recargaste (F5)?

**Usa el diagnóstico:**
```bash
bash firebase-diagnose.sh
```

→ Ver [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md)

### Error: "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

---

## 🎯 Próximos pasos

Una vez ejecutando la app, puedes:

1. **Crear viajes** - Guarda tus planes largos
2. **Añadir itinerarios** - Organiza días específicos
3. **Registrar gastos** - Controla tu presupuesto
4. **Compartir planes** - Invita amigos

---

## 💡 Tips

- **Desarrollo rápido:** Edita `app.py` y recarga (F5)
- **Cachear datos:** Usa `@st.cache_data` para optimizar
- **Ambiente variable:** Crea `.env` para secrets locales
- **Producción:** Ver [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md#-despliegue-en-streamlit-cloud-producción)

---

## 🆘 Necesitas ayuda?

1. Revisa [FAQ.md](./FAQ.md)
2. Lee [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md)
3. Abre un issue en GitHub

---

**¿Listo? Comienza con:**
```bash
bash setup.sh
```

O ejecuta directamente:
```bash
streamlit run src/app.py
```

¡Buen viaje! 🌍✈️
