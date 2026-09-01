import streamlit as st
import random
from datetime import datetime
# Importaciones preparadas para TTS y BD (requieren instalación)
# from gtts import gTTS
# import firebase_admin
# from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN Y ESTILOS VISUALES ---
st.set_page_config(page_title="Mon Dragon", layout="centered", page_icon="🐉")

# Inyección de CSS para ocultar el menú por defecto y dar aspecto de app
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F8F9FA; font-family: 'Helvetica', sans-serif; }
    .glass-panel { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .btn-solid { background-color: #4D79FF; color: white; border-radius: 15px; padding: 10px; width: 100%; border: none; font-weight: bold; }
    .dock-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 15px; border-top: 1px solid #eee; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

# --- 2. DICCIONARIOS Y DATOS (Todo mezclado en el archivo) ---
TEXTOS = {
    "fr": {"login": "Connexion", "code": "Code d'étudiant", "enter": "Entrer", "home": "Début"},
    "es": {"login": "Conexión", "code": "Código de estudiante", "enter": "Entrar", "home": "Inicio"}
}

FASES_EVOLUCION = {
    1: {"nombre": "Œuf", "min_nivel": 1},
    2: {"nombre": "Bébé", "min_nivel": 5},
    3: {"nombre": "Adolescent", "min_nivel": 12},
    4: {"nombre": "Légendaire", "min_nivel": 30}
}

# --- 3. GESTIÓN DE ESTADO Y LÓGICA ---
if 'user' not in st.session_state:
    st.session_state.user = {'logged': False, 'id': '', 'xp': 0, 'nivel': 1, 'fase': 'Œuf', 'view': 'home', 'lang': 'fr'}

def ganar_xp(cantidad):
    st.session_state.user['xp'] += cantidad
    # Aquí iría la lógica de Firebase para guardar datos
    st.success(f"+{cantidad} XP!")

def cambiar_vista(vista):
    st.session_state.user['view'] = vista

# --- 4. RENDERIZADO DE PANTALLAS (UI) ---
lang = st.session_state.user['lang']

if not st.session_state.user['logged']:
    st.markdown("<div class='glass-panel text-center'>", unsafe_allow_html=True)
    st.title(f"🐉 {TEXTOS[lang]['login']}")
    codigo = st.text_input(TEXTOS[lang]['code'])
    if st.button(TEXTOS[lang]['enter']):
        if codigo:
            st.session_state.user['logged'] = True
            st.session_state.user['id'] = codigo
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    vista = st.session_state.user['view']
    
    if vista == 'home':
        st.markdown("<div class='glass-panel text-center'>", unsafe_allow_html=True)
        st.header(f"Niveau {st.session_state.user['nivel']}")
        st.subheader(f"Fase actual: {st.session_state.user['fase']}")
        st.progress(min(st.session_state.user['xp'] / 100, 1.0))
        st.write("Tu dragón está descansando...")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif vista == 'misiones':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.header("Misiones ODS")
        if st.button("Completar reto de reciclaje (Agua)"):
            ganar_xp(25)
        st.markdown("</div>", unsafe_allow_html=True)

    # Menú inferior falso usando columnas al final del scroll[cite: 2]
    st.write("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Inicio", use_container_width=True): cambiar_vista('home'); st.rerun()
    with col2:
        if st.button("🎮 Retos", use_container_width=True): cambiar_vista('misiones'); st.rerun()
