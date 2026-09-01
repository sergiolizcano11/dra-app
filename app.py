import streamlit as st
from data.database import init_firebase
from core.state_manager import load_user_session, sync_to_cloud
from ui.styles import apply_styles
from ui.components import render_dock

st.set_page_config(page_title="Mon Cycle Français", layout="centered", page_icon="🐉")

# 1. Conectar a la base de datos
db = init_firebase()

# 2. Pantalla de Acceso (Login)
if 'user' not in st.session_state:
    st.title("Connexion 🗝️")
    st.write("Introduce tu código de estudiante para ver a tu dragón.")
    
    user_id_input = st.text_input("Código de Alumno", placeholder="Ej: ALUMNO_01")
    if st.button("Entrar"):
        if user_id_input.strip() != "":
            load_user_session(db, user_id_input.strip())
            st.rerun()
    st.stop() # Detiene la ejecución hasta que inicie sesión

# 3. Flujo normal de la app (Onboarding o Home)
# Aquí va el resto de tu código de app.py...
# Recuerda llamar a `sync_to_cloud(db)` cada vez que sumes XP en checkin.py o arcade.py
