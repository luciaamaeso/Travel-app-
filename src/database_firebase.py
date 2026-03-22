import firebase_admin
from firebase_admin import db
from datetime import datetime, timedelta
from firebase_config import ref
import streamlit as st

# ──────────────────────────────────────────────
#  FUNCIÓN AUXILIAR SEGURA
# ──────────────────────────────────────────────

def obtener_datos_seguro(ref_path, default=None):
    """Obtiene datos de forma segura manejando None"""
    try:
        if ref_path is None:
            return default
        resultado = ref_path.get()
        
        # Firebase puede retornar tanto DataSnapshot como list directamente
        if hasattr(resultado, 'val'):
            # Es un DataSnapshot normal
            valor = resultado.val()
            return valor if valor is not None else default
        elif isinstance(resultado, list):
            # Firebase retorna lista cuando hay índices numéricos
            # Filtrar None y retornar como dict o list
            cleaned = [item for item in resultado if item is not None]
            if not cleaned:
                return default
            # Si es una lista con un solo elemento, retornarlo como lista
            return cleaned
        else:
            return default
    except Exception as e:
        print(f"[Firebase] ⚠️ Error al obtener datos: {e}")
        return default


def normalizar_datos(datos):
    """Convierte datos a formato estándar (dict o list de dicts)"""
    if isinstance(datos, dict):
        return datos.values()
    elif isinstance(datos, list):
        return datos
    else:
        return []

# ──────────────────────────────────────────────
#  VALIDACIÓN DE CONEXIÓN
# ──────────────────────────────────────────────

def verificar_conexion():
    """Verifica si Firebase está disponible"""
    if ref is None:
        st.error("""
        ❌ **No hay conexión con Firebase**
        
        ### Pasos para resolver:
        
        1. Ve a [🔗 Firebase Console](https://console.firebase.google.com)
        2. Selecciona tu proyecto **'travel-app'**
        3. ⚙️ **Configuración del proyecto** → **Cuentas de servicio**
        4. Haz clic en **"Generar clave privada"**
        5. Guarda el archivo como `serviceAccountKey.json` en la **RAÍZ del proyecto**
           - Debe estar aquí: `Travel-app-/serviceAccountKey.json`
           - NO en: `Travel-app-/src/serviceAccountKey.json`
        6. Recarga la aplicación (F5)
        
        ### Diagnóstico:
        Si el problema persiste, ejecuta:
        ```bash
        bash firebase-diagnose.sh
        ```
        
        📖 Ver: [docs/FIREBASE_TROUBLESHOOTING.md](../docs/FIREBASE_TROUBLESHOOTING.md)
        """)
        st.stop()

# ──────────────────────────────────────────────
#  INICIALIZAR BD
# ──────────────────────────────────────────────

def inicializar_db():
    """Crea la estructura base en Firebase si no existe"""
    verificar_conexion()
    
    # Crear estructura base
    try:
        # Usar función auxiliar segura para verificar existencia
        if not obtener_datos_seguro(ref.child('viajes'), None):
            ref.child('viajes').set({})
        if not obtener_datos_seguro(ref.child('notas'), None):
            ref.child('notas').set({})
        if not obtener_datos_seguro(ref.child('lugares'), None):
            ref.child('lugares').set({})
        if not obtener_datos_seguro(ref.child('aportes_ahorro'), None):
            ref.child('aportes_ahorro').set({})
        if not obtener_datos_seguro(ref.child('itinerarios_dia'), None):
            ref.child('itinerarios_dia').set({})
        if not obtener_datos_seguro(ref.child('actividades_itinerario'), None):
            ref.child('actividades_itinerario').set({})
    except Exception as e:
        st.error(f"❌ Error al inicializar la BD: {e}\n\nEjecuta: `bash firebase-diagnose.sh`")



# ──────────────────────────────────────────────
#  VIAJES
# ──────────────────────────────────────────────

def crear_viaje(nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji):
    """Crear un nuevo viaje"""
    verificar_conexion()
    
    try:
        viajes_ref = ref.child('viajes')
        
        # Usar función auxiliar segura
        datos = obtener_datos_seguro(viajes_ref, {})
        
        # Obtener el siguiente ID
        viaje_id = len(datos) + 1
        
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
    
    except Exception as e:
        st.error(f"❌ Error al crear viaje: {e}")
        print(f"[Firebase] Error en crear_viaje: {e}")
        return None


def crear_itinerarios_del_viaje(viaje_id, fecha_inicio, fecha_fin, nombre_viaje, emoji_viaje):
    """Crea itinerarios automáticos para cada día del viaje (rango de fechas)"""
    verificar_conexion()
    
    try:
        # Convertir strings a date si es necesario
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        itinerarios_ref = ref.child('itinerarios_dia')
        datos = obtener_datos_seguro(itinerarios_ref, {})
        
        # Generar itinerarios para cada día
        fecha_actual = fecha_inicio
        itinerarios_creados = []
        
        while fecha_actual <= fecha_fin:
            itinerario_id = len(datos) + 1 + len(itinerarios_creados)
            
            itinerario = {
                'id': itinerario_id,
                'nombre': f"{nombre_viaje} - {fecha_actual.strftime('%d/%m/%Y')}",
                'fecha': str(fecha_actual),
                'viaje_id': viaje_id,  # Referencia al viaje padre
                'emoji': emoji_viaje,
                'descripcion': '',
                'creado_en': datetime.now().isoformat()
            }
            
            itinerarios_ref.child(str(itinerario_id)).set(itinerario)
            itinerarios_creados.append(itinerario_id)
            
            # Avanzar al siguiente día
            fecha_actual += timedelta(days=1)
        
        print(f"[Firebase] ✅ {len(itinerarios_creados)} itinerarios creados para viaje {viaje_id}")
        return itinerarios_creados
    
    except Exception as e:
        print(f"[Firebase] ⚠️ Error al crear itinerarios automáticos: {e}")
        return []


def obtener_viajes(filtro_estado=None, busqueda=None):
    """Obtener todos los viajes con filtros opcionales"""
    verificar_conexion()
    
    try:
        datos = obtener_datos_seguro(ref.child('viajes'), {})
    except Exception as e:
        st.error(f"Error al obtener viajes: {e}")
        return []
    
    # Manejar tanto dict como list (Firebase retorna list si los IDs son numéricos)
    if isinstance(datos, dict):
        viajes = list(datos.values())
    elif isinstance(datos, list):
        viajes = datos
    else:
        viajes = []
    
    # Asegurar que todos los elementos son diccionarios
    viajes = [v for v in viajes if isinstance(v, dict)]
    
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
    try:
        # Primero intentar obtener directamente por ID
        dato = obtener_datos_seguro(ref.child('viajes').child(str(viaje_id)), None)
        if dato:
            return dato
        
        # Si no encuentra, buscar en todos los viajes
        todos_viajes = obtener_viajes()
        for v in todos_viajes:
            if v.get('id') == viaje_id or str(v.get('id')) == str(viaje_id):
                return v
        
        return None
    except Exception as e:
        print(f"[Firebase] Error al obtener viaje {viaje_id}: {e}")
        return None
        return None


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
    import time
    try:
        viaje_id_str = str(viaje_id)
        
        print(f"\n[Firebase] ════════════════════════════════════════")
        print(f"[Firebase] Eliminando VIAJE {viaje_id_str} (tipo: {type(viaje_id).__name__})")
        print(f"[Firebase] ════════════════════════════════════════")
        
        # Función auxiliar para comparar IDs (convierte todo a string)
        def ids_coinciden(id_guardado, id_buscado):
            """Compara dos IDs convirtiéndolos a string"""
            resultado = str(id_guardado) == str(id_buscado)
            if not resultado:
                print(f"[Firebase] DEBUG: '{id_guardado}' (tipo {type(id_guardado).__name__}) != '{id_buscado}' (tipo {type(id_buscado).__name__})")
            return resultado
        
        ref.child('viajes').child(viaje_id_str).delete()
        print(f"[Firebase] ✓ Viaje {viaje_id_str} eliminado de la base de datos")
        
        # Pequeño delay para que Firebase procese la eliminación
        time.sleep(0.5)
        
        # Eliminar notas asociadas
        notas = obtener_datos_seguro(ref.child('notas'), {})
        if isinstance(notas, dict):
            notas_eliminadas = 0
            for nota_id, nota in notas.items():
                if isinstance(nota, dict) and ids_coinciden(nota.get('viaje_id'), viaje_id):
                    ref.child('notas').child(str(nota_id)).delete()
                    notas_eliminadas += 1
            print(f"[Firebase] Notas: {notas_eliminadas} eliminada(s)")
        
        # Eliminar lugares asociados
        lugares = obtener_datos_seguro(ref.child('lugares'), {})
        if isinstance(lugares, dict):
            lugares_eliminados = 0
            for lugar_id, lugar in lugares.items():
                if isinstance(lugar, dict) and ids_coinciden(lugar.get('viaje_id'), viaje_id):
                    ref.child('lugares').child(str(lugar_id)).delete()
                    lugares_eliminados += 1
            print(f"[Firebase] Lugares: {lugares_eliminados} eliminado(s)")
        
        # Eliminar aportes asociados
        aportes = obtener_datos_seguro(ref.child('aportes_ahorro'), {})
        if isinstance(aportes, dict):
            aportes_eliminados = 0
            for aporte_id, aporte in aportes.items():
                if isinstance(aporte, dict) and ids_coinciden(aporte.get('viaje_id'), viaje_id):
                    ref.child('aportes_ahorro').child(str(aporte_id)).delete()
                    aportes_eliminados += 1
            print(f"[Firebase] Aportes: {aportes_eliminados} eliminado(s)")
        
        # Eliminar itinerarios y sus actividades asociadas
        print(f"\n[Firebase] Procesando ITINERARIOS...")
        itinerarios_raw = obtener_datos_seguro(ref.child('itinerarios_dia'), {})
        print(f"[Firebase] DEBUG: itinerarios tipo={type(itinerarios_raw).__name__}, valor={itinerarios_raw if isinstance(itinerarios_raw, (dict, list)) and len(str(itinerarios_raw)) < 100 else '...'}")
        
        # Convertir a dict si es lista
        itinerarios = {}
        if isinstance(itinerarios_raw, dict):
            itinerarios = itinerarios_raw
        elif isinstance(itinerarios_raw, list):
            # Si es lista, convertir a dict con índice
            for idx, item in enumerate(itinerarios_raw):
                if isinstance(item, dict):
                    itinerarios[str(idx)] = item
        
        print(f"[Firebase] DEBUG: Después de conversión: {len(itinerarios)} itinerarios en dict")
        
        if itinerarios:
            print(f"[Firebase] DEBUG: Total itinerarios en DB: {len(itinerarios)}")
            print(f"[Firebase] DEBUG: Buscando itinerarios con viaje_id={viaje_id_str}")
            
            itinerarios_encontrados = []
            for itin_id, itin in itinerarios.items():
                if isinstance(itin, dict):
                    viaje_id_del_itin = itin.get('viaje_id')
                    print(f"[Firebase] DEBUG: Itinerario {itin_id} tiene viaje_id={viaje_id_del_itin} (tipo: {type(viaje_id_del_itin).__name__})")
                    
                    if ids_coinciden(viaje_id_del_itin, viaje_id):
                        itinerarios_encontrados.append((itin_id, itin))
                        print(f"[Firebase] ✓ Itinerario {itin_id} COINCIDE, será eliminado")
            
            print(f"\n[Firebase] Itinerarios encontrados: {len(itinerarios_encontrados)}")
            
            for itin_id, itin in itinerarios_encontrados:
                # Primero eliminar actividades de este itinerario
                actividades = obtener_datos_seguro(ref.child('actividades_itinerario'), {})
                if isinstance(actividades, dict):
                    actividades_eliminadas = 0
                    for act_id, act in actividades.items():
                        if isinstance(act, dict) and ids_coinciden(act.get('itinerario_id'), itin.get('id')):
                            ref.child('actividades_itinerario').child(str(act_id)).delete()
                            actividades_eliminadas += 1
                    if actividades_eliminadas > 0:
                        print(f"[Firebase] Actividades del itinerario {itin_id}: {actividades_eliminadas} eliminada(s)")
                
                # Luego eliminar el itinerario
                ref.child('itinerarios_dia').child(str(itin_id)).delete()
                print(f"[Firebase] ✓ Itinerario {itin_id} eliminado")
        
        print(f"\n[Firebase] ════════════════════════════════════════")
        print(f"[Firebase] ✅ VIAJE {viaje_id_str} ELIMINADO CORRECTAMENTE")
        print(f"[Firebase] ════════════════════════════════════════\n")
    except Exception as e:
        print(f"[Firebase] ❌ Error al eliminar viaje {viaje_id}: {e}")
        import traceback
        traceback.print_exc()


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


def estadisticas_viajes():
    """Obtener estadísticas específicas de viajes"""
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
    datos = obtener_datos_seguro(notas_ref, {})
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
    datos = obtener_datos_seguro(ref.child('notas'), {})
    notas = [n for n in normalizar_datos(datos) if isinstance(n, dict) and n.get('viaje_id') == viaje_id]
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
    datos = obtener_datos_seguro(lugares_ref, {})
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
    datos = obtener_datos_seguro(ref.child('lugares'), {})
    lugares = [l for l in normalizar_datos(datos) if isinstance(l, dict) and l.get('viaje_id') == viaje_id]
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
    datos = obtener_datos_seguro(aportes_ref, {})
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
    datos = obtener_datos_seguro(ref.child('aportes_ahorro'), {})
    aportes = [a for a in normalizar_datos(datos) if isinstance(a, dict) and a.get('viaje_id') == viaje_id]
    aportes.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    return aportes


def eliminar_aporte(aporte_id):
    """Eliminar un aporte"""
    ref.child('aportes_ahorro').child(str(aporte_id)).delete()


def resetear_ahorros_viaje(viaje_id):
    """Eliminar todos los aportes de un viaje (resetear ahorros a cero)"""
    try:
        aportes = obtener_aportes(viaje_id)
        for aporte in aportes:
            ref.child('aportes_ahorro').child(str(aporte.get('id'))).delete()
        print(f"[Firebase] ✅ Ahorros del viaje {viaje_id} reseteados ({len(aportes)} aportes eliminados)")
    except Exception as e:
        print(f"[Firebase] ❌ Error al resetear ahorros del viaje {viaje_id}: {e}")


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
    datos = obtener_datos_seguro(itinerarios_ref, {})
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
    datos = obtener_datos_seguro(ref.child('itinerarios_dia'), {})
    
    # Manejar tanto dict como list
    if isinstance(datos, dict):
        itinerarios = list(datos.values())
    elif isinstance(datos, list):
        itinerarios = datos
    else:
        itinerarios = []
    
    # Asegurar que todos son dicts
    itinerarios = [i for i in itinerarios if isinstance(i, dict)]
    
    if orden == "fecha":
        itinerarios.sort(key=lambda x: x.get('fecha', ''), reverse=True)
    else:
        itinerarios.sort(key=lambda x: x.get('creado_en', ''), reverse=True)
    
    return itinerarios


def obtener_itinerario(itinerario_id):
    """Obtener un itinerario específico"""
    try:
        # Primero intentar obtener directamente por ID
        dato = obtener_datos_seguro(ref.child('itinerarios_dia').child(str(itinerario_id)), None)
        if dato:
            return dato
        
        # Si no encuentra, buscar en todos los itinerarios
        todos_itinerarios = obtener_itinerarios()
        for it in todos_itinerarios:
            if it.get('id') == itinerario_id or str(it.get('id')) == str(itinerario_id):
                return it
        
        return None
    except Exception as e:
        print(f"[Firebase] Error al obtener itinerario {itinerario_id}: {e}")
        return None


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
    actividades = obtener_datos_seguro(ref.child('actividades_itinerario'), {})
    if isinstance(actividades, dict):
        for actividad_id, actividad in actividades.items():
            if isinstance(actividad, dict) and actividad.get('itinerario_id') == itinerario_id:
                ref.child('actividades_itinerario').child(str(actividad_id)).delete()


def agregar_actividad_itinerario(itinerario_id, hora_inicio, actividad, ubicacion=None, notas=None, hora_fin=None, color="#c44569"):
    """Agregar una actividad a un itinerario"""
    actividades_ref = ref.child('actividades_itinerario')
    datos = obtener_datos_seguro(actividades_ref, {})
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
    datos = obtener_datos_seguro(ref.child('actividades_itinerario'), {})
    actividades = [a for a in normalizar_datos(datos) if isinstance(a, dict) and a.get('itinerario_id') == itinerario_id]
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


def estadisticas_itinerarios():
    """Obtener estadísticas específicas de itinerarios"""
    itinerarios = obtener_itinerarios()
    total_actividades = 0
    
    for it in itinerarios:
        actividades = obtener_actividades_itinerario(it.get('id'))
        if actividades:
            total_actividades += len(actividades)
    
    return {
        'total': len(itinerarios),
        'total_actividades': total_actividades
    }
