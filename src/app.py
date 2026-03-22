import streamlit as st
import database_firebase as db
import pandas as pd
from datetime import date, time
import math

# ──────────────────────────────────────────────
#  CONFIGURACIÓN DE LA APP
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Mi Travel App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Fondo principal */
    .stApp { background-color: #1a0e14; }

    /* Tarjeta de viaje */
    .trip-card {
        background: linear-gradient(135deg, #3b1021, #5b1a33);
        border: 1px solid #7c2d4f;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }
    .trip-card:hover { border-color: #c44569; }

    /* Badge de estado */
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .badge-idea        { background: #5a1e33; color: #ffd7e5; }
    .badge-planificado { background: #74263f; color: #ffe3ec; }
    .badge-próximo     { background: #8e3150; color: #fff0f5; }
    .badge-completado  { background: #4c1730; color: #ffd0e0; }

    /* Métrica personalizada */
    .metric-box {
        background: #2b1320;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid #7c2d4f;
    }
    .metric-value { font-size: 32px; font-weight: 700; color: #f7a3bf; }
    .metric-label { font-size: 13px; color: #d8a7ba; margin-top: 4px; }

    /* Nota */
    .nota-box {
        background: #2b1320;
        border-left: 3px solid #c44569;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .nota-categoria { font-size: 11px; color: #d8a7ba; text-transform: uppercase; letter-spacing: 1px; }
    .nota-texto { color: #ffeaf2; margin-top: 4px; }
    .nota-fecha { font-size: 11px; color: #b88398; margin-top: 6px; }

    .place-box {
        background: #2b1320;
        border: 1px solid #7c2d4f;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .saving-box {
        background: #2b1320;
        border: 1px solid #7c2d4f;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }

    /* Timeline de actividades */
    .activity-timeline {
        background: #2b1320;
        border-left: 3px solid #c44569;
        border-radius: 0 10px 10px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .activity-time { font-size: 13px; font-weight: 700; color: #f7a3bf; }
    .activity-title { color: #ffeaf2; font-weight: 600; margin-top: 4px; }
    .activity-location { color: #efc8d7; font-size: 12px; margin-top: 2px; }
    .activity-notes { color: #d8a7ba; font-size: 11px; margin-top: 6px; font-style: italic; }

    /* Tarjeta de itinerario */
    .itinerario-card {
        background: linear-gradient(135deg, #1f3a3a, #2b5f5f);
        border: 1px solid #4a9595;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }
    .itinerario-card:hover { border-color: #5fc9a1; }

    /* Timeline visual de itinerario */
    .timeline-container {
        margin-top: 30px;
    }
    .timeline-hour {
        display: flex;
        margin-bottom: 20px;
    }
    .timeline-hour-label {
        font-weight: 700;
        color: #f7a3bf;
        min-width: 80px;
        padding-right: 20px;
        text-align: right;
    }
    .timeline-hour-content {
        flex: 1;
    }
    .timeline-activity {
        background: #2b1320;
        border-left: 4px solid;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .timeline-activity-title {
        font-weight: 600;
        color: #ffeaf2;
    }
    .timeline-activity-location {
        color: #efc8d7;
        font-size: 12px;
        margin-top: 4px;
    }
    .timeline-activity-notes {
        color: #d8a7ba;
        font-size: 11px;
        margin-top: 6px;
        font-style: italic;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #240f1a; }

    /* Títulos */
    h1, h2, h3 { color: #ffeaf2 !important; }
    p, label { color: #efc8d7 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  VALIDACIÓN DE CONEXIÓN FIREBASE
# ──────────────────────────────────────────────

# Verificar conexión ANTES de inicializar
from firebase_config import ref

if ref is None:
    print("\n" + "!"*70)
    print("! ERROR CRÍTICO: Firebase no se inicializó correctamente")
    print("!"*70)
    st.error("""
    ❌ **No hay conexión con Firebase**
    
    ### ¿Por qué sucede esto?
    
    Firebase no se pudo inicializar. Las causas más comunes son:
    1. El archivo `serviceAccountKey.json` no está en la raíz del proyecto
    2. El archivo está en la carpeta equivocada (ej. en `src/` o `docs/`)
    3. El archivo está corrupto o inválido
    4. No tienes conexión a internet
    
    ### Solución rápida:
    
    **Paso 1: Verifica dónde está el archivo**
    ```bash
    ls -la | grep serviceAccount
    ```
    
    **Debe estar aquí:**
    ```
    Travel-app-/
    ├── serviceAccountKey.json  ← AQUÍ ✓
    ├── src/
    ├── docs/
    └── ...
    ```
    
    **Si está en `src/`, muévelo:**
    ```bash
    mv src/serviceAccountKey.json ./serviceAccountKey.json
    ```
    
    **Paso 2: Recarga la app**
    - Presiona F5 en el navegador, o
    - Presiona Ctrl+C en la terminal y ejecuta: `streamlit run src/app.py`
    
    ### Diagnóstico completo:
    
    Si el archivo está en el lugar correcto pero sigue fallando:
    ```bash
    bash firebase-diagnose.sh
    ```
    
    Este script verificará todo automáticamente.
    
    ### Documentación:
    
    📖 [FIREBASE_TROUBLESHOOTING.md](../docs/FIREBASE_TROUBLESHOOTING.md)
    📖 [ERROR_NONETYPE.md](../docs/ERROR_NONETYPE.md)
    """)
    st.stop()
    # Backup - si st.stop() no funciona
    raise RuntimeError("Firebase no inicializado - la aplicación no puede continuar")

# Inicializar base de datos
db.inicializar_db()

# ──────────────────────────────────────────────
#  ESTADO DE SESIÓN
# ──────────────────────────────────────────────

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "viaje_id" not in st.session_state:
    st.session_state.viaje_id = None
if "viaje_seleccionado_id" not in st.session_state:
    st.session_state.viaje_seleccionado_id = None
if "itinerario_id" not in st.session_state:
    st.session_state.itinerario_id = None
if "itinerario_seleccionado_id" not in st.session_state:
    st.session_state.itinerario_seleccionado_id = None
if "editar" not in st.session_state:
    st.session_state.editar = False

ESTADOS = ["idea", "planificado", "próximo", "completado"]
EMOJIS_VIAJE = ["🗺️","✈️","🏖️","🏔️","🌆","🏛️","🌿","🌊","🏜️","🌸","🎒","🚂","🛳️","🏕️","🌍"]
EMOJIS_ITINERARIO = ["📅","🌅","☀️","🌤️","⛅","🌇","🌙","⭐","✨","🎯","🎪","🎭","🎬","🎤","🎸"]
CATEGORIAS_NOTA = ["general", "alojamiento", "transporte", "restaurantes", "actividades", "presupuesto", "documentos", "otros"]
COLORES_ACTIVIDAD = ["#c44569", "#f7a3bf", "#ff6b9d", "#ffc0cb", "#ff85a2", "#ffb3c1", "#5fc9a1", "#4a9595"]

BADGE = {
    "idea":        ("💡 Idea",        "badge-idea"),
    "planificado": ("📋 Planificado", "badge-planificado"),
    "próximo":     ("✈️ Próximo",     "badge-próximo"),
    "completado":  ("✅ Completado",  "badge-completado"),
}

def ir_a(pagina, viaje_id=None, itinerario_id=None):
    st.session_state.pagina = pagina
    st.session_state.viaje_id = viaje_id
    st.session_state.itinerario_id = itinerario_id
    st.session_state.editar = False
    st.rerun()

def fecha_desde_texto(valor):
    if not valor:
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None

# ──────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ✈️ Mi Travel App")
    st.markdown("---")

    seccion = st.radio(
        "Selecciona sección",
        ["🌍 Viajes", "📅 Itinerarios"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Inicializar variables por defecto
    filtro = "todos"
    busqueda = None
    busqueda_itinerario = None


    if seccion == "🌍 Viajes":
        # Cambiar automáticamente a viajes_inicio cuando se selecciona esta sección
        if st.session_state.pagina.startswith("itinerarios"):
            ir_a("viajes_inicio")
        
        if st.button("🏠 Inicio - Viajes", use_container_width=True):
            ir_a("viajes_inicio")
        if st.button("➕ Nuevo viaje", use_container_width=True):
            ir_a("viajes_nuevo")
        if st.button("📊 Estadísticas", use_container_width=True):
            ir_a("estadisticas_viajes")
        
        st.markdown("---")
        st.markdown("**Filtrar por estado**")
        filtro = st.selectbox("", ["todos"] + ESTADOS, label_visibility="collapsed", key="filtro_viajes")
        busqueda = st.text_input("🔍 Buscar destino...", placeholder="ej. Tokio, París...", key="busqueda_viajes")
        
        # Mostrar ahorros del viaje seleccionado
        st.markdown("---")
        st.markdown("### 🪙 Ahorros")
        
        if st.session_state.viaje_seleccionado_id:
            viaje_info = db.obtener_viaje(st.session_state.viaje_seleccionado_id)
            if viaje_info:
                ahorrado = db.total_ahorrado_viaje(viaje_info.get("id"))
                presupuesto_objetivo = float(viaje_info.get('presupuesto', 0))
                progreso = 0.0
                if presupuesto_objetivo > 0:
                    progreso = min(ahorrado / presupuesto_objetivo, 1.0)
                
                st.metric("Ahorrado", f"{ahorrado:.0f} €", f"de {presupuesto_objetivo:.0f} €")
                if presupuesto_objetivo > 0:
                    st.progress(progreso)
                
                # Botón para resetear ahorros en el sidebar
                if st.button("🔄 Resetear ahorros", use_container_width=True, key="reset_ahorros_sidebar"):
                    db.resetear_ahorros_viaje(viaje_info.get("id"))
                    st.success("✅ Ahorros reseteados")
                    st.rerun()
        else:
            st.caption("Selecciona un viaje para ver los ahorros")
    
    else:  # Itinerarios
        # Cambiar automáticamente a itinerarios_inicio cuando se selecciona esta sección
        if st.session_state.pagina.startswith("viajes"):
            ir_a("itinerarios_inicio")
        
        if st.button("🏠 Inicio - Itinerarios", use_container_width=True):
            ir_a("itinerarios_inicio")
        if st.button("➕ Nuevo itinerario", use_container_width=True):
            ir_a("itinerarios_nuevo")
        if st.button("📊 Estadísticas", use_container_width=True):
            ir_a("estadisticas_itinerarios")
        
        st.markdown("---")
        busqueda_itinerario = st.text_input("🔍 Buscar itinerario...", placeholder="ej. Día en París...", key="busqueda_itinerario")

    st.markdown("---")
    st.caption("Tu diario de viajes personal 🌍")

# ──────────────────────────────────────────────
#  SECCIÓN VIAJES
# ──────────────────────────────────────────────

if st.session_state.pagina == "viajes_inicio":
    st.markdown("# 🌍 Mis Viajes")

    # Obtener el filtro y búsqueda del session_state o valores por defecto
    filtro = st.session_state.get("filtro_viajes", "todos")
    busqueda = st.session_state.get("busqueda_viajes", None)
    
    viajes = db.obtener_viajes(filtro_estado=filtro if filtro != "todos" else None, busqueda=busqueda if busqueda else None)

    if not viajes:
        st.markdown("---")
        st.info("No tienes viajes guardados todavía. ¡Crea tu primero en **Nuevo viaje**!")
    else:
        st.markdown(f"**{len(viajes)} viaje(s) encontrado(s)**")
        st.markdown("---")
        
        # Mostrar lista de viajes para seleccionar
        viaje_seleccionado = None
        for v in viajes:
            label, css = BADGE.get(v.get("estado"), ("", ""))
            fecha_info = ""
            if v.get("fecha_inicio"):
                fecha_info = f"📅 {v.get('fecha_inicio')}"
                if v.get("fecha_fin"):
                    fecha_info += f" → {v.get('fecha_fin')}"

            presupuesto_info = f"💶 {v.get('presupuesto', 0):.0f} €" if v.get("presupuesto") else ""
            
            # Calcular porcentaje de ahorro
            presupuesto_objetivo = float(v.get('presupuesto', 0))
            aportes = db.obtener_aportes(v.get("id"))
            ahorrado = sum(float(ap['monto']) for ap in aportes) if aportes else 0.0
            progreso_ahorro = min(ahorrado / presupuesto_objetivo, 1.0) if presupuesto_objetivo > 0 else 0.0
            
            # Badge especial si ahorro está al 100%
            badge_ahorro = ""
            if progreso_ahorro >= 1.0 and presupuesto_objetivo > 0:
                badge_ahorro = '<span class="badge badge-completado" style="background: linear-gradient(135deg, #4ade80, #22c55e); font-weight:700; margin-left:8px">✅ Listo para viajar</span>'

            # Determinar si este viaje está seleccionado
            is_selected = st.session_state.viaje_seleccionado_id == v.get('id')
            border_color = "#c44569" if is_selected else "#7c2d4f"
            background = "linear-gradient(135deg, #5b1a33, #3b1021)" if is_selected else "linear-gradient(135deg, #3b1021, #5b1a33)"

            col_select, col_info = st.columns([0.8, 10])
            
            with col_select:
                if st.button("🔘" if is_selected else "⭕", key=f"select_{v.get('id')}", help="Seleccionar/Desseleccionar"):
                    if is_selected:
                        st.session_state.viaje_seleccionado_id = None
                    else:
                        st.session_state.viaje_seleccionado_id = v.get('id')
                    st.rerun()
            
            with col_info:
                # Construir HTML sin f-strings complejos para evitar problemas con Streamlit
                pais_info = f", {v.get('pais', '')}" if v.get('pais') else ""
                destino_con_pais = f"📍 {v.get('destino', 'Destino desconocido')}{pais_info}"
                
                # Construir línea de información adicional
                info_items = []
                if fecha_info:
                    info_items.append(fecha_info)
                if presupuesto_info:
                    info_items.append(presupuesto_info)
                info_extras = "&nbsp;&nbsp;".join(info_items)
                
                # Construir HTML concatenando strings simples
                html_viaje = '<div class="trip-card" style="border-color: ' + border_color + '; background: ' + background + ';">'
                html_viaje += '<div style="display:flex; justify-content:space-between; align-items:flex-start">'
                html_viaje += '<div>'
                html_viaje += '<span style="font-size:28px">' + v.get('emoji', '✈️') + '</span>'
                html_viaje += '<span style="font-size:20px; font-weight:700; color:#e2e8f0; margin-left:8px">' + v.get('nombre', 'Sin nombre') + '</span>'
                html_viaje += badge_ahorro
                html_viaje += '</div>'
                html_viaje += '<span class="badge ' + css + '">' + label + '</span>'
                html_viaje += '</div>'
                html_viaje += '<div style="color:#8892a4; margin-top:6px">'
                html_viaje += destino_con_pais
                if info_extras:
                    html_viaje += '&nbsp;&nbsp;' + info_extras
                html_viaje += '</div>'
                if v.get('descripcion'):
                    html_viaje += '<div style="color:#a0aec0; margin-top:8px; font-size:14px">' + v.get('descripcion', '') + '</div>'
                html_viaje += '</div>'
                
                st.markdown(html_viaje, unsafe_allow_html=True)
                
                # Mostrar opciones si está seleccionado
                if is_selected:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("👁️ Ver", use_container_width=True, key=f"ver_{v.get('id')}"):
                            ir_a("viajes_detalle", viaje_id=v.get("id"))
                    with col2:
                        if st.button("✏️ Editar", use_container_width=True, key=f"edit_{v.get('id')}"):
                            ir_a("viajes_editar", viaje_id=v.get("id"))
                    with col3:
                        if st.button("🗑️ Eliminar", use_container_width=True, key=f"del_{v.get('id')}"):
                            db.eliminar_viaje(v.get("id"))
                            st.session_state.viaje_seleccionado_id = None
                            st.rerun()
            
            st.write("")  # Espaciador



elif st.session_state.pagina == "viajes_nuevo":
    st.markdown("# ➕ Nuevo Viaje")
    st.markdown("---")

    # Los checkboxes FUERA del formulario para que funcionen correctamente
    st.markdown("### 📅 Fechas")
    col_fi, col_ff = st.columns(2)
    with col_fi:
        sin_fecha_ini = st.checkbox("Sin fecha de inicio", value=False, key="sin_fecha_ini_nuevo")
        if not sin_fecha_ini:
            fecha_ini = st.date_input("Fecha de inicio", value=date.today(), key="fecha_ini_nuevo")
        else:
            fecha_ini = None

    with col_ff:
        sin_fecha_fin = st.checkbox("Sin fecha de fin", value=False, key="sin_fecha_fin_nuevo")
        if not sin_fecha_fin:
            fecha_fin = st.date_input("Fecha de fin", value=date.today(), key="fecha_fin_nuevo")
        else:
            fecha_fin = None

    st.markdown("---")

    with st.form("form_nuevo_viaje"):
        col1, col2 = st.columns(2)
        with col1:
            nombre     = st.text_input("Nombre del viaje *", placeholder="ej. Aventura en Japón")
            destino    = st.text_input("Ciudad / Destino *", placeholder="ej. Tokio")
            pais       = st.text_input("País", placeholder="ej. Japón")
            estado     = st.selectbox("Estado", ESTADOS)
        with col2:
            emoji      = st.selectbox("Icono", EMOJIS_VIAJE)
            presupuesto = st.number_input("Presupuesto estimado (€)", min_value=0.0, step=50.0)

        descripcion = st.text_area("Descripción / ideas iniciales", placeholder="Escribe lo que tengas en mente...")

        enviado = st.form_submit_button("💾 Guardar viaje", use_container_width=True)
        if enviado:
            if not nombre or not destino:
                st.error("El nombre y el destino son obligatorios.")
            else:
                viaje_id = db.crear_viaje(
                    nombre, destino, pais, estado,
                    str(fecha_ini) if fecha_ini else None,
                    str(fecha_fin) if fecha_fin else None,
                    presupuesto, descripcion, emoji
                )
                
                # Crear itinerarios automáticos si ambas fechas están definidas
                if viaje_id and fecha_ini and fecha_fin:
                    db.crear_itinerarios_del_viaje(viaje_id, fecha_ini, fecha_fin, nombre, emoji)
                
                st.success("✅ ¡Viaje guardado!")
                ir_a("viajes_inicio")
elif st.session_state.pagina == "viajes_editar":
    # Verificar que tenemos un viaje_id válido
    if not st.session_state.viaje_id:
        st.error("Error: No se especificó un viaje.")
        if st.button("← Volver a Viajes"):
            ir_a("viajes_inicio")
        st.stop()
    
    viaje = db.obtener_viaje(st.session_state.viaje_id)
    if not viaje:
        st.error(f"Viaje no encontrado (ID: {st.session_state.viaje_id}).")
        if st.button("← Volver a Viajes"):
            st.session_state.viaje_id = None
            ir_a("viajes_inicio")
        st.stop()
    else:
        st.markdown("# ✏️ Editar Viaje")
        st.markdown("---")

        if st.button("← Volver"):
            ir_a("viajes_inicio")

        fecha_inicio_actual = fecha_desde_texto(viaje.get("fecha_inicio"))
        fecha_fin_actual = fecha_desde_texto(viaje.get("fecha_fin"))

        # Los checkboxes FUERA del formulario para que funcionen correctamente
        st.markdown("### 📅 Fechas")
        col_fi, col_ff = st.columns(2)
        with col_fi:
            sin_fecha_i_e = st.checkbox("Sin fecha de inicio", value=fecha_inicio_actual is None, key="edit_sin_fecha_ini")
            if not sin_fecha_i_e:
                fecha_i_e = st.date_input("Fecha inicio", value=fecha_inicio_actual or date.today(), key="edit_fecha_ini")
            else:
                fecha_i_e = None

        with col_ff:
            sin_fecha_f_e = st.checkbox("Sin fecha de fin", value=fecha_fin_actual is None, key="edit_sin_fecha_fin")
            if not sin_fecha_f_e:
                fecha_f_e = st.date_input("Fecha fin", value=fecha_fin_actual or date.today(), key="edit_fecha_fin")
            else:
                fecha_f_e = None

        st.markdown("---")

        with st.form("form_editar_viaje"):
            col1, col2 = st.columns(2)
            with col1:
                nombre_e  = st.text_input("Nombre", value=viaje.get("nombre"))
                destino_e = st.text_input("Destino", value=viaje.get("destino"))
                pais_e    = st.text_input("País", value=viaje.get("pais") or "")
                estado_e  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index(viaje.get("estado")) if viaje.get("estado") in ESTADOS else 0)
            with col2:
                emoji_e   = st.selectbox("Icono", EMOJIS_VIAJE, index=EMOJIS_VIAJE.index(viaje.get("emoji")) if viaje.get("emoji") in EMOJIS_VIAJE else 0)
                pres_e    = st.number_input("Presupuesto (€)", value=float(viaje.get("presupuesto") or 0), step=50.0)

            desc_e = st.text_area("Descripción", value=viaje.get("descripcion") or "")

            col_guardar, col_eliminar = st.columns(2)
            with col_guardar:
                if st.form_submit_button("💾 Guardar cambios", use_container_width=True):
                    db.actualizar_viaje(
                        viaje.get("id"), nombre_e, destino_e, pais_e, estado_e,
                        str(fecha_i_e) if fecha_i_e else None,
                        str(fecha_f_e) if fecha_f_e else None,
                        pres_e, desc_e, emoji_e
                    )
                    st.success("✅ Cambios guardados")
                    ir_a("viajes_inicio")
            
            with col_eliminar:
                if st.form_submit_button("🗑️ Eliminar viaje", use_container_width=True):
                    db.eliminar_viaje(viaje.get("id"))
                    st.success("✅ Viaje eliminado")
                    ir_a("viajes_inicio")

elif st.session_state.pagina == "viajes_detalle":
    # Verificar que tenemos un viaje_id válido
    if not st.session_state.viaje_id:
        st.error("Error: No se especificó un viaje.")
        if st.button("← Volver a Viajes"):
            ir_a("viajes_inicio")
        st.stop()
    
    viaje = db.obtener_viaje(st.session_state.viaje_id)
    if not viaje:
        st.error(f"Viaje no encontrado (ID: {st.session_state.viaje_id}).")
        if st.button("← Volver a Viajes"):
            st.session_state.viaje_id = None
            ir_a("viajes_inicio")
    else:
        # Cabecera
        if st.button("← Volver"):
            ir_a("viajes_inicio")

        label, css = BADGE.get(viaje.get("estado"), ("", ""))
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin:20px 0 8px">
            <span style="font-size:48px">{viaje['emoji']}</span>
            <div>
                <h1 style="margin:0">{viaje['nombre']}</h1>
                <span class="badge {css}">{label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Información principal en columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 Ubicación")
            st.markdown(f"**Destino:** {viaje.get('destino', 'No especificado')}")
            st.markdown(f"**País:** {viaje.get('pais', 'No especificado')}")
        
        with col2:
            st.markdown("### 📅 Fechas")
            st.markdown(f"**Inicio:** {viaje.get('fecha_inicio', 'Sin fecha')}")
            st.markdown(f"**Fin:** {viaje.get('fecha_fin', 'Sin fecha')}")
        
        st.markdown("---")
        
        st.markdown("### 💶 Presupuesto")
        st.markdown(f"**Estimado:** {viaje.get('presupuesto', 0):.0f} €")
        
        st.markdown("---")
        
        st.markdown("### 📝 Descripción")
        if viaje.get("descripcion"):
            st.text(viaje.get("descripcion"))
        else:
            st.info("Sin descripción")
        
        st.markdown("---")
        
        # Botones de acción
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Editar viaje", use_container_width=True):
                ir_a("viajes_editar", viaje.get("id"))
        with col2:
            if st.button("🗑️ Eliminar viaje", use_container_width=True):
                db.eliminar_viaje(viaje.get("id"))
                st.success("✅ Viaje eliminado")
                ir_a("viajes_inicio")

        st.markdown("---")

        # Notas
        st.markdown("### 📝 Notas e ideas")

        with st.expander("➕ Añadir nota", expanded=False):
            with st.form("form_nota"):
                cat  = st.selectbox("Categoría", CATEGORIAS_NOTA)
                texto = st.text_area("Escribe tu nota...", height=100)
                if st.form_submit_button("Añadir", use_container_width=True):
                    if texto.strip():
                        db.agregar_nota(viaje.get("id"), cat, texto.strip())
                        st.rerun()
                    else:
                        st.warning("La nota no puede estar vacía.")

        notas = db.obtener_notas(viaje.get("id"))
        if not notas:
            st.caption("Todavía no hay notas. ¡Añade la primera!")
        else:
            cats_con_notas = list(dict.fromkeys(n["categoria"] for n in notas))
            for cat in cats_con_notas:
                notas_cat = [n for n in notas if n["categoria"] == cat]
                st.markdown(f"**{cat.upper()}** ({len(notas_cat)})")
                for nota in notas_cat:
                    col_nota, col_del = st.columns([10, 1])
                    with col_nota:
                        st.markdown(f"""
                        <div class="nota-box">
                            <div class="nota-categoria">📌 {nota['categoria']}</div>
                            <div class="nota-texto">{nota['contenido']}</div>
                            <div class="nota-fecha">{nota['creado_en'][:16]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_del:
                        if st.button("🗑️", key=f"nota_{nota['id']}"):
                            db.eliminar_nota(nota.get("id"))
                            st.rerun()

        st.markdown("---")

        # Lugares
        st.markdown("### 📍 Sitios concretos que quieres visitar")
        with st.expander("➕ Añadir sitio", expanded=False):
            with st.form("form_lugar"):
                lugar_nombre = st.text_input("Nombre del sitio *", placeholder="ej. Torre Eiffel")
                lugar_ubicacion = st.text_input("Ubicación", placeholder="ej. París, Francia")
                lugar_desc = st.text_area("Notas", placeholder="horarios, entradas, recomendaciones...")
                if st.form_submit_button("Guardar sitio", use_container_width=True):
                    if lugar_nombre.strip():
                        db.agregar_lugar(viaje.get("id"), lugar_nombre.strip(), lugar_ubicacion.strip() or None, lugar_desc.strip() or None)
                        st.rerun()
                    else:
                        st.warning("El nombre del sitio es obligatorio.")

        lugares = db.obtener_lugares(viaje.get("id"))
        if not lugares:
            st.caption("Todavía no has añadido sitios para este viaje.")
        else:
            for lugar in lugares:
                col_lugar, col_del_lugar = st.columns([10, 1])
                with col_lugar:
                    st.markdown(f"""
                    <div class="place-box">
                        <div style="font-weight:700; color:#ffeaf2">📌 {lugar['nombre']}</div>
                        <div style="color:#efc8d7">{('📍 ' + lugar['ubicacion']) if lugar['ubicacion'] else '📍 Ubicación no especificada'}</div>
                        <div style="color:#d8a7ba; margin-top:6px">{lugar['descripcion'] if lugar['descripcion'] else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del_lugar:
                    if st.button("🗑️", key=f"lugar_{lugar['id']}"):
                        db.eliminar_lugar(lugar.get("id"))
                        st.rerun()

        st.markdown("---")

        # ── Ahorro para el viaje ──
        st.markdown("### 🪙 Bote de ahorro para el viaje")
        ahorrado = db.total_ahorrado_viaje(viaje.get("id"))
        presupuesto_objetivo = float(viaje.get("presupuesto") or 0)
        progreso = 0.0
        if presupuesto_objetivo > 0:
            progreso = min(ahorrado / presupuesto_objetivo, 1.0)

        st.markdown(f"""
        <div class="saving-box">
            <div style="color:#ffeaf2; font-weight:700; font-size:18px">Ahorrado: {ahorrado:.0f} €</div>
            <div style="color:#efc8d7">Objetivo (presupuesto): {presupuesto_objetivo:.0f} €</div>
            <div style="color:#d8a7ba">Faltan: {max(presupuesto_objetivo - ahorrado, 0):.0f} €</div>
        </div>
        """, unsafe_allow_html=True)

        if presupuesto_objetivo > 0:
            st.progress(progreso, text=f"Progreso de ahorro: {progreso*100:.1f}%")
            
            # Mostrar mensaje si se ha completado el ahorro
            if progreso >= 1.0:
                st.success("✅ ¡Listo para viajar! El ahorro se ha completado correctamente")
        else:
            st.caption("Define un presupuesto en este viaje para ver el progreso de ahorro.")

        with st.expander("➕ Añadir dinero al bote", expanded=False):
            with st.form("form_ahorro"):
                monto = st.number_input("Cantidad a añadir (€)", min_value=1.0, step=5.0)
                desc_aporte = st.text_input("Nota del aporte", placeholder="ej. ahorro del mes")
                if st.form_submit_button("Añadir al bote", use_container_width=True):
                    if monto > 0:
                        db.agregar_aporte(viaje.get("id"), float(monto), desc_aporte.strip() or None)
                        st.rerun()

        # Botón para resetear ahorros
        col_reset_1, col_reset_2 = st.columns([2, 1])
        with col_reset_2:
            if st.button("🔄 Resetear", use_container_width=True, help="Borra todos los ahorros como si los hubieras gastado en el viaje"):
                db.resetear_ahorros_viaje(viaje.get("id"))
                st.success("✅ Ahorros reseteados a cero")
                st.rerun()

        aportes = db.obtener_aportes(viaje.get("id"))
        if not aportes:
            st.caption("Todavía no hay aportes de ahorro.")
        else:
            for ap in aportes:
                col_ap, col_del_ap = st.columns([10, 1])
                with col_ap:
                    st.markdown(f"""
                    <div class="place-box">
                        <div style="font-weight:700; color:#ffeaf2">+ {ap['monto']:.0f} €</div>
                        <div style="color:#d8a7ba">{ap.get('descripcion') or 'Sin nota'}</div>
                        <div class="nota-fecha">{ap['creado_en'][:16]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del_ap:
                    if st.button("🗑️", key=f"aporte_{ap['id']}"):
                        db.eliminar_aporte(ap["id"])
                        st.rerun()

        st.markdown("---")

elif st.session_state.pagina == "estadisticas_viajes":
    st.markdown("# 📊 Estadísticas - Viajes")
    st.markdown("---")

    if st.button("← Volver"):
        ir_a("viajes_inicio")

    stats = db.estadisticas_viajes()

    col1, col2, col3, col4, col5 = st.columns(5)
    metricas = [
        (col1, stats["total"],        "Total viajes",  "🌍"),
        (col2, stats["ideas"],        "Ideas",         "💡"),
        (col3, stats["planificados"], "Planificados",  "📋"),
        (col4, stats["proximos"],     "Próximos",      "✈️"),
        (col5, stats["completados"],  "Completados",   "✅"),
    ]
    for col, valor, label, icono in metricas:
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div style="font-size:24px">{icono}</div>
                <div class="metric-value">{valor}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"\n\n💶 **Presupuesto total estimado:** `{stats['presupuesto_total']:.0f} €`")

    st.markdown("---")
    st.markdown("### 📋 Todos los viajes")
    todos = db.obtener_viajes()
    if todos:
        # Crear lista con solo las columnas disponibles
        columnas_disponibles = ["emoji", "nombre", "destino", "pais", "estado", "fecha_inicio", "presupuesto"]
        df = pd.DataFrame(todos)[columnas_disponibles]
        
        # Agregar fecha_fin solo si existe
        if any("fecha_fin" in v and v["fecha_fin"] for v in todos):
            df["fecha_fin"] = [v.get("fecha_fin", "") for v in todos]
            df.columns = ["", "Nombre", "Destino", "País", "Estado", "Inicio", "Presupuesto (€)", "Fin"]
            # Reordenar columnas
            df = df[["", "Nombre", "Destino", "País", "Estado", "Inicio", "Fin", "Presupuesto (€)"]]
        else:
            df.columns = ["", "Nombre", "Destino", "País", "Estado", "Inicio", "Presupuesto (€)"]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay viajes todavía.")

elif st.session_state.pagina == "estadisticas_itinerarios":
    st.markdown("# 📊 Estadísticas - Itinerarios")
    st.markdown("---")

    if st.button("← Volver"):
        ir_a("itinerarios_inicio")

    stats = db.estadisticas_itinerarios()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:24px">📅</div>
            <div class="metric-value">{stats["total"]}</div>
            <div class="metric-label">Total itinerarios</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size:24px">🎯</div>
            <div class="metric-value">{stats["total_actividades"]}</div>
            <div class="metric-label">Total actividades</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Todos los itinerarios")
    todos_itinerarios = db.obtener_itinerarios()
    if todos_itinerarios:
        # Crear DataFrame con campos disponibles
        df = pd.DataFrame(todos_itinerarios)
        # Seleccionar solo columnas que existen
        cols_disponibles = [col for col in ["emoji", "nombre", "fecha", "ciudad"] if col in df.columns]
        df = df[cols_disponibles]
        
        # Renombrar columnas
        nombres_columnas = {
            "emoji": "",
            "nombre": "Nombre",
            "fecha": "Fecha",
            "ciudad": "Ciudad"
        }
        df.columns = [nombres_columnas.get(col, col) for col in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay itinerarios todavía.")

# ──────────────────────────────────────────────
#  SECCIÓN ITINERARIOS
# ──────────────────────────────────────────────

elif st.session_state.pagina == "itinerarios_inicio":
    st.markdown("# 📅 Mis Itinerarios")

    itinerarios = db.obtener_itinerarios()
    
    # Filtrar por búsqueda si existe
    if 'busqueda_itinerario' in locals() and busqueda_itinerario:
        itinerarios = [i for i in itinerarios if busqueda_itinerario.lower() in i['nombre'].lower() or busqueda_itinerario.lower() in (i.get('ciudad') or '').lower()]

    if not itinerarios:
        st.markdown("---")
        st.info("No tienes itinerarios guardados todavía. ¡Crea tu primero en **Nuevo itinerario**!")
    else:
        st.markdown(f"**{len(itinerarios)} itinerario(s) encontrado(s)**")
        st.markdown("---")
        
        # Agrupar itinerarios por viaje
        itinerarios_por_viaje = {}
        for it in itinerarios:
            viaje_id = it.get('viaje_id')
            if viaje_id not in itinerarios_por_viaje:
                itinerarios_por_viaje[viaje_id] = []
            itinerarios_por_viaje[viaje_id].append(it)
        
        # Obtener información de los viajes
        viajes = db.obtener_viajes()
        viajes_dict = {v.get('id'): v for v in viajes}
        
        # Mostrar itinerarios agrupados por viaje
        for viaje_id, its_del_viaje in itinerarios_por_viaje.items():
            viaje_info = viajes_dict.get(viaje_id)
            if viaje_info:
                st.markdown(f"## {viaje_info.get('emoji', '✈️')} {viaje_info.get('nombre', 'Viaje sin nombre')}")
            else:
                st.markdown(f"## ✈️ Viaje #{viaje_id}")
            
            for it in its_del_viaje:
                # Determinar si este itinerario está seleccionado
                is_selected = st.session_state.itinerario_seleccionado_id == it.get('id')
                border_color = "#5fc9a1" if is_selected else "#4a9595"
                background = "linear-gradient(135deg, #2b5f5f, #1f3a3a)" if is_selected else "linear-gradient(135deg, #1f3a3a, #2b5f5f)"

                col_select, col_info = st.columns([0.8, 10])
                
                with col_select:
                    if st.button("🔘" if is_selected else "⭕", key=f"select_it_{it.get('id')}", help="Seleccionar/Desseleccionar"):
                        if is_selected:
                            st.session_state.itinerario_seleccionado_id = None
                        else:
                            st.session_state.itinerario_seleccionado_id = it.get('id')
                        st.rerun()
                
                with col_info:
                    # Construir HTML sin f-strings complejos
                    ciudad_info = f"&nbsp;&nbsp;📍 {it.get('ciudad')}" if it.get('ciudad') else ""
                    descripcion_html = f"<div style='color:#a0aec0; margin-top:8px; font-size:14px'>{it.get('descripcion', '')}</div>" if it.get('descripcion') else ""
                    
                    html_card = '<div class="itinerario-card" style="border-color: ' + border_color + '; background: ' + background + ';">'
                    html_card += '<div style="display:flex; justify-content:space-between; align-items:flex-start">'
                    html_card += '<div>'
                    html_card += '<span style="font-size:28px">' + it['emoji'] + '</span>'
                    html_card += '<span style="font-size:20px; font-weight:700; color:#e2e8f0; margin-left:8px">' + it['nombre'] + '</span>'
                    html_card += '</div>'
                    html_card += '</div>'
                    html_card += '<div style="color:#8892a4; margin-top:6px">'
                    html_card += '📅 ' + it['fecha']
                    html_card += ciudad_info
                    html_card += '</div>'
                    html_card += descripcion_html
                    html_card += '</div>'
                    
                    st.markdown(html_card, unsafe_allow_html=True)
                    
                    # Mostrar opciones si está seleccionado
                    if is_selected:
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col1:
                            if st.button("👁️ Ver", use_container_width=True, key=f"ver_it_{it.get('id')}"):
                                ir_a("itinerarios_detalle", itinerario_id=it["id"])
                        with col2:
                            if st.button("✏️ Editar", use_container_width=True, key=f"edit_it_{it.get('id')}"):
                                ir_a("itinerarios_editar", itinerario_id=it["id"])
                        with col3:
                            if st.button("🗑️ Eliminar", use_container_width=True, key=f"del_it_{it.get('id')}"):
                                db.eliminar_itinerario(it["id"])
                                st.session_state.itinerario_seleccionado_id = None
                                st.rerun()
            
            st.markdown("---")
            
            st.write("")  # Espaciador


elif st.session_state.pagina == "itinerarios_nuevo":
    st.markdown("# ➕ Nuevo Itinerario")
    st.markdown("---")

    with st.form("form_nuevo_itinerario"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del itinerario *", placeholder="ej. Día en París")
            fecha = st.date_input("Fecha *", value=date.today())
        with col2:
            emoji = st.selectbox("Emoji", EMOJIS_ITINERARIO)
            ciudad = st.text_input("Ciudad", placeholder="ej. París")
        
        descripcion = st.text_area("Descripción / tema del día", placeholder="ej. Museos y monumentos...")

        enviado = st.form_submit_button("💾 Guardar itinerario", use_container_width=True)
        if enviado:
            if not nombre:
                st.error("El nombre del itinerario es obligatorio.")
            else:
                it_id = db.crear_itinerario(
                    nombre, str(fecha), ciudad.strip() or None, 
                    descripcion.strip() or None, emoji
                )
                st.success("✅ ¡Itinerario creado!")
                ir_a("itinerarios_detalle", itinerario_id=it_id)

elif st.session_state.pagina == "itinerarios_editar":
    # Verificar que tenemos un itinerario_id válido
    if not st.session_state.itinerario_id:
        st.error("Error: No se especificó un itinerario.")
        if st.button("← Volver a Itinerarios"):
            ir_a("itinerarios_inicio")
        st.stop()
    
    itinerario = db.obtener_itinerario(st.session_state.itinerario_id)
    if not itinerario:
        st.error(f"Itinerario no encontrado (ID: {st.session_state.itinerario_id}).")
        if st.button("← Volver a Itinerarios"):
            st.session_state.itinerario_id = None
            ir_a("itinerarios_inicio")
        st.stop()
    else:
        st.markdown("# ✏️ Editar Itinerario")
        st.markdown("---")

        if st.button("← Volver"):
            ir_a("itinerarios_inicio")

        fecha_actual = fecha_desde_texto(itinerario.get("fecha"))

        with st.form("form_editar_itinerario"):
            col1, col2 = st.columns(2)
            with col1:
                nombre_e = st.text_input("Nombre", value=itinerario.get("nombre"))
                fecha_e = st.date_input("Fecha", value=fecha_actual or date.today())
            with col2:
                emoji_e = st.selectbox("Emoji", EMOJIS_ITINERARIO, index=EMOJIS_ITINERARIO.index(itinerario.get("emoji")) if itinerario.get("emoji") in EMOJIS_ITINERARIO else 0)
                ciudad_e = st.text_input("Ciudad", value=itinerario.get("ciudad") or "")
            
            desc_e = st.text_area("Descripción", value=itinerario.get("descripcion") or "")

            col_guardar, col_eliminar = st.columns(2)
            with col_guardar:
                if st.form_submit_button("💾 Guardar cambios", use_container_width=True):
                    db.actualizar_itinerario(
                        itinerario.get("id"), nombre_e, str(fecha_e), 
                        ciudad_e.strip() or None, desc_e.strip() or None, emoji_e
                    )
                    st.success("✅ Cambios guardados")
                    ir_a("itinerarios_inicio")
            
            with col_eliminar:
                if st.form_submit_button("🗑️ Eliminar itinerario", use_container_width=True):
                    db.eliminar_itinerario(itinerario.get("id"))
                    st.success("✅ Itinerario eliminado")
                    ir_a("itinerarios_inicio")

elif st.session_state.pagina == "itinerarios_detalle":
    # Verificar que tenemos un itinerario_id válido
    if not st.session_state.itinerario_id:
        st.error("Error: No se especificó un itinerario.")
        if st.button("← Volver a Itinerarios"):
            ir_a("itinerarios_inicio")
        st.stop()
    
    itinerario = db.obtener_itinerario(st.session_state.itinerario_id)
    if not itinerario:
        st.error(f"Itinerario no encontrado (ID: {st.session_state.itinerario_id}).")
        if st.button("← Volver a Itinerarios"):
            st.session_state.itinerario_id = None
            ir_a("itinerarios_inicio")
        st.stop()
    else:
        col_back, col_edit = st.columns([8, 2])
        with col_back:
            if st.button("← Volver"):
                ir_a("itinerarios_inicio")
        with col_edit:
            if st.button("✏️ Editar"):
                ir_a("itinerarios_editar", itinerario_id=st.session_state.itinerario_id)

        # Construir header del itinerario sin f-strings complejos
        ciudad_info = f" • 📍 {itinerario.get('ciudad')}" if itinerario.get('ciudad') else ""
        fecha_con_ciudad = f"📅 {itinerario['fecha']}{ciudad_info}"
        
        html_header = '<div style="display:flex; align-items:center; gap:16px; margin:20px 0 8px">'
        html_header += '<span style="font-size:48px">' + itinerario['emoji'] + '</span>'
        html_header += '<div>'
        html_header += '<h1 style="margin:0">' + itinerario['nombre'] + '</h1>'
        html_header += '<span style="color:#8892a4">' + fecha_con_ciudad + '</span>'
        html_header += '</div>'
        html_header += '</div>'
        
        st.markdown(html_header, unsafe_allow_html=True)

        if itinerario.get("descripcion"):
            st.info(itinerario.get("descripcion"))

        st.markdown("---")

        # Formulario para añadir actividades
        st.markdown("### ➕ Añadir actividad")
        with st.form(f"form_actividad_{itinerario['id']}"):
            col_h1, col_h2, col_color = st.columns(3)
            with col_h1:
                hora_inicio = st.time_input("Hora inicio *", value=time(9, 0), key=f"hi_{itinerario['id']}")
            with col_h2:
                hora_fin = st.time_input("Hora fin", value=None, key=f"hf_{itinerario['id']}")
            with col_color:
                color = st.selectbox("Color", COLORES_ACTIVIDAD, index=0, key=f"color_{itinerario['id']}")
            
            actividad = st.text_input("Actividad *", placeholder="ej. Desayuno en La Boca", key=f"act_{itinerario['id']}")
            ubicacion = st.text_input("Ubicación", placeholder="ej. La Boca, Buenos Aires", key=f"ubi_{itinerario['id']}")
            notas = st.text_area("Notas", placeholder="recomendaciones, cosas a llevar...", key=f"notas_{itinerario['id']}")
            
            if st.form_submit_button("✅ Añadir actividad", use_container_width=True):
                if actividad.strip() and hora_inicio:
                    db.agregar_actividad_itinerario(
                        itinerario.get("id"),
                        str(hora_inicio),
                        actividad.strip(),
                        ubicacion.strip() or None,
                        notas.strip() or None,
                        str(hora_fin) if hora_fin else None,
                        color
                    )
                    st.rerun()
                else:
                    st.warning("La actividad y la hora de inicio son obligatorios.")

        st.markdown("---")

        # Vista visual de las actividades por franjas horarias
        st.markdown("### 📊 Vista de tu día")
        actividades = db.obtener_actividades_itinerario(itinerario.get("id"))
        
        if not actividades:
            st.caption("No hay actividades todavía. ¡Añade la primera!")
        else:
            # Agrupar actividades por hora
            actividades_por_hora = {}
            for act in actividades:
                hora = act['hora_inicio'][:5]  # HH:MM
                if hora not in actividades_por_hora:
                    actividades_por_hora[hora] = []
                actividades_por_hora[hora].append(act)
            
            # Mostrar en orden
            horas_ordenadas = sorted(actividades_por_hora.keys())
            
            st.markdown("""<div class="timeline-container">""", unsafe_allow_html=True)
            
            for hora in horas_ordenadas:
                acts = actividades_por_hora[hora]
                st.markdown(f"""
                <div class="timeline-hour">
                    <div class="timeline-hour-label">⏰ {hora}</div>
                    <div class="timeline-hour-content">
                """, unsafe_allow_html=True)
                
                for act in acts:
                    hora_fin_str = f" → {act['hora_fin']}" if act['hora_fin'] else ""
                    
                    col_act, col_del = st.columns([10, 1])
                    with col_act:
                        st.markdown(f"""
                        <div class="timeline-activity" style="border-left-color: {act['color']} !important;">
                            <div class="timeline-activity-title">🎯 {act['actividad']}</div>
                            {f'<div class="timeline-activity-location">📍 {act["ubicacion"]}</div>' if act['ubicacion'] else ''}
                            {f'<div class="timeline-activity-notes">{act["notas"]}</div>' if act['notas'] else ''}
                            <div style="color: #b88398; font-size: 11px; margin-top: 6px;">⏱️ {act["hora_inicio"]}{hora_fin_str}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_del:
                        if st.button("🗑️", key=f"act_it_{act['id']}", help="Eliminar"):
                            db.eliminar_actividad_itinerario(act["id"])
                            st.rerun()
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""</div>""", unsafe_allow_html=True)

# Página por defecto
if st.session_state.pagina == "inicio":
    ir_a("viajes_inicio")
