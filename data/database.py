import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def init_firebase():
    # Evita inicializar la app múltiples veces al recargar
    if not firebase_admin._apps:
        # Usamos los "secrets" de Streamlit por seguridad
        cred_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def get_user_data(db, user_id):
    """Obtiene los datos del alumno si existen."""
    doc_ref = db.collection('alumnos').document(user_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def save_user_data(db, user_id, data):
    """Guarda o actualiza el progreso en la nube."""
    db.collection('alumnos').document(user_id).set(data, merge=True)
