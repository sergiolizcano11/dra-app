import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ==========================================
# BLOQUE 1: CONFIGURACIÓN VISUAL Y APP
# ==========================================
st.set_page_config(
    page_title="Dragon Évolution",
    page_icon="🐉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# BLOQUE 2: CSS AVANZADO (DISEÑO GEN Z)
# ==========================================
# Implementación de estética Gen Z con bordes redondeados y diseño limpio[cite: 1]
st.markdown("""
<style>
    :root {
        --bg: #1a1a2e;
        --card-bg: rgba(25, 30, 45, 0.95);
        --accent: #f1c40f;
        --water: #3498db;
        --fire: #e74c3c;
        --plant: #2ecc71;
    }
    .stApp { background-color: var(--bg); color: white; font-family: 'Poppins', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* TARJETAS ESTILO GLASSMORPHISM */
    .stDataFrame, .stForm, div[data-testid="stExpander"], .css-1r6slb0 {
        background: var(--card-bg) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* BOTONES */
    .stButton > button {
        background: linear-gradient(45deg, #f1c40f, #f39c12);
        color: #000;
        border-radius: 12px;
        font-weight: 800;
        width: 100%;
        transition: 0.2s;
        border: none;
    }
    .stButton > button:active { transform: scale(0.95); }

    /* INPUTS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 12px;
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
    }
    
    h1, h2, h3 { color: var(--accent); font-weight: 800; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BLOQUE 3: BASE DE DATOS SEGURA (FIREBASE)
# ==========================================
# Sustituimos los archivos CSV[cite: 2] por Firestore para proteger los datos de accesos externos.

@st.cache_resource
def init_firebase():
    """Inicializa la conexión segura con Firebase."""
    if not firebase_admin._apps:
        # En producción (Streamlit Cloud), usa st.secrets["firebase"]
        # Aquí usamos un bloque try-except para que no colapse si aún no has puesto las claves.
        try:
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except:
            st.warning("⚠️ Firebase no está configurado en st.secrets. Usando modo de prueba temporal.")
            return None
    return firestore.client()

db = init_firebase()

def save_dragon_data(pseudo, data):
    """Guarda o actualiza los datos del dragón en la nube."""
    if db:
        db.collection('dragones').document(pseudo).set(data, merge=True)
    else:
        st.session_state['temp_db'][pseudo] = data # Fallback local

def get_dragon_data(pseudo):
    """Recupera los datos del dragón."""
    if db:
        doc = db.collection('dragones').document(pseudo).get()
        return doc.to_dict() if doc.exists else None
    return st.session_state['temp_db'].get(pseudo)

if 'temp_db' not in st.session_state:
    st.session_state['temp_db'] = {}

# ==========================================
# BLOQUE 4: LÓGICA DE EVOLUCIÓN Y CARNET
# ==========================================
EVOLUTION_STAGES = [
    {"max_xp": 100, "name": "Œuf", "emoji": "🥚"},
    {"max_xp": 300, "name": "Bébé", "emoji": "🦎"},
    {"max_xp": 600, "name": "Adolescent", "emoji": "🦖"},
    {"max_xp": 1000, "name": "Adulte", "emoji": "🐲"},
    {"max_xp": 99999, "name": "Légendaire", "emoji": "🐉"}
]

def get_evolution_stage(xp):
    for stage in EVOLUTION_STAGES:
        if xp < stage["max_xp"]:
            return stage
    return EVOLUTION_STAGES[-1]

# Reutilizamos tu generador de carnet modificándolo para el Dragón[cite: 2]
def create_badge(pseudo, element, stage):
    W, H = 400, 600
    img = Image.new('RGB', (W, H), color='#1a1a2e')
    d = ImageDraw.Draw(img)
    
    # Colores por elemento
    colors = {"Eau": "#3498db", "Feu": "#e74c3c", "Plante": "#2ecc71"}
    bg_color = colors.get(element, "#f1c40f")
    
    d.rectangle([(0, 0), (W, 150)], fill=bg_color)
    try: font = ImageFont.truetype("arial.ttf", 40)
    except: font = ImageFont.load_default()
    
    d.text((20, 50), "DRESSEUR ODD", fill="white", font=font)
    d.text((150, 200), stage['emoji'], fill="white", font=font)
    d.text((50, 300), pseudo, fill="white", font=font)
    
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(f"Dragon:{pseudo}|Element:{element}")
    qr.make(fit=True)
    img.paste(qr.make_image(fill_color="black", back_color="white"), (100, 420))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# ==========================================
# BLOQUE 5: NAVEGACIÓN Y ESTADO
# ==========================================
# Mantenemos tu lógica de enrutamiento[cite: 2]
if 'page' not in st.session_state: st.session_state['page'] = 'profile'
if 'current_user' not in st.session_state: st.session_state['current_user'] = None

def nav(page_name):
    st.session_state['page'] = page_name
    st.rerun()

def add_xp(amount):
    if st.session_state['current_user']:
        data = get_dragon_data(st.session_state['current_user'])
        data['xp'] += amount
        save_dragon_data(st.session_state['current_user'], data)
        st.toast(f"¡+{amount} XP ganada!", icon="✨")

# ==========================================
# BLOQUE 6: VISTAS (SCREENS)
# ==========================================

# --- PÁGINA 1: INCUBADORA (ELECCIÓN DEL DRAGÓN) ---
if st.session_state['page'] == 'profile':
    st.markdown("<h1>L'ÉCLOSERIE 🥚</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Choisis l'œuf de ton futur dragon.</p>", unsafe_allow_html=True)
    
    with st.form("dragon_creation"):
        pseudo = st.text_input("Ton Pseudo (Tu nombre de entrenador):")
        
        st.markdown("### Élément du Dragon")
        element = st.radio("Sélectionne ton type:", ["💧 Eau", "🔥 Feu", "🌿 Plante"], horizontal=True)
        
        if st.form_submit_button("Éclore l'Œuf (Empezar)"):
            if pseudo:
                elem_clean = element.split(" ")[1] # Extrae Eau, Feu o Plante
                
                # Comprobar si existe en la BD
                existing_data = get_dragon_data(pseudo)
                if not existing_data:
                    new_data = {
                        "pseudo": pseudo,
                        "element": elem_clean,
                        "xp": 0,
                        "journal": []
                    }
                    save_dragon_data(pseudo, new_data)
                
                st.session_state['current_user'] = pseudo
                nav('home')
            else:
                st.error("¡Debes introducir un nombre!")

# --- PÁGINA 2: EL DRAGÓN (DASHBOARD) ---
elif st.session_state['page'] == 'home':
    if not st.session_state['current_user']: nav('profile')
    
    user_data = get_dragon_data(st.session_state['current_user'])
    stage = get_evolution_stage(user_data['xp'])
    
    st.markdown(f"<h2>{user_data['pseudo']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><span style='background:#333; padding:5px 10px; border-radius:10px;'>Dragon d'{user_data['element']}</span></p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"<div style='font-size: 8rem; text-align: center; margin: 20px 0;'>{stage['emoji']}</div>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center; color:#ccc;'>STADE: {stage['name'].upper()}</h4>", unsafe_allow_html=True)
        
        # Barra de progreso
        pct = min(user_data['xp'] / stage['max_xp'], 1.0)
        st.progress(pct)
        st.caption(f"<div style='text-align:center;'>{user_data['xp']} / {stage['max_xp']} XP</div>", unsafe_allow_html=True)

    st.markdown("---")
    badge_img = create_badge(user_data['pseudo'], user_data['element'], stage)
    st.download_button("⬇️ Télécharger Passeport", badge_img, file_name="dragon_passport.png", mime="image/png")

# --- PÁGINA 3: MISIONES (CÓDIGOS Y NORMALES) ---
elif st.session_state['page'] == 'missions':
    st.markdown("<h1>L'ARÈNE ⚔️</h1>", unsafe_allow_html=True)
    
    # Misiones por Código (Mundo Real)[cite: 1]
    with st.expander("🔑 Missions Secrètes (Codes)", expanded=True):
        st.write("Introduit le code donné par le professeur.")
        secret_code = st.text_input("Code Secret:", key="code_input").upper()
        if st.button("Valider le Code"):
            # Códigos predefinidos[cite: 1]
            valid_codes = {"ODD-74A": 100, "RELAIS-100": 100, "BIOS-50": 50}
            if secret_code in valid_codes:
                add_xp(valid_codes[secret_code])
                st.success("Code Validé !")
            else:
                st.error("Code Incorrect.")

    # Misiones Normales (Entrenamiento)
    with st.expander("🧠 Entraînement Quotidien"):
        q1 = st.radio("Traduis 'Medio Ambiente':", ["La Nature", "L'Environnement", "Le Climat"], index=None)
        if st.button("Vérifier (Vocabulaire)"):
            if q1 == "L'Environnement":
                st.success("Correct!")
                add_xp(20)
            else:
                st.error("Faux.")

# --- PÁGINA 4: EL DIARIO (FORTALEZAS Y DEBILIDADES) ---
elif st.session_state['page'] == 'journal':
    st.markdown("<h1>LE GRIMOIRE 📖</h1>", unsafe_allow_html=True)
    st.info("Note ici tes forces et tes faiblesses pour faire grandir ton dragon mentalement.")
    
    with st.form("journal_entry"):
        st.markdown("### Mon Évaluation")
        forces = st.text_area("🌟 Tes points forts aujourd'hui (Puntos fuertes):", placeholder="Ex: J'ai bien compris le vocabulaire...")
        faiblesses = st.text_area("🐢 Ce que tu dois améliorer (Puntos flojos):", placeholder="Ex: Je dois réviser les verbes...")
        
        if st.form_submit_button("Sauvegarder (+30 XP)"):
            if forces and faiblesses:
                data = get_dragon_data(st.session_state['current_user'])
                # Guardamos la entrada en la base de datos
                data['journal'].append({"forces": forces, "faiblesses": faiblesses})
                data['xp'] += 30
                save_dragon_data(st.session_state['current_user'], data)
                st.success("Journal mis à jour !")
                st.balloons()
            else:
                st.error("Remplis les deux champs.")

# ==========================================
# BLOQUE 7: MENÚ INFERIOR (DOCK)
# ==========================================
st.write("<br><br><br>", unsafe_allow_html=True) # Espacio inferior
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)

# Mantenemos tu sistema de navegación por botones[cite: 2]
with c1:
    if st.button("🐉\nDragon"): nav('home')
with c2:
    if st.button("⚔️\nMissions"): nav('missions')
with c3:
    if st.button("📖\nJournal"): nav('journal')
with c4:
    if st.button("⚙️\nProfil"): nav('profile')
