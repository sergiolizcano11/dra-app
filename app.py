import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Dragon Évolution", page_icon="🐉", layout="centered")

# Ocultar menú nativo y aplicar diseño "Neo-Pop"[cite: 2]
st.markdown("""
<style>
    :root { --bg: #F4F7F6; --card-bg: #FFFFFF; --primary: #4D79FF; }
    .stApp { background-color: var(--bg); font-family: 'Segoe UI', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Tarjetas estilo Soft UI[cite: 2] */
    .solid-panel {
        background: var(--card-bg); border-radius: 24px; padding: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    
    /* Botones vibrantes[cite: 2] */
    .stButton > button {
        background: linear-gradient(90deg, #FFD93D, #FF6B6B); color: black;
        border-radius: 50px; border: none; padding: 12px; font-weight: 800; width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:active { transform: scale(0.95); }
    
    /* Animación del Dragón */
    .dragon-sprite { font-size: 100px; animation: float 3s ease-in-out infinite; }
    @keyframes float { 0% {transform: translateY(0px);} 50% {transform: translateY(-15px);} 100% {transform: translateY(0px);} }
</style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE MEMORIA (BASE DE DATOS)[cite: 1, 4] ---
FILE_DRAGONS = 'dragones_memoria.csv'

def init_db():
    # Creamos el archivo si no existe para no perder la memoria[cite: 4]
    if not os.path.exists(FILE_DRAGONS):
        pd.DataFrame(columns=['Propietario', 'NombreDragon', 'Elemento', 'XP']).to_csv(FILE_DRAGONS, index=False)

def load_data(): return pd.read_csv(FILE_DRAGONS)
def save_data(df): df.to_csv(FILE_DRAGONS, index=False)

init_db()
df_dragones = load_data()

# --- 3. LÓGICA DE EVOLUCIÓN (TIPO TAMAGOTCHI) ---
def get_dragon_form(elemento, xp):
    """Calcula la forma del dragón según la experiencia."""
    # Fases de experiencia
    if xp < 100: fase = "Huevo"
    elif xp < 300: fase = "Bebé"
    else: fase = "Adulto"
    
    # Sprites (Emojis) según elemento y fase
    sprites = {
        "Fuego 🔥": {"Huevo": "🥚🔥", "Bebé": "🦎🔥", "Adulto": "🐲🔥"},
        "Agua 💧": {"Huevo": "🥚💧", "Bebé": "🦎💧", "Adulto": "🐲💧"},
        "Planta 🌿": {"Huevo": "🥚🌿", "Bebé": "🦎🌿", "Adulto": "🐲🌿"}
    }
    
    return fase, sprites[elemento][fase]

# --- 4. RUTAS Y ESTADO DE SESIÓN ---
if 'user' not in st.session_state: st.session_state['user'] = None
if 'view' not in st.session_state: st.session_state['view'] = 'login'

def nav(vista):
    st.session_state['view'] = vista
    st.rerun()

# ==========================================
#              INTERFAZ DE LA APP
# ==========================================

# VISTA 1: LOGIN / IDENTIFICACIÓN
if st.session_state['view'] == 'login':
    st.markdown("<h1 style='text-align:center;'>🐉 Dragon App</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
        usuario = st.text_input("Tu nombre de estudiante:", placeholder="Ej: Alex")
        if st.button("Entrar"):
            if usuario:
                st.session_state['user'] = usuario
                # Comprobar si el usuario ya tiene un dragón guardado
                if usuario in df_dragones['Propietario'].values:
                    nav('tamagotchi')
                else:
                    nav('onboarding')
            else:
                st.error("Introduce tu nombre para continuar.")
        st.markdown("</div>", unsafe_allow_html=True)

# VISTA 2: ONBOARDING (SOLO ELEGIR NOMBRE Y ELEMENTO)
elif st.session_state['view'] == 'onboarding':
    st.markdown("<h1 style='text-align:center;'>✨ La Incubadora</h1>", unsafe_allow_html=True)
    
    with st.form("crear_dragon"):
        st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
        st.markdown("### 1. Bautiza a tu dragón")
        nombre_dragon = st.text_input("Nombre:", placeholder="Ej: Ignis, Aqua...")
        
        st.markdown("### 2. Elige su elemento")
        elemento = st.radio("Elemento:", ["Fuego 🔥", "Agua 💧", "Planta 🌿"], horizontal=True)
        
        if st.form_submit_button("¡Adoptar Huevo!"):
            if nombre_dragon:
                # Guardamos el nuevo dragón en la base de datos (Nivel inicial 0 XP)
                nuevo_dragon = pd.DataFrame([[st.session_state['user'], nombre_dragon, elemento, 0]], 
                                          columns=['Propietario', 'NombreDragon', 'Elemento', 'XP'])
                df_dragones = pd.concat([df_dragones, nuevo_dragon], ignore_index=True)
                save_data(df_dragones) # Guardamos para no perder la memoria[cite: 4]
                nav('tamagotchi')
            else:
                st.error("Tu dragón necesita un nombre.")
        st.markdown("</div>", unsafe_allow_html=True)

# VISTA 3: EL TAMAGOTCHI (EVOLUCIÓN)
elif st.session_state['view'] == 'tamagotchi':
    # Recuperar los datos del dragón del usuario actual
    mi_dragon = df_dragones[df_dragones['Propietario'] == st.session_state['user']].iloc[0]
    xp_actual = mi_dragon['XP']
    
    # Calcular fase y sprite actual
    fase, sprite = get_dragon_form(mi_dragon['Elemento'], xp_actual)
    
    # UI del Tamagotchi
    st.markdown(f"<h1 style='text-align:center; color:#4D79FF;'>{mi_dragon['NombreDragon']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-weight:bold;'>Fase: {fase} | Elemento: {mi_dragon['Elemento']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='solid-panel'><div class='dragon-sprite'>{sprite}</div></div>", unsafe_allow_html=True)
    
    # Barra de Progreso XP
    st.progress(min(xp_actual / 300, 1.0))
    st.caption(f"<div style='text-align:center;'>{xp_actual} XP acumulada</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Botón simulado para ganar experiencia (Esto será reemplazado por los ejercicios de francés)
    if st.button("📚 Completar misión de Francés (+50 XP)"):
        # Actualizar base de datos
        idx = df_dragones.index[df_dragones['Propietario'] == st.session_state['user']].tolist()[0]
        df_dragones.at[idx, 'XP'] += 50
        save_data(df_dragones)
        st.toast("¡Tu dragón ha ganado experiencia!", icon="✨")
        st.rerun()
    
    if st.button("Salir"):
        st.session_state['user'] = None
        nav('login')
