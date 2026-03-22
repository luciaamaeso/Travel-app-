# 🌍 Mi Travel App

Una app para guardar tus viajes, ideas de destinos y no perder la cabeza viendo precios en booking a las 3 de la mañana. 

Apunta dónde quieres ir, qué quieres ver, cuánto dinero necesitas y gestionar lo ahorrado. Todo en un sitio sin tener 500 pestañas abiertas.

## Qué lleva

- Python 
- Streamlit (interfaz web)
- SQLite (base de datos simple)
- Pandas (para ver los números en tabla)

## Qué puedes hacer

- Crear viajes y dejar que se queden en "idea" una eternidad
- Marcar dónde estás en el proceso (idea, planificado, próximo o si esta hecho)
- Escribir notas sobre hoteles, vuelos, comidas, todo lo que se te ocurra
- Meter un presupuesto y ir viendo cuánto dinero pones en el bote
- Buscar viajes si tienes unos cuantos guardados ya
- Ver estadísticas generales de gastos y viajes

## Cómo arrancarlo

```bash
# Clonar (si es que lo tienes en repo)
git clone https://github.com/tu-usuario/mi-travel-app.git
cd mi-travel-app

# Crear un entorno virtual
python -m venv venv
source venv/bin/activate        # En Mac/Linux
venv\Scripts\activate           # En Windows

# Instalar las librerías
pip install -r requirements.txt

# Meter y que salga la interfaz
streamlit run app.py
```

Se te abre en `http://localhost:8501` y listo.

## Estructura

```
├── app.py          # Todo lo visual
├── database.py     # La gestión de la BD
├── requirements.txt
├── README.md       # Este archivo
└── viajes.db       # Se crea sola con los datos que vayas insertando
```

### Tabla `viajes`
Donde guardar cada trip que se te ocurra.

| Campo | Qué es |
|-------|--------|
| id | número único |
| nombre | "Viaje a Japón" o lo que sea |
| destino | ciudad destino |
| pais | país |
| estado | si es idea, está planeado, es el próximo o ya pasó |
| fecha_inicio | cuándo sale (opcional) |
| fecha_fin | cuándo vuelve (opcional) |
| presupuesto | euros que te piensa gastar |
| descripcion | notas sueltas sobre el viaje |
| emoji | un icono para identificarlo rápido |

### Tabla `notas`
Para apuntar todo lo que se te ocurra: hoteles, restaurantes, cosas que ver, documentos...

| Campo | Qué es |
|-------|--------|
| id | número único |
| viaje_id | a cuál viaje pertenece |
| categoria | tipo de nota (alojamiento, transporte, etc) |
| contenido | lo que escribas |

### Tabla `lugares`
Sitios específicos que quieres visitar en cada viaje.

| Campo | Qué es |
|-------|--------|
| id | número único |
| viaje_id | el viaje al que pertenece |
| nombre | nombre del sitio |
| ubicacion | dónde está exactamente |
| descripcion | notas (horarios, entradas, recomendaciones) |

### Tabla `aportes_ahorro`
Tu bote de dinero para cada viaje.

| Campo | Qué es |
|-------|--------|
| id | número único |
| viaje_id | el viaje para el que ahorras |
| monto | cuántos euros metes |
| descripcion | nota del aporte |
