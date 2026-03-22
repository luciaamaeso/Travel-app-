# 🌍 Travel App

Una aplicación web moderna para **planificar viajes completos** con itinerarios diarios detallados, control de gastos, seguimiento de ahorros y mucho más. Perfecto para viajeros que quieren organizar cada momento de su aventura.
Hecha un domingo vibecodeando para solucionar mi problema de almacenaje de planes y viajes!


**🚀 [Ir al Inicio Rápido](#-inicio-rápido) • 📖 [Documentación](./docs/) • ❓ [FAQ](./docs/FAQ.md)**

---

## ✨ Características Principales

### 🧳 Gestión de Viajes
- ✅ Crear viajes con destino, país, fechas y presupuesto
- ✅ Editar y eliminar viajes (con eliminación en cascada de datos relacionados)
- ✅ Seleccionar/deseleccionar viajes con sistema visual (⭕/🔘)
- ✅ Ver estado del viaje (Planeando, En curso, Completado)
- ✅ Asignar emoji personalizado a cada viaje

### 📅 Itinerarios Automáticos
- ✅ **Generación automática**: 1 itinerario por día en tu rango de fechas
- ✅ Crear itinerarios adicionales con nombre y fecha personalizados
- ✅ Organizar actividades por franjas horarias
- ✅ Ver itinerarios en vista expandida por día

### 🗺️ Actividades y Lugares
- ✅ Agregar actividades a itinerarios con hora de inicio/fin
- ✅ Registrar ubicación de cada actividad
- ✅ Añadir notas y elegir color de categoría
- ✅ Guardar lugares de interés con descripción
- ✅ Eliminar actividades y lugares fácilmente

### 💰 Control Financiero
- ✅ Establecer presupuesto para cada viaje
- ✅ Registrar aportes/ahorros con descripción opcional
- ✅ Barra de progreso visual del porcentaje de ahorro
- ✅ **🎯 Badge automático "✅ Listo para viajar"** cuando alcanzas el 100% de ahorro
- ✅ Lista de todas las contribuciones al bote de ahorro

### 📊 Estadísticas y Análisis
- ✅ Estadísticas de viajes: cantidad, destinos más frecuentes, presupuesto total
- ✅ Estadísticas de itinerarios: total creados, promedio por viaje
- ✅ Estadísticas de actividades: cantidad registrada, categorías más usadas
- ✅ Estadísticas de ahorros: total ahorrado, promedio por viaje

### 🌐 Sincronización en la Nube
- ✅ Todos los datos se guardan en **Firebase Realtime Database**
- ✅ Acceso a tus viajes desde cualquier dispositivo
- ✅ Sincronización en tiempo real

---

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8 o superior
- Cuenta de Firebase (gratis en [firebase.google.com](https://console.firebase.google.com))
- Git

### Pasos de Instalación

**1️⃣ Clonar el repositorio**
```bash
git clone <URL-del-repo>
cd Travel-app-
```

**2️⃣ Instalar dependencias**
```bash
bash setup.sh
```

O manualmente:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3️⃣ Configurar Firebase**
- Ve a [Firebase Console](https://console.firebase.google.com)
- Selecciona o crea un proyecto
- ⚙️ Configuración del proyecto → Cuentas de Servicio
- Genera una clave privada (JSON)
- Guarda el archivo como `serviceAccountKey.json` en la **raíz del proyecto**

**4️⃣ Ejecutar la aplicación**
```bash
streamlit run src/app.py
```

La app se abrirá en `http://localhost:8501` ✨

### ❓ Diagnóstico
Si algo no funciona:
```bash
bash firebase-diagnose.sh
```

---

## 📖 Cómo Usar la App

### Vista General
La app tiene dos paneles principales:

#### 📌 Barra Lateral (Navegación)
- **Viajes**: Gestiona todos tus viajes
- **Estadísticas**: Visualiza datos y análisis

#### 🎯 Sección de Viajes
1. **Lista de Viajes**: Haz clic en ⭕ para seleccionar un viaje
2. **Opciones**: Una vez seleccionado aparecen 3 botones:
   - 👁️ **Ver**: Ve los detalles completos
   - ✏️ **Editar**: Modifica nombre, fechas, presupuesto, etc.
   - 🗑️ **Eliminar**: Borra el viaje (¡también borra itinerarios y actividades!)

### Crear un Viaje
1. Haz clic en **"+ Nuevo viaje"**
2. Completa:
   - **Nombre**: Ej. "Viaje a Japón"
   - **Destino**: Ej. "Tokio"
   - **País**: Ej. "Japón"
   - **Presupuesto**: Tu presupuesto total en €
   - **Descripción** (opcional): Notas adicionales
   - **Emoji**: Elige uno que represente tu viaje
   - **¿Sin fechas?** (checkbox): Marca si prefieres no definir fechas aún

3. Si defines **fechas de inicio y fin**, la app **creará automáticamente 1 itinerario por cada día** 🎉

### Ver Detalles del Viaje
Haz clic en 👁️ **Ver** para acceder a:

#### Información General
- Nombre, destino, país, estado, presupuesto
- Descripción y emoji asignado

#### 📅 Itinerarios
- Lista de itinerarios del viaje
- Click en un itinerario para expandirlo y ver:
  - **Actividades por hora** organizadas en orden cronológico
  - Cada actividad muestra: hora, nombre, ubicación, notas y color

#### ➕ Crear Itinerario Adicional
- Agrega itinerarios extras (no automáticos) con nombre y fecha personalizados

#### 🗺️ Lugares de Interés
- Lista de lugares que quieres visitar
- Click en ➕ para agregar nuevo lugar
- Cada lugar tiene: nombre, dirección, descripción

#### 🪙 Bote de Ahorro
- **Progreso visual** de tu ahorro contra el presupuesto
- **Desglose**: Ahorrado, Objetivo, Falta por ahorrar
- **✅ Listo para viajar**: Aparece cuando alcanzas el 100% del ahorro
- Botón ➕ para agregar dinero al bote
- Lista de todos tus aportes con fechas

### Gestionar Actividades
En cada itinerario expandido:
1. Haz clic en ➕ **Agregar actividad**
2. Completa:
   - **Hora de inicio y fin**: Franja horaria
   - **Actividad**: Nombre de la actividad
   - **Ubicación**: Dónde se realiza
   - **Color**: Categoriza visualmente
   - **Notas**: Detalles adicionales

### Ver Estadísticas
Desde la barra lateral:
1. **Estadísticas - Viajes**: Datos sobre todos tus viajes
2. **Estadísticas - Itinerarios**: Información de itinerarios
3. **Estadísticas - Actividades**: Análisis de actividades
4. **Estadísticas - Ahorros**: Tracking de dinero guardado

---

## 📁 Estructura del Proyecto

```
Travel-app-/
├── 📖 docs/                          # Documentación detallada
│   ├── QUICKSTART.md                 # Guía rápida de 5 minutos
│   ├── README.md                     # Descripción completa
│   ├── FAQ.md                        # Preguntas frecuentes
│   ├── SETUP_CREDENCIALES.md         # Cómo obtener credenciales Firebase
│   ├── SETUP_FIREBASE.md             # Info adicional de Firebase
│   ├── FIREBASE_TROUBLESHOOTING.md   # Solución de problemas
│   └── ERROR_NONETYPE.md             # Referencia de errores
│
├── 💻 src/                           # Código fuente
│   ├── app.py                        # Aplicación principal (Streamlit)
│   ├── database_firebase.py          # Funciones de BD con Firebase
│   ├── database.py                   # BD local (fallback)
│   └── firebase_config.py            # Configuración de Firebase
│
├── ⚙️ config/                        # Archivos de configuración
├── 💾 data/                          # Datos locales (si aplica)
│
├── 📋 requirements.txt               # Dependencias Python
├── 🔧 setup.sh                       # Script de instalación automática
├── 🔍 firebase-diagnose.sh           # Script de diagnóstico
├── 📄 .env.example                   # Variables de entorno (ejemplo)
├── 🚫 .gitignore                     # Archivos a ignorar en Git
│
└── 📦 venv/                          # Entorno virtual (no subir a Git)
```

---

## 🛠️ Tech Stack

| Tecnología | Uso |
|-----------|-----|
| **Python 3.12** | Lenguaje principal |
| **Streamlit** | Framework web interactivo |
| **Firebase Realtime DB** | Base de datos en la nube |
| **firebase-admin** | SDK de Firebase para Python |
| **Pandas** | Manipulación y análisis de datos |

---

## 📚 Documentación Adicional

| Documento | Contenido |
|-----------|----------|
| **[QUICKSTART.md](./docs/QUICKSTART.md)** | Guía rápida de 5 minutos |
| **[FAQ.md](./docs/FAQ.md)** | Preguntas frecuentes |
| **[SETUP_CREDENCIALES.md](./docs/SETUP_CREDENCIALES.md)** | Pasos para obtener credenciales Firebase |
| **[SETUP_FIREBASE.md](./docs/SETUP_FIREBASE.md)** | Info técnica de Firebase |
| **[FIREBASE_TROUBLESHOOTING.md](./docs/FIREBASE_TROUBLESHOOTING.md)** | Solución de problemas |

---

## ⚠️ Notas Importantes

### Datos en la Nube
- Todos los datos se guardan en **Firebase** automáticamente
- Asegúrate de mantener `serviceAccountKey.json` **seguro** (no lo subas a Git)
- Las credenciales en `.gitignore` están protegidas

### Eliminación de Viajes
- Al eliminar un viaje, **se eliminan también**:
  - ✅ Todos sus itinerarios
  - ✅ Todas las actividades de esos itinerarios
  - ✅ Todos los aportes/ahorros del viaje
  - ✅ Todos los lugares de interés del viaje

### Itinerarios Automáticos
- Si defines fechas al crear/editar un viaje, se crean automáticamente itinerarios
- **1 itinerario por día** en el rango de fechas seleccionado
- Puedes agregar más itinerarios manualmente después

---

## 💜 Soporte

¿Preguntas o problemas?
- 📖 Consulta la [Documentación](./docs/)
- ❓ Revisa las [Preguntas Frecuentes](./docs/FAQ.md)
- 🔍 Ejecuta el diagnóstico: `bash firebase-diagnose.sh`

---

**Hecho con 💜 para viajeros que aman planificar** ✈️🌍

