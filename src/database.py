import sqlite3
from datetime import datetime

DB_NAME = "viajes.db"


def conectar():
    """Crea conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Devuelve filas como diccionarios
    return conn


def inicializar_db():
    """Crea las tablas si no existen."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viajes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT NOT NULL,
            destino     TEXT NOT NULL,
            pais        TEXT,
            estado      TEXT DEFAULT 'idea',
            fecha_inicio TEXT,
            fecha_fin    TEXT,
            presupuesto  REAL DEFAULT 0,
            descripcion  TEXT,
            emoji        TEXT DEFAULT '🗺️',
            creado_en    TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            viaje_id   INTEGER NOT NULL,
            categoria  TEXT DEFAULT 'general',
            contenido  TEXT NOT NULL,
            creado_en  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lugares (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            viaje_id    INTEGER NOT NULL,
            nombre      TEXT NOT NULL,
            ubicacion   TEXT,
            descripcion TEXT,
            creado_en   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aportes_ahorro (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            viaje_id    INTEGER NOT NULL,
            monto       REAL NOT NULL,
            descripcion TEXT,
            creado_en   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planes_dia (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            viaje_id    INTEGER NOT NULL,
            fecha       TEXT NOT NULL,
            creado_en   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (viaje_id) REFERENCES viajes(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_dia_id INTEGER NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin    TEXT,
            actividad   TEXT NOT NULL,
            ubicacion   TEXT,
            notas       TEXT,
            orden       INTEGER DEFAULT 0,
            creado_en   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (plan_dia_id) REFERENCES planes_dia(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itinerarios_dia (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT NOT NULL,
            fecha           TEXT NOT NULL,
            ciudad          TEXT,
            descripcion     TEXT,
            emoji           TEXT DEFAULT '📅',
            creado_en       TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actividades_itinerario (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            itinerario_id   INTEGER NOT NULL,
            hora_inicio     TEXT NOT NULL,
            hora_fin        TEXT,
            actividad       TEXT NOT NULL,
            ubicacion       TEXT,
            notas           TEXT,
            color           TEXT DEFAULT '#c44569',
            orden           INTEGER DEFAULT 0,
            creado_en       TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (itinerario_id) REFERENCES itinerarios_dia(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
#  VIAJES
# ──────────────────────────────────────────────

def crear_viaje(nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji):
    conn = conectar()
    conn.execute("""
        INSERT INTO viajes (nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji))
    conn.commit()
    conn.close()


def obtener_viajes(filtro_estado=None, busqueda=None):
    conn = conectar()
    query = "SELECT * FROM viajes"
    params = []
    condiciones = []

    if filtro_estado and filtro_estado != "todos":
        condiciones.append("estado = ?")
        params.append(filtro_estado)

    if busqueda:
        condiciones.append("(nombre LIKE ? OR destino LIKE ? OR pais LIKE ?)")
        like = f"%{busqueda}%"
        params.extend([like, like, like])

    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    query += " ORDER BY creado_en DESC"
    viajes = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(v) for v in viajes]


def obtener_viaje(viaje_id):
    conn = conectar()
    viaje = conn.execute("SELECT * FROM viajes WHERE id = ?", (viaje_id,)).fetchone()
    conn.close()
    return dict(viaje) if viaje else None


def actualizar_viaje(viaje_id, nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji):
    conn = conectar()
    conn.execute("""
        UPDATE viajes
        SET nombre=?, destino=?, pais=?, estado=?, fecha_inicio=?, fecha_fin=?, presupuesto=?, descripcion=?, emoji=?
        WHERE id=?
    """, (nombre, destino, pais, estado, fecha_inicio, fecha_fin, presupuesto, descripcion, emoji, viaje_id))
    conn.commit()
    conn.close()


def eliminar_viaje(viaje_id):
    conn = conectar()
    conn.execute("DELETE FROM viajes WHERE id = ?", (viaje_id,))
    conn.commit()
    conn.close()


def estadisticas():
    conn = conectar()
    stats = {}
    stats["total"] = conn.execute("SELECT COUNT(*) FROM viajes").fetchone()[0]
    stats["ideas"] = conn.execute("SELECT COUNT(*) FROM viajes WHERE estado='idea'").fetchone()[0]
    stats["planificados"] = conn.execute("SELECT COUNT(*) FROM viajes WHERE estado='planificado'").fetchone()[0]
    stats["proximos"] = conn.execute("SELECT COUNT(*) FROM viajes WHERE estado='próximo'").fetchone()[0]
    stats["completados"] = conn.execute("SELECT COUNT(*) FROM viajes WHERE estado='completado'").fetchone()[0]
    stats["presupuesto_total"] = conn.execute("SELECT COALESCE(SUM(presupuesto),0) FROM viajes").fetchone()[0]
    conn.close()
    return stats


# ──────────────────────────────────────────────
#  NOTAS
# ──────────────────────────────────────────────

def agregar_nota(viaje_id, categoria, contenido):
    conn = conectar()
    conn.execute(
        "INSERT INTO notas (viaje_id, categoria, contenido) VALUES (?, ?, ?)",
        (viaje_id, categoria, contenido)
    )
    conn.commit()
    conn.close()


def obtener_notas(viaje_id):
    conn = conectar()
    notas = conn.execute(
        "SELECT * FROM notas WHERE viaje_id = ? ORDER BY creado_en DESC",
        (viaje_id,)
    ).fetchall()
    conn.close()
    return [dict(n) for n in notas]


def eliminar_nota(nota_id):
    conn = conectar()
    conn.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
#  LUGARES A VISITAR
# ──────────────────────────────────────────────

def agregar_lugar(viaje_id, nombre, ubicacion=None, descripcion=None):
    conn = conectar()
    conn.execute(
        """
        INSERT INTO lugares (viaje_id, nombre, ubicacion, descripcion)
        VALUES (?, ?, ?, ?)
        """,
        (viaje_id, nombre, ubicacion, descripcion),
    )
    conn.commit()
    conn.close()


def obtener_lugares(viaje_id):
    conn = conectar()
    lugares = conn.execute(
        "SELECT * FROM lugares WHERE viaje_id = ? ORDER BY creado_en DESC",
        (viaje_id,),
    ).fetchall()
    conn.close()
    return [dict(l) for l in lugares]


def eliminar_lugar(lugar_id):
    conn = conectar()
    conn.execute("DELETE FROM lugares WHERE id = ?", (lugar_id,))
    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
#  AHORRO
# ──────────────────────────────────────────────

def agregar_aporte(viaje_id, monto, descripcion=None):
    conn = conectar()
    conn.execute(
        """
        INSERT INTO aportes_ahorro (viaje_id, monto, descripcion)
        VALUES (?, ?, ?)
        """,
        (viaje_id, monto, descripcion),
    )
    conn.commit()
    conn.close()


def obtener_aportes(viaje_id):
    conn = conectar()
    aportes = conn.execute(
        "SELECT * FROM aportes_ahorro WHERE viaje_id = ? ORDER BY creado_en DESC",
        (viaje_id,),
    ).fetchall()
    conn.close()
    return [dict(a) for a in aportes]


def eliminar_aporte(aporte_id):
    conn = conectar()
    conn.execute("DELETE FROM aportes_ahorro WHERE id = ?", (aporte_id,))
    conn.commit()
    conn.close()


def total_ahorrado_viaje(viaje_id):
    conn = conectar()
    total = conn.execute(
        "SELECT COALESCE(SUM(monto), 0) FROM aportes_ahorro WHERE viaje_id = ?",
        (viaje_id,),
    ).fetchone()[0]
    conn.close()
    return float(total or 0)


# ──────────────────────────────────────────────
#  PLANES DE UN DÍA
# ──────────────────────────────────────────────

def crear_plan_dia(viaje_id, fecha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO planes_dia (viaje_id, fecha) VALUES (?, ?)",
        (viaje_id, fecha),
    )
    plan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return plan_id


def obtener_planes_dia(viaje_id):
    conn = conectar()
    planes = conn.execute(
        "SELECT * FROM planes_dia WHERE viaje_id = ? ORDER BY fecha DESC",
        (viaje_id,),
    ).fetchall()
    conn.close()
    return [dict(p) for p in planes]


def obtener_plan_dia(plan_id):
    conn = conectar()
    plan = conn.execute(
        "SELECT * FROM planes_dia WHERE id = ?",
        (plan_id,),
    ).fetchone()
    conn.close()
    return dict(plan) if plan else None


def eliminar_plan_dia(plan_id):
    conn = conectar()
    conn.execute("DELETE FROM planes_dia WHERE id = ?", (plan_id,))
    conn.commit()
    conn.close()


def agregar_actividad(plan_dia_id, hora_inicio, actividad, ubicacion=None, notas=None, hora_fin=None):
    conn = conectar()
    cursor = conn.cursor()
    # Obtener el mayor orden actual
    max_orden = conn.execute(
        "SELECT MAX(orden) FROM actividades WHERE plan_dia_id = ?",
        (plan_dia_id,),
    ).fetchone()[0]
    orden = (max_orden or 0) + 1
    
    cursor.execute(
        """
        INSERT INTO actividades (plan_dia_id, hora_inicio, hora_fin, actividad, ubicacion, notas, orden)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (plan_dia_id, hora_inicio, hora_fin, actividad, ubicacion, notas, orden),
    )
    conn.commit()
    conn.close()


def obtener_actividades(plan_dia_id):
    conn = conectar()
    actividades = conn.execute(
        "SELECT * FROM actividades WHERE plan_dia_id = ? ORDER BY orden ASC",
        (plan_dia_id,),
    ).fetchall()
    conn.close()
    return [dict(a) for a in actividades]


def actualizar_actividad(actividad_id, hora_inicio, hora_fin, actividad, ubicacion, notas):
    conn = conectar()
    conn.execute(
        """
        UPDATE actividades
        SET hora_inicio=?, hora_fin=?, actividad=?, ubicacion=?, notas=?
        WHERE id=?
        """,
        (hora_inicio, hora_fin, actividad, ubicacion, notas, actividad_id),
    )
    conn.commit()
    conn.close()


def eliminar_actividad(actividad_id):
    conn = conectar()
    conn.execute("DELETE FROM actividades WHERE id = ?", (actividad_id,))
    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
#  ITINERARIOS DE UN DÍA (INDEPENDIENTES)
# ──────────────────────────────────────────────

def crear_itinerario(nombre, fecha, ciudad=None, descripcion=None, emoji="📅"):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO itinerarios_dia (nombre, fecha, ciudad, descripcion, emoji)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre, fecha, ciudad, descripcion, emoji)
    )
    itinerario_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return itinerario_id


def obtener_itinerarios(orden="fecha"):
    conn = conectar()
    query = "SELECT * FROM itinerarios_dia"
    if orden == "fecha":
        query += " ORDER BY fecha DESC"
    else:
        query += " ORDER BY creado_en DESC"
    itinerarios = conn.execute(query).fetchall()
    conn.close()
    return [dict(i) for i in itinerarios]


def obtener_itinerario(itinerario_id):
    conn = conectar()
    itinerario = conn.execute(
        "SELECT * FROM itinerarios_dia WHERE id = ?",
        (itinerario_id,)
    ).fetchone()
    conn.close()
    return dict(itinerario) if itinerario else None


def actualizar_itinerario(itinerario_id, nombre, fecha, ciudad, descripcion, emoji):
    conn = conectar()
    conn.execute(
        """
        UPDATE itinerarios_dia
        SET nombre=?, fecha=?, ciudad=?, descripcion=?, emoji=?
        WHERE id=?
        """,
        (nombre, fecha, ciudad, descripcion, emoji, itinerario_id)
    )
    conn.commit()
    conn.close()


def eliminar_itinerario(itinerario_id):
    conn = conectar()
    conn.execute("DELETE FROM itinerarios_dia WHERE id = ?", (itinerario_id,))
    conn.commit()
    conn.close()


def agregar_actividad_itinerario(itinerario_id, hora_inicio, actividad, ubicacion=None, notas=None, hora_fin=None, color="#c44569"):
    conn = conectar()
    cursor = conn.cursor()
    max_orden = conn.execute(
        "SELECT MAX(orden) FROM actividades_itinerario WHERE itinerario_id = ?",
        (itinerario_id,)
    ).fetchone()[0]
    orden = (max_orden or 0) + 1
    
    cursor.execute(
        """
        INSERT INTO actividades_itinerario (itinerario_id, hora_inicio, hora_fin, actividad, ubicacion, notas, color, orden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (itinerario_id, hora_inicio, hora_fin, actividad, ubicacion, notas, color, orden)
    )
    conn.commit()
    conn.close()


def obtener_actividades_itinerario(itinerario_id):
    conn = conectar()
    actividades = conn.execute(
        "SELECT * FROM actividades_itinerario WHERE itinerario_id = ? ORDER BY orden ASC",
        (itinerario_id,)
    ).fetchall()
    conn.close()
    return [dict(a) for a in actividades]


def actualizar_actividad_itinerario(actividad_id, hora_inicio, hora_fin, actividad, ubicacion, notas, color):
    conn = conectar()
    conn.execute(
        """
        UPDATE actividades_itinerario
        SET hora_inicio=?, hora_fin=?, actividad=?, ubicacion=?, notas=?, color=?
        WHERE id=?
        """,
        (hora_inicio, hora_fin, actividad, ubicacion, notas, color, actividad_id)
    )
    conn.commit()
    conn.close()


def eliminar_actividad_itinerario(actividad_id):
    conn = conectar()
    conn.execute("DELETE FROM actividades_itinerario WHERE id = ?", (actividad_id,))
    conn.commit()
    conn.close()
