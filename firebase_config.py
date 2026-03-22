import os
import json
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# Cargar las credenciales desde la variable de entorno o archivo local
def inicializar_firebase():
    """Inicializa Firebase con las credenciales"""
    
    # Intenta cargar desde variable de entorno (para producción)
    firebase_json = os.environ.get('FIREBASE_CONFIG')
    
    if firebase_json:
        # Estamos en producción (Streamlit Cloud, etc)
        try:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            st.error(f"Error al cargar FIREBASE_CONFIG de variables de entorno: {e}")
            return None
    else:
        # Estamos en local
        if not os.path.exists('serviceAccountKey.json'):
            st.error("""
            ⚠️ **No se encontró serviceAccountKey.json**
            
            Pasos para arreglarlo:
            1. Ve a https://firebase.google.com
            2. Abre tu proyecto 'travel-app'
            3. Ve a ⚙️ Settings → Service Accounts
            4. Click en "Generate New Private Key"
            5. Guarda el archivo como `serviceAccountKey.json` en esta carpeta
            6. Recarga la aplicación
            """)
            return None
        
        try:
            cred = credentials.Certificate('serviceAccountKey.json')
        except Exception as e:
            st.error(f"Error al leer serviceAccountKey.json: {e}")
            return None
    
    # Inicializar Firebase
    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://travelappformanagement-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        return db.reference()
    except ValueError:
        # Ya está inicializado
        return db.reference()
    except Exception as e:
        st.error(f"Error al conectar con Firebase: {e}")
        return None

# Llamar cuando importe el módulo
ref = inicializar_firebase()

