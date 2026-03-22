# 🌍 Mi Travel App 

Gestiona tus **viajes largos** y crea **itinerarios de un día** con visualización por franjas horarias.
Hecha un domingo vibecodeando para solucionar mi problema de almacenaje de planes y viajes!

---

## 📋 Dos secciones principales

### 🌍 **Viajes** - Para viajes largos
- Crear viajes con fechas, destino y presupuesto
- Estados: Idea → Planificado → Próximo → Completado
- **Notas categorizadas**: alojamiento, transporte, restaurantes, actividades, presupuesto, documentos
- **Lugares a visitar**: registra sitios específicos con detalles
- **Bote de ahorro**: controla el dinero ahorrado vs presupuesto
- **Estadísticas**: resumen de todos tus viajes y gastos

### 📅 **Itinerarios** - Para días específicos
- Crea itinerarios independientes con fecha y ciudad
- **Vista visual por franjas horarias** (09:00, 10:00, etc)
- Añade actividades con:
  - Hora inicio/fin
  - Ubicación
  - Notas
  - Color personalizado (8 colores disponibles)
- Todo organizados por orden de tiempo

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.8+ | Lenguaje principal |
| **Streamlit** | ≥1.32.0 | Interfaz web interactiva |
| **Firebase** | ≥6.0.0 | Base de datos en la nube |
| **Pandas** | ≥2.0.0 | Manipulación de datos |

---

## ⚡ Arranque Rápido

### Requisitos Previos
- Python 3.8 o superior
- pip o poetry
- Credenciales de Firebase configuradas

### Instalación

```bash
# Clonar repositorio
git clone <url-repositorio>
cd Travel-app-

# Crear entorno virtual
python -m venv venv

# Activar entorno
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Configurar Firebase

⚠️ **IMPORTANTE**: Consulta [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md) para configurar tus credenciales de Firebase de forma segura.

```bash
# Una vez configurado:
streamlit run app.py
```

Abre en tu navegador: `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
Travel-app-/
├── app.py                      # Aplicación principal Streamlit
├── database_firebase.py        # Operaciones con Firebase
├── database.py                 # Base de datos local (SQLite)
├── firebase_config.py          # Configuración de Firebase
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
├── SETUP_CREDENCIALES.md       # Guía de configuración de Firebase
├── config/                     # Archivos de configuración
├── data/                       # Datos locales
└── SETUP_FIREBASE.md           # Documentación adicional
```

---

## 🗄️ Estructura de la Base de Datos

### Tabla: `viajes`
Almacena los viajes largos planificados.

| Campo | Tipo | Descripción |
|-------|------|------------|
| id | UUID | ID único del viaje |
| nombre | String | Nombre del viaje |
| destino | String | Ubicación del viaje |
| fecha_inicio | Date | Fecha de inicio |
| fecha_fin | Date | Fecha de finalización |
| presupuesto | Float | Presupuesto total |
| estado | String | Idea/Planificado/Próximo/Completado |
| notas | JSON | Notas categorizadas |
| gastos | Float | Gastos acumulados |

### Tabla: `itinerarios`
Almacena los itinerarios diarios.

| Campo | Tipo | Descripción |
|-------|------|------------|
| id | UUID | ID único |
| fecha | Date | Fecha del itinerario |
| ciudad | String | Ubicación |
| actividades | JSON | Actividades por hora |

---

## 🔧 Desarrollo

### Ejecutar en modo desarrollo
```bash
streamlit run app.py --logger.level=debug
```

### Ejecutar tests (si existen)
```bash
python -m pytest
```

---

## 🔐 Seguridad

⚠️ **Confidencial**: 
- **NUNCA** commitees archivos `*-firebase-adminsdk-*.json`
- Las credenciales están protegidas en `.gitignore`
- Para colaboradores: consulta [SETUP_CREDENCIALES.md](./SETUP_CREDENCIALES.md)

---

## 📝 Licencia

Este proyecto es de uso personal.

---

## 💬 Contacto

¿Sugerencias? Abre un issue en el repositorio.

---

**Made with 💜 for travel planning**
| destino | Ciudad destino |
| pais | País |
| estado | idea / planificado / próximo / completado |
| fecha_inicio | Fecha salida |
| fecha_fin | Fecha regreso |
| presupuesto | Presupuesto en € |
| descripcion | Notas generales |
| emoji | Icono identificador |

### `notas` - Anotaciones por viaje
| Campo | Descripción |
|-------|------------|
| id | ID único |
| viaje_id | Viaje asociado |
| categoria | general / alojamiento / transporte / restaurantes / actividades / presupuesto / documentos / otros |
| contenido | La nota |

### `lugares` - Sitios a visitar
| Campo | Descripción |
|-------|------------|
| id | ID único |
| viaje_id | Viaje asociado |
| nombre | Nombre del lugar |
| ubicacion | Ubicación |
| descripcion | Detalles (horarios, entradas, etc) |

### `aportes_ahorro` - Bote de dinero
| Campo | Descripción |
|-------|------------|
| id | ID único |
| viaje_id | Viaje asociado |
| monto | Dinero ahorrado (€) |
| descripcion | Nota del aporte |

### `itinerarios_dia` - Itinerarios de un día
| Campo | Descripción |
|-------|------------|
| id | ID único |
| nombre | Nombre del itinerario |
| fecha | Fecha del día |
| ciudad | Ciudad |
| descripcion | Tema/plan del día |
| emoji | Icono identificador |

### `actividades_itinerario` - Actividades por hora
| Campo | Descripción |
|-------|------------|
| id | ID único |
| itinerario_id | Itinerario asociado |
| hora_inicio | Hora inicio (HH:MM) |
| hora_fin | Hora fin (opcional) |
| actividad | Descripción de la actividad |
| ubicacion | Dónde |
| notas | Detalles adicionales |
| color | Color de identificación |

## Características

✅ Gestión completa de viajes largos  
✅ Presupuestos y progreso de ahorro  
✅ Itinerarios visuales por hora  
✅ Búsqueda y filtros  
✅ Estadísticas de gastos

