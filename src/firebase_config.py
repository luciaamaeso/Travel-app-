import os
import json
import glob
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# Cargar las credenciales desde la variable de entorno o archivo local
def _encontrar_archivo_credenciales():
    """Busca el archivo de credenciales Firebase en la carpeta raíz del proyecto"""
    # Obtener la carpeta raíz (padre de src/)
    carpeta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Patrones de nombres posibles
    patrones = [
        os.path.join(carpeta_raiz, 'serviceAccountKey.json'),
        os.path.join(carpeta_raiz, '*-firebase-adminsdk-*.json'),
        'serviceAccountKey.json',  # Por si acaso se ejecuta desde otra carpeta
        '*-firebase-adminsdk-*.json'
    ]
    
    for patron in patrones:
        archivos = glob.glob(patron)
        if archivos:
            return archivos[0]
    return None

def inicializar_firebase():
    """Inicializa Firebase con las credenciales"""
    print("\n" + "="*60)
    print("[Firebase] INICIALIZANDO FIREBASE")
    print("="*60)
    
    # Intenta cargar desde variable de entorno (para producción)
    firebase_json = os.environ.get('FIREBASE_CONFIG')
    
    if firebase_json:
        # Estamos en producción (Streamlit Cloud, etc)
        print("[Firebase] Detectado FIREBASE_CONFIG en variable de entorno")
        try:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            print("[Firebase] ✓ Credenciales cargadas desde variable de entorno")
        except Exception as e:
            print(f"[Firebase] ✗ Error al cargar FIREBASE_CONFIG: {e}")
            return None
    else:
        # Estamos en local - buscar archivo de credenciales
        print("[Firebase] Buscando archivo de credenciales local...")
        archivo_cred = _encontrar_archivo_credenciales()
        
        if not archivo_cred:
            print("[Firebase] ✗ NO SE ENCONTRÓ ARCHIVO DE CREDENCIALES")
            print("[Firebase] Buscando en:")
            print(f"  - {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/serviceAccountKey.json")
            print(f"  - {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/*-firebase-adminsdk-*.json")
            print(f"  - ./serviceAccountKey.json (desde carpeta actual)")
            print("[Firebase] Solución: Copia serviceAccountKey.json a la RAÍZ del proyecto")
            return None
        
        print(f"[Firebase] ✓ Archivo encontrado: {archivo_cred}")
        
        try:
            cred = credentials.Certificate(archivo_cred)
            print("[Firebase] ✓ Credenciales parseadas correctamente")
        except json.JSONDecodeError as e:
            print(f"[Firebase] ✗ Archivo JSON inválido: {e}")
            return None
        except Exception as e:
            print(f"[Firebase] ✗ Error al leer {archivo_cred}: {e}")
            return None
    
    # Verificar que tenemos credenciales
    if cred is None:
        print("[Firebase] ✗ Error crítico: cred es None después de cargar")
        return None
    
    print("[Firebase] Iniciando conexión a Firebase...")
    print(f"[Firebase] Database URL: https://travelappformanagement-default-rtdb.europe-west1.firebasedatabase.app/")
    
    # Inicializar Firebase
    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://travelappformanagement-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("[Firebase] ✓ Firebase app inicializado")
        
        # Obtener referencia
        db_ref = db.reference()
        print("[Firebase] ✓ Referencia a base de datos obtenida")
        print("="*60)
        return db_ref
        
    except ValueError as e:
        # Ya está inicializado
        if "already exists" in str(e):
            print("[Firebase] ✓ Firebase ya estaba inicializado (reutilizando)")
            try:
                db_ref = db.reference()
                print("[Firebase] ✓ Referencia a base de datos obtenida")
                print("="*60)
                return db_ref
            except Exception as ref_error:
                print(f"[Firebase] ✗ Error al obtener referencia: {ref_error}")
                return None
        else:
            print(f"[Firebase] ✗ ValueError: {e}")
            print("="*60)
            return None
    except Exception as e:
        print(f"[Firebase] ✗ Error CRÍTICO al conectar: {e}")
        print(f"[Firebase] Tipo de error: {type(e).__name__}")
        import traceback
        print(f"[Firebase] Traceback:\n{traceback.format_exc()}")
        print("="*60)
        return None

# Llamar cuando importe el módulo
ref = inicializar_firebase()

# Debug: Mostrar estado de conexión
if ref is None:
    print("\n" + "!"*60)
    print("! FIREBASE NO DISPONIBLE - LA APP NO FUNCIONARÁ")
    print("!"*60)
    print("! Próximos pasos:")
    print("! 1. Verifica que serviceAccountKey.json está en la RAÍZ")
    print("! 2. Ejecuta: bash firebase-diagnose.sh")
    print("!"*60 + "\n")
else:
    print("[Firebase] ✓✓✓ CONEXIÓN EXITOSA ✓✓✓")
    print()

