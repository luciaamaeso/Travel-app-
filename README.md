# 🌍 Mi Travel App 

Gestiona tus **viajes largos** y crea **itinerarios de un día** con visualización por franjas horarias.
Hecha un domingo vibecodeando para solucionar mi problema de almacenaje de planes y viajes!

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

## Stack

- **Python** 
- **Streamlit** (interfaz web)
- **SQLite** (base de datos)
- **Pandas** (tablas)

## Arrancar

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501`

## Estructura BD

### `viajes` - Viajes largos
| Campo | Descripción |
|-------|------------|
| id | ID único |
| nombre | Nombre del viaje |
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

