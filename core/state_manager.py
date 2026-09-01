import streamlit as st
from data.database import get_user_data, save_user_data

def load_user_session(db, user_id):
    """Carga los datos de Firebase al iniciar sesión."""
    cloud_data = get_user_data(db, user_id)
    
    if cloud_data:
        st.session_state.user = cloud_data
    else:
        # Valores por defecto para un nuevo alumno
        st.session_state.user = {
            'id': user_id,
            'setup_complete': False,
            'nombre': 'Apprenti',
            'elemento': 'Fuego',
            'nivel': 1,
            'xp': 0,
            'xp_next': 50,
            'fase_actual': 'Éveil',
            'view': 'Home'
        }
        sync_to_cloud(db) # Guardamos el perfil inicial

def sync_to_cloud(db):
    """Función para llamar cada vez que el alumno gana XP o cambia de fase."""
    if 'user' in st.session_state and 'id' in st.session_state.user:
        save_user_data(db, st.session_state.user['id'], st.session_state.user)
