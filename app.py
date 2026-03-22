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

# Inicializar base de datos
db.inicializar_db()

# ──────────────────────────────────────────────
#  ESTADO DE SESIÓN
# ──────────────────────────────────────────────

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "viaje_id" not in st.session_state:
    st.session_state.viaje_id = None
if "itinerario_id" not in st.session_state:
    st.session_state.itinerario_id = None
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
        if st.button("🏠 Inicio - Viajes", use_container_width=True):
            ir_a("viajes_inicio")
        if st.button("➕ Nuevo viaje", use_container_width=True):
            ir_a("viajes_nuevo")
        if st.button("📊 Estadísticas", use_container_width=True):
            ir_a("estadisticas")
        
        st.markdown("---")
        st.markdown("**Filtrar por estado**")
        filtro = st.selectbox("", ["todos"] + ESTADOS, label_visibility="collapsed", key="filtro_viajes")
        busqueda = st.text_input("🔍 Buscar destino...", placeholder="ej. Tokio, París...", key="busqueda_viajes")
    
    else:  # Itinerarios
        if st.button("🏠 Inicio - Itinerarios", use_container_width=True):
            ir_a("itinerarios_inicio")
        if st.button("➕ Nuevo itinerario", use_container_width=True):
            ir_a("itinerarios_nuevo")
        
        st.markdown("---")
        busqueda_itinerario = st.text_input("🔍 Buscar itinerario...", placeholder="ej. Día en París...", key="busqueda_itinerario")

    st.markdown("---")
    st.caption("Tu diario de viajes personal 🌍")

# ──────────────────────────────────────────────
#  SECCIÓN VIAJES
# ──────────────────────────────────────────────

if st.session_state.pagina == "viajes_inicio":
    st.markdown("# 🌍 Mis Viajes")


    viajes = db.obtener_viajes(filtro_estado=filtro, busqueda=busqueda if busqueda else None)

    if not viajes:
        st.markdown("---")
        st.info("No tienes viajes guardados todavía. ¡Crea tu primero en **Nuevo viaje**!")
    else:
        st.markdown(f"**{len(viajes)} viaje(s) encontrado(s)**")
        st.markdown("---")
        for v in viajes:
            label, css = BADGE.get(v["estado"], ("", ""))
            fecha_info = ""
            if v["fecha_inicio"]:
                fecha_info = f"📅 {v['fecha_inicio']}"
                if v["fecha_fin"]:
                    fecha_info += f" → {v['fecha_fin']}"

            presupuesto_info = f"💶 {v['presupuesto']:.0f} €" if v["presupuesto"] else ""

            st.markdown(f"""
            <div class="trip-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start">
                    <div>
                        <span style="font-size:28px">{v['emoji']}</span>
                        <span style="font-size:20px; font-weight:700; color:#e2e8f0; margin-left:8px">{v['nombre']}</span>
                    </div>
                    <span class="badge {css}">{label}</span>
                </div>
                <div style="color:#8892a4; margin-top:6px">
                    📍 {v['destino']}{', ' + v['pais'] if v['pais'] else ''}
                    {"&nbsp;&nbsp;" + fecha_info if fecha_info else ""}
                    {"&nbsp;&nbsp;" + presupuesto_info if presupuesto_info else ""}
                </div>
                {"<div style='color:#a0aec0; margin-top:8px; font-size:14px'>" + v['descripcion'] + "</div>" if v['descripcion'] else ""}
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("📝 Ver", key=f"ver_{v['id']}"):
                    ir_a("viajes_detalle", v["id"])
            with col2:
                if st.button("🗑️", key=f"del_{v['id']}"):
                    db.eliminar_viaje(v["id"])
                    st.rerun()

elif st.session_state.pagina == "viajes_nuevo":
    st.markdown("# ➕ Nuevo Viaje")
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
            sin_fecha_ini = st.checkbox("Sin fecha de inicio", value=True)
            fecha_ini = None
            if not sin_fecha_ini:
                fecha_ini = st.date_input("Fecha de inicio", value=date.today())

            sin_fecha_fin = st.checkbox("Sin fecha de fin", value=True)
            fecha_fin = None
            if not sin_fecha_fin:
                fecha_fin = st.date_input("Fecha de fin", value=date.today())

            presupuesto = st.number_input("Presupuesto estimado (€)", min_value=0.0, step=50.0)

        descripcion = st.text_area("Descripción / ideas iniciales", placeholder="Escribe lo que tengas en mente...")

        enviado = st.form_submit_button("💾 Guardar viaje", use_container_width=True)
        if enviado:
            if not nombre or not destino:
                st.error("El nombre y el destino son obligatorios.")
            else:
                db.crear_viaje(
                    nombre, destino, pais, estado,
                    str(fecha_ini) if fecha_ini else None,
                    str(fecha_fin) if fecha_fin else None,
                    presupuesto, descripcion, emoji
                )
                st.success("✅ ¡Viaje guardado!")
                ir_a("viajes_inicio")

elif st.session_state.pagina == "viajes_detalle":
    viaje = db.obtener_viaje(st.session_state.viaje_id)
    if not viaje:
        st.error("Viaje no encontrado.")
        ir_a("inicio")
    else:
        # Cabecera
        col_back, col_edit = st.columns([8, 2])
        with col_back:
            if st.button("← Volver"):
                ir_a("inicio")
        with col_edit:
            if st.button("✏️ Editar viaje"):
                st.session_state.editar = not st.session_state.editar

        label, css = BADGE.get(viaje["estado"], ("", ""))
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin:20px 0 8px">
            <span style="font-size:48px">{viaje['emoji']}</span>
            <div>
                <h1 style="margin:0">{viaje['nombre']}</h1>
                <span class="badge {css}">{label}</span>
                &nbsp;<span style="color:#8892a4">📍 {viaje['destino']}{', '+viaje['pais'] if viaje['pais'] else ''}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if viaje["descripcion"]:
            st.info(viaje["descripcion"])

        col_a, col_b = st.columns(2)
        with col_a:
            if viaje["fecha_inicio"]:
                st.markdown(f"📅 **Inicio:** {viaje['fecha_inicio']}")
            if viaje["fecha_fin"]:
                st.markdown(f"📅 **Fin:** {viaje['fecha_fin']}")
        with col_b:
            if viaje["presupuesto"]:
                st.markdown(f"💶 **Presupuesto:** {viaje['presupuesto']:.0f} €")

        st.markdown("---")

        # ── Formulario de edición ──
        if st.session_state.editar:
            st.markdown("### ✏️ Editar viaje")
            fecha_inicio_actual = fecha_desde_texto(viaje["fecha_inicio"])
            fecha_fin_actual = fecha_desde_texto(viaje["fecha_fin"])

            with st.form("form_editar"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre_e  = st.text_input("Nombre", value=viaje["nombre"])
                    destino_e = st.text_input("Destino", value=viaje["destino"])
                    pais_e    = st.text_input("País", value=viaje["pais"] or "")
                    estado_e  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index(viaje["estado"]) if viaje["estado"] in ESTADOS else 0)
                with col2:
                    emoji_e   = st.selectbox("Icono", EMOJIS_VIAJE, index=EMOJIS_VIAJE.index(viaje["emoji"]) if viaje["emoji"] in EMOJIS_VIAJE else 0)
                    sin_fecha_i_e = st.checkbox("Sin fecha de inicio", value=fecha_inicio_actual is None)
                    fecha_i_e = None
                    if not sin_fecha_i_e:
                        fecha_i_e = st.date_input("Fecha inicio", value=fecha_inicio_actual or date.today())

                    sin_fecha_f_e = st.checkbox("Sin fecha de fin", value=fecha_fin_actual is None)
                    fecha_f_e = None
                    if not sin_fecha_f_e:
                        fecha_f_e = st.date_input("Fecha fin", value=fecha_fin_actual or date.today())

                    pres_e    = st.number_input("Presupuesto (€)", value=float(viaje["presupuesto"] or 0), step=50.0)
                desc_e = st.text_area("Descripción", value=viaje["descripcion"] or "")

                if st.form_submit_button("💾 Guardar cambios", use_container_width=True):
                    db.actualizar_viaje(
                        viaje["id"], nombre_e, destino_e, pais_e, estado_e,
                        str(fecha_i_e) if fecha_i_e else None,
                        str(fecha_f_e) if fecha_f_e else None,
                        pres_e, desc_e, emoji_e
                    )
                    st.success("✅ Cambios guardados")
                    ir_a("viajes_detalle", viaje["id"])

        st.markdown("---")

        # Notas
        st.markdown("### 📝 Notas e ideas")

        with st.expander("➕ Añadir nota", expanded=False):
            with st.form("form_nota"):
                cat  = st.selectbox("Categoría", CATEGORIAS_NOTA)
                texto = st.text_area("Escribe tu nota...", height=100)
                if st.form_submit_button("Añadir", use_container_width=True):
                    if texto.strip():
                        db.agregar_nota(viaje["id"], cat, texto.strip())
                        st.rerun()
                    else:
                        st.warning("La nota no puede estar vacía.")

        notas = db.obtener_notas(viaje["id"])
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
                            db.eliminar_nota(nota["id"])
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
                        db.agregar_lugar(viaje["id"], lugar_nombre.strip(), lugar_ubicacion.strip() or None, lugar_desc.strip() or None)
                        st.rerun()
                    else:
                        st.warning("El nombre del sitio es obligatorio.")

        lugares = db.obtener_lugares(viaje["id"])
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
                        db.eliminar_lugar(lugar["id"])
                        st.rerun()

        st.markdown("---")

        # ── Ahorro para el viaje ──
        st.markdown("### 🪙 Bote de ahorro para el viaje")
        ahorrado = db.total_ahorrado_viaje(viaje["id"])
        presupuesto_objetivo = float(viaje["presupuesto"] or 0)
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
        else:
            st.caption("Define un presupuesto en este viaje para ver el progreso de ahorro.")

        with st.expander("➕ Añadir dinero al bote", expanded=False):
            with st.form("form_ahorro"):
                monto = st.number_input("Cantidad a añadir (€)", min_value=1.0, step=5.0)
                desc_aporte = st.text_input("Nota del aporte", placeholder="ej. ahorro del mes")
                if st.form_submit_button("Añadir al bote", use_container_width=True):
                    if monto > 0:
                        db.agregar_aporte(viaje["id"], float(monto), desc_aporte.strip() or None)
                        st.rerun()

        aportes = db.obtener_aportes(viaje["id"])
        if not aportes:
            st.caption("Todavía no hay aportes de ahorro.")
        else:
            for ap in aportes:
                col_ap, col_del_ap = st.columns([10, 1])
                with col_ap:
                    st.markdown(f"""
                    <div class="place-box">
                        <div style="font-weight:700; color:#ffeaf2">+ {ap['monto']:.0f} €</div>
                        <div style="color:#d8a7ba">{ap['descripcion'] if ap['descripcion'] else 'Sin nota'}</div>
                        <div class="nota-fecha">{ap['creado_en'][:16]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del_ap:
                    if st.button("🗑️", key=f"aporte_{ap['id']}"):
                        db.eliminar_aporte(ap["id"])
                        st.rerun()

        st.markdown("---")

elif st.session_state.pagina == "estadisticas":
    st.markdown("# 📊 Estadísticas")
    st.markdown("---")

    if st.button("← Volver"):
        ir_a("viajes_inicio")

    stats = db.estadisticas()

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
        df = pd.DataFrame(todos)[["emoji", "nombre", "destino", "pais", "estado", "fecha_inicio", "fecha_fin", "presupuesto"]]
        df.columns = ["", "Nombre", "Destino", "País", "Estado", "Inicio", "Fin", "Presupuesto (€)"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay viajes todavía.")

# ──────────────────────────────────────────────
#  SECCIÓN ITINERARIOS
# ──────────────────────────────────────────────

elif st.session_state.pagina == "itinerarios_inicio":
    st.markdown("# 📅 Mis Itinerarios")

    itinerarios = db.obtener_itinerarios()
    
    # Filtrar por búsqueda si existe
    if 'busqueda_itinerario' in locals() and busqueda_itinerario:
        itinerarios = [i for i in itinerarios if busqueda_itinerario.lower() in i['nombre'].lower() or busqueda_itinerario.lower() in (i['ciudad'] or '').lower()]

    if not itinerarios:
        st.markdown("---")
        st.info("No tienes itinerarios guardados todavía. ¡Crea tu primero en **Nuevo itinerario**!")
    else:
        st.markdown(f"**{len(itinerarios)} itinerario(s) encontrado(s)**")
        st.markdown("---")
        for it in itinerarios:
            st.markdown(f"""
            <div class="itinerario-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start">
                    <div>
                        <span style="font-size:28px">{it['emoji']}</span>
                        <span style="font-size:20px; font-weight:700; color:#e2e8f0; margin-left:8px">{it['nombre']}</span>
                    </div>
                </div>
                <div style="color:#8892a4; margin-top:6px">
                    📅 {it['fecha']}
                    {f"&nbsp;&nbsp;📍 {it['ciudad']}" if it['ciudad'] else ""}
                </div>
                {"<div style='color:#a0aec0; margin-top:8px; font-size:14px'>" + it['descripcion'] + "</div>" if it['descripcion'] else ""}
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("👁️ Ver", key=f"ver_it_{it['id']}"):
                    ir_a("itinerarios_detalle", itinerario_id=it["id"])
            with col2:
                if st.button("🗑️", key=f"del_it_{it['id']}"):
                    db.eliminar_itinerario(it["id"])
                    st.rerun()

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

elif st.session_state.pagina == "itinerarios_detalle":
    itinerario = db.obtener_itinerario(st.session_state.itinerario_id)
    if not itinerario:
        st.error("Itinerario no encontrado.")
        ir_a("itinerarios_inicio")
    else:
        col_back, col_edit = st.columns([8, 2])
        with col_back:
            if st.button("← Volver"):
                ir_a("itinerarios_inicio")
        with col_edit:
            if st.button("✏️ Editar"):
                st.session_state.editar = not st.session_state.editar

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; margin:20px 0 8px">
            <span style="font-size:48px">{itinerario['emoji']}</span>
            <div>
                <h1 style="margin:0">{itinerario['nombre']}</h1>
                <span style="color:#8892a4">📅 {itinerario['fecha']}{f" • 📍 {itinerario['ciudad']}" if itinerario['ciudad'] else ""}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if itinerario["descripcion"]:
            st.info(itinerario["descripcion"])

        st.markdown("---")

        if st.session_state.editar:
            st.markdown("### ✏️ Editar itinerario")
            fecha_actual = fecha_desde_texto(itinerario["fecha"])

            with st.form("form_editar_it"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre_e = st.text_input("Nombre", value=itinerario["nombre"])
                    fecha_e = st.date_input("Fecha", value=fecha_actual or date.today())
                with col2:
                    emoji_e = st.selectbox("Emoji", EMOJIS_ITINERARIO, index=EMOJIS_ITINERARIO.index(itinerario["emoji"]) if itinerario["emoji"] in EMOJIS_ITINERARIO else 0)
                    ciudad_e = st.text_input("Ciudad", value=itinerario["ciudad"] or "")
                
                desc_e = st.text_area("Descripción", value=itinerario["descripcion"] or "")

                if st.form_submit_button("💾 Guardar cambios", use_container_width=True):
                    db.actualizar_itinerario(
                        itinerario["id"], nombre_e, str(fecha_e), 
                        ciudad_e.strip() or None, desc_e.strip() or None, emoji_e
                    )
                    st.success("✅ Cambios guardados")
                    ir_a("itinerarios_detalle", itinerario_id=itinerario["id"])

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
                        itinerario["id"],
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
        actividades = db.obtener_actividades_itinerario(itinerario["id"])
        
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
