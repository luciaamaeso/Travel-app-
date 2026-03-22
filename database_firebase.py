import firebase_admin
from firebase_admin import db
from datetime import datetime
from firebase_config import ref
import streamlit as st

# ──────────────────────────────────────────────
#  VALIDACIÓN DE CONEXIÓN
# ──────────────────────────────────────────────

def verificar_conexion():
    """Verifica si Firebase está disponible"""
    if ref is None:
        st.error("❌ No hay conexión con Firebase. Por favor, sigue estos pasos:\n\n"
                 "1. Ve a https://firebase.google.com\n"
                 "2. Abre tu proyecto 'travel-app'\n"
                 "3. ⚙️ Settings → Service Accounts\n"
                 "4. 'Generate New Private Key'\n"
                 "5. Guarda como `serviceAccountKey.json` en la carpeta del proyecto\n"
                 "6. Recarga la app (F5)")
        st.stop()

# ──────────────────────────────────────────────
#  INICIALIZAR BD
# ──────────────────────────────────────────────

def inicializar_db():
    """Crea la estructura base en Firebase si no existe"""
    verificar_conexion()
    
    # Crear estructura base
    try:
        ref.child('viajes').set({}) if not ref.child('viajes').get().val() else None
        ref.child('notas').set({}) if not ref.child('notas').get().val() else None
        ref.child('lugares').set({}) if not ref.child('lugares').get().val() else None
        ref.child('aportes_ahorro').set({}) if not ref.child('aportes_ahorro').get().val() else None
        ref.child('itinerarios_dia').set({}) if not ref.child('itinerarios_dia').get().val() else None
        ref.child('actividades_itinerario').set({}) if not ref.child('actividades_itinerario').get().val() else None
    except Exception as e:
        st.error(f"Error al inicializar la BD: {e}")



# ──────────────────────────────────────────────
#  VIAJES
# ──────────────────────────────────────────────

def crear_viaje(nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji):
    """Crear un nuevo viaje"""
    viajes_ref = ref.child('viajes')
    datos = viajes_ref.get()
    
    # Obtener el siguiente ID
    viaje_id = len(datos.val() or {}) + 1
    
    nuevo_viaje = {
        'id': viaje_id,
        'nombre': nombre,
        'destino': destino,
        'pais': pais,
        'estado': estado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'presupuesto': presupuesto,
        'descripcion': descripcion,
        'emoji': emoji,
        'creado_en': datetime.now().isoformat()
    }
    
    viajes_ref.child(str(viaje_id)).set(nuevo_viaje)
    return viaje_id


def obtener_viajes(filtro_estado=None, busqueda=None):
    """Obtener todos los viajes con filtros opcionales"""
    datos = ref.child('viajes').get().val() or {}
    viajes = list(datos.values()) if isinstance(datos, dict) else []
    
    # Filtrar por estado
    if filtro_estado and filtro_estado != "todos":
        viajes = [v for v in viajes if v.get('estado') == filtro_estado]
    
    # Filtrar por búsqueda
    if busqueda:
        busqueda_lower = busqueda.lower()
        viajes = [v for v in viajes if 
                 busqueda_lower in v.get('nombre', '').lower() or
                 busqueda_lower in v.get('destino', '').lower() or
                 busqueda_lower in v.get('pais', '').lower()]
    
    # Ordenar por fecha de creación (más recientes primero)
    viajes.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    return viajes


def obtener_viaje(viaje_id):
    """Obtener un viaje específico"""
    dato = ref.child('viajes').child(str(viaje_id)).get().val()
    return dato if dato else None


def actualizar_viaje(viaje_id, nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji):
    """Actualizar un viaje existente"""
    viaje = obtener_viaje(viaje_id)
    if not viaje:
        return
    
    viaje_actualizado = {
        'id': viaje_id,
        'nombre': nombre,
        'destino': destino,
        'pais': pais,
        'estado': estado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'presupuesto': presupuesto,
        'descripcion': descripcion,
        'emoji': emoji,
        'creado_en': viaje.get('creado_en')
    }
    
    ref.child('viajes').child(str(viaje_id)).set(viaje_actualizado)


def eliminar_viaje(viaje_id):
    """Eliminar un viaje y todos sus datos asociados"""
    ref.child('viajes').child(str(viaje_id)).delete()
    
    # Eliminar notas asociadas
    notas = ref.child('notas').get().val() or {}
    for nota_id, nota in notas.items():
        if nota.get('viaje_id') == viaje_id:
            ref.child('notas').child(nota_id).delete()
    
    # Eliminar lugares asociados
    lugares = ref.child('lugares').get().val() or {}
    for lugar_id, lugar in lugares.items():
        if lugar.get('viaje_id') == viaje_id:
            ref.child('lugares').child(lugar_id).delete()
    
    # Eliminar aportes asociados
    aportes = ref.child('aportes_ahorro').get().val() or {}
    for aporte_id, aporte in aportes.items():
        if aporte.get('viaje_id') == viaje_id:
            ref.child('aportes_ahorro').child(aporte_id).delete()


def estadisticas():
    """Obtener estadísticas generales"""
    viajes = obtener_viajes()
    
    return {
        'total': len(viajes),
        'ideas': len([v for v in viajes if v.get('estado') == 'idea']),
        'planificados': len([v for v in viajes if v.get('estado') == 'planificado']),
        'proximos': len([v for v in viajes if v.get('estado') == 'próximo']),
        'completados': len([v for v in viajes if v.get('estado') == 'completado']),
        'presupuesto_total': sum(float(v.get('presupuesto', 0)) for v in viajes)
    }


# ──────────────────────────────────────────────
#  NOTAS
# ──────────────────────────────────────────────

def agregar_nota(viaje_id, categoria, contenido):
    """Agregar una nota a un viaje"""
    notas_ref = ref.child('notas')
    datos = notas_ref.get().val() or {}
    nota_id = len(datos) + 1
    
    nota = {
        'id': nota_id,
        'viaje_id': viaje_id,
        'categoria': categoria,
        'contenido': contenido,
        'creado_en': datetime.now().isoformat()
    }
    
    notas_ref.child(str(nota_id)).set(nota)
    return nota_id


def obtener_notas(viaje_id):
    """Obtener todas las notas de un viaje"""
    datos = ref.child('notas').get().val() or {}
    notas = [n for n in datos.values() if isinstance(n, dict) and n.get('viaje_id') == viaje_id]
    notas.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    return notas


def eliminar_nota(nota_id):
    """Eliminar una nota"""
    ref.child('notas').child(str(nota_id)).delete()


# ──────────────────────────────────────────────
#  LUGARES
# ──────────────────────────────────────────────

def agregar_lugar(viaje_id, nombre, ubicacion=None, descripcion=None):
    """Agregar un lugar a un viaje"""
    lugares_ref = ref.child('lugares')
    datos = lugares_ref.get().val() or {}
    lugar_id = len(datos) + 1
    
    lugar = {
        'id': lugar_id,
        'viaje_id': viaje_id,
        'nombre': nombre,
        'ubicacion': ubicacion,
        'descripcion': descripcion,
        'creado_en': datetime.now().isoformat()
    }
    
    lugares_ref.child(str(lugar_id)).set(lugar)
    return lugar_id


def obtener_lugares(viaje_id):
    """Obtener todos los lugares de un viaje"""
    datos = ref.child('lugares').get().val() or {}
    lugares = [l for l in datos.values() if isinstance(l, dict) and l.get('viaje_id') == viaje_id]
    lugares.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    return lugares


def eliminar_lugar(lugar_id):
    """Eliminar un lugar"""
    ref.child('lugares').child(str(lugar_id)).delete()


# ──────────────────────────────────────────────
#  AHORRO
# ──────────────────────────────────────────────

def agregar_aporte(viaje_id, monto, descripcion=None):
    """Agregar un aporte al bote de ahorro"""
    aportes_ref = ref.child('aportes_ahorro')
    datos = aportes_ref.get().val() or {}
    aporte_id = len(datos) + 1
    
    aporte = {
        'id': aporte_id,
        'viaje_id': viaje_id,
        'monto': monto,
        'descripcion': descripcion,
        'creado_en': datetime.now().isoformat()
    }
    
    aportes_ref.child(str(aporte_id)).set(aporte)
    return aporte_id


def obtener_aportes(viaje_id):
    """Obtener todos los aportes de un viaje"""
    datos = ref.child('aportes_ahorro').get().val() or {}
    aportes = [a for a in datos.values() if isinstance(a, dict) and a.get('viaje_id') == viaje_id]
    aportes.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    return aportes


def eliminar_aporte(aporte_id):
    """Eliminar un aporte"""
    ref.child('aportes_ahorro').child(str(aporte_id)).delete()


def total_ahorrado_viaje(viaje_id):
    """Calcular el total ahorrado para un viaje"""
    aportes = obtener_aportes(viaje_id)
    return sum(float(a.get('monto', 0)) for a in aportes)


# ──────────────────────────────────────────────
#  ITINERARIOS DE UN DÍA
# ──────────────────────────────────────────────

def crear_itinerario(nombre, fecha, ciudad=None, descripcion=None, emoji="📅"):
    """Crear un nuevo itinerario"""
    itinerarios_ref = ref.child('itinerarios_dia')
    datos = itinerarios_ref.get().val() or {}
    itinerario_id = len(datos) + 1
    
    itinerario = {
        'id': itinerario_id,
        'nombre': nombre,
        'fecha': fecha,
        'ciudad': ciudad,
        'descripcion': descripcion,
        'emoji': emoji,
        'creado_en': datetime.now().isoformat()
    }
    
    itinerarios_ref.child(str(itinerario_id)).set(itinerario)
    return itinerario_id


def obtener_itinerarios(orden="fecha"):
    """Obtener todos los itinerarios"""
    datos = ref.child('itinerarios_dia').get().val() or {}
    itinerarios = list(datos.values()) if isinstance(datos, dict) else []
    
    if orden == "fecha":
        itinerarios.sort(key=lambda x: x.get('fecha', ''), reverse=True)
    else:
        itinerarios.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    
    return itinerarios


def obtener_itinerario(itinerario_id):
    """Obtener un itinerario específico"""
    dato = ref.child('itinerarios_dia').child(str(itinerario_id)).get().val()
    return dato if dato else None


def actualizar_itinerario(itinerario_id, nombre, fecha, ciudad, descripcion, emoji):
    """Actualizar un itinerario"""
    itinerario = obtener_itinerario(itinerario_id)
    if not itinerario:
        return
    
    itinerario_actualizado = {
        'id': itinerario_id,
        'nombre': nombre,
        'fecha': fecha,
        'ciudad': ciudad,
        'descripcion': descripcion,
        'emoji': emoji,
        'creado_en': itinerario.get('creado_en')
    }
    
    ref.child('itinerarios_dia').child(str(itinerario_id)).set(itinerario_actualizado)


def eliminar_itinerario(itinerario_id):
    """Eliminar un itinerario y sus actividades"""
    ref.child('itinerarios_dia').child(str(itinerario_id)).delete()
    
    # Eliminar actividades asociadas
    actividades = ref.child('actividades_itinerario').get().val() or {}
    for actividad_id, actividad in actividades.items():
        if actividad.get('itinerario_id') == itinerario_id:
            ref.child('actividades_itinerario').child(actividad_id).delete()


def agregar_actividad_itinerario(itinerario_id, hora_inicio, actividad, ubicacion=None, notas=None, hora_fin=None, color="#c44569"):
    """Agregar una actividad a un itinerario"""
    actividades_ref = ref.child('actividades_itinerario')
    datos = actividades_ref.get().val() or {}
    actividad_id = len(datos) + 1
    
    actividad_obj = {
        'id': actividad_id,
        'itinerario_id': itinerario_id,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'actividad': actividad,
        'ubicacion': ubicacion,
        'notas': notas,
        'color': color,
        'creado_en': datetime.now().isoformat()
    }
    
    actividades_ref.child(str(actividad_id)).set(actividad_obj)
    return actividad_id


def obtener_actividades_itinerario(itinerario_id):
    """Obtener todas las actividades de un itinerario"""
    datos = ref.child('actividades_itinerario').get().val() or {}
    actividades = [a for a in datos.values() if isinstance(a, dict) and a.get('itinerario_id') == itinerario_id]
    actividades.sort(key=lambda x: x.get('hora_inicio', ''))
    return actividades


def actualizar_actividad_itinerario(actividad_id, hora_inicio, hora_fin, actividad, ubicacion, notas, color):
    """Actualizar una actividad de itinerario"""
    ref.child('actividades_itinerario').child(str(actividad_id)).update({
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'actividad': actividad,
        'ubicacion': ubicacion,
        'notas': notas,
        'color': color
    })


def eliminar_actividad_itinerario(actividad_id):
    """Eliminar una actividad de itinerario"""
    ref.child('actividades_itinerario').child(str(actividad_id)).delete()
