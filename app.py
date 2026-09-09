import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Le Nid du Dragon",
    page_icon="🐉",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 2. CSS "FANTASÍA MEDIEVAL" ---
st.markdown("""
<style>
    /* Fuentes Épicas de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=MedievalSharp&display=swap');

    :root {
        --primary: #8B0000; /* Rojo oscuro místico */
        --accent: #D4AF37; /* Dorado antiguo */
        --text: #2c1e16; /* Marrón muy oscuro para leer bien */
        --parchment: rgba(244, 238, 224, 0.95); /* Color pergamino */
    }

    /* FONDO DE FANTASÍA (Bosque mágico/Castillo) */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'MedievalSharp', cursive;
    }
    
    /* Capa oscura sutil para resaltar el pergamino */
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4); 
        z-index: -1;
    }

    /* TARJETAS ESTILO PERGAMINO */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .solid-panel {
        background: var(--parchment);
        border-radius: 8px;
        padding: 25px;
        border: 2px solid var(--accent);
        box-shadow: inset 0 0 15px rgba(139, 69, 19, 0.2), 5px 5px 15px rgba(0,0,0,0.6);
        margin-bottom: 25px;
        color: var(--text);
    }

    /* CABECERA ÉPICA */
    .hero-header {
        background: linear-gradient(180deg, #1a1a1a 0%, #3a0000 100%);
        padding: 30px 20px;
        border-radius: 0 0 15px 15px;
        color: var(--accent);
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 3px solid var(--accent);
        box-shadow: 0 10px 20px rgba(0,0,0,0.7);
    }
    .hero-header h1 { 
        font-family: 'Cinzel', serif; 
        font-weight: 900; 
        font-size: 2.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 2px 2px 5px #000;
        margin-bottom: 5px;
    }

    /* TEXTOS */
    h1, h2, h3, h4 { color: var(--primary) !important; font-family: 'Cinzel', serif; font-weight: 900 !important; }
    p, label, .stMarkdown { color: var(--text) !important; font-size: 1.1rem; }

    /* BOTONES DE MADERA/ORO */
    .stButton > button {
        background: linear-gradient(to bottom, #8B0000, #4a0000);
        color: var(--accent);
        border-radius: 5px;
        border: 2px solid var(--accent);
        padding: 12px;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    
    .stButton > button:hover {
        background: linear-gradient(to bottom, #a30000, #5c0000);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.6);
    }
    
    .stButton > button:active {
        transform: translateY(2px);
        box-shadow: 0 1px 2px rgba(0,0,0,0.6);
    }

    /* MENÚ INFERIOR TIPO DOCK MEDIEVAL */
    .dock-nav { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background: linear-gradient(to top, #1a1a1a, transparent); 
        display: flex; justify-content: space-around; padding: 20px 0 15px 0; z-index: 1000; 
    }
    .dock-item { 
        background: var(--parchment);
        border: 2px solid var(--accent);
        border-radius: 50%;
        width: 60px; height: 60px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; cursor: pointer; transition: 0.2s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.8);
    }
    .dock-item:hover { transform: scale(1.1); background: #fff; }
    
    /* Efecto de flotación para el dragón */
    .dragon-emoji { font-size: 8rem; text-align: center; display: block; margin: 20px 0; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    
    /* Barra de XP de Cristal/Magia */
    .xp-container { background: #1a1a1a; border-radius: 10px; height: 25px; position: relative; border: 2px solid var(--accent); margin-top: 15px;}
    .xp-fill { background: linear-gradient(90deg, #4b0082, #8a2be2, #00ffff); height: 100%; width: 0%; transition: width 0.8s; border-radius: 8px;}
    .xp-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: 'Poppins', sans-serif; font-weight: bold; font-size: 0.8rem; color: white;}

    /* Ocultar interfaz nativa de Streamlit */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DATOS LOCAL ---
FILE_DRAGONS = 'dragones_db.csv'
FILE_JOURNAL = 'grimorio_db.csv'

def init_db():
    if not os.path.exists(FILE_DRAGONS):
        pd.DataFrame(columns=['Propietario', 'NombreDragon', 'Elemento', 'XP']).to_csv(FILE_DRAGONS, index=False)
    if not os.path.exists(FILE_JOURNAL):
        pd.DataFrame(columns=['Propietario', 'Date', 'Reflexion']).to_csv(FILE_JOURNAL, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_dragones = load_data(FILE_DRAGONS)
df_journal = load_data(FILE_JOURNAL)

# --- 4. LÓGICA DE EVOLUCIÓN (5 FASES) ---
EVOLUTION_STAGES = [
    {"max_xp": 100, "name": "L'Œuf (Huevo)", "emoji": "🥚"},
    {"max_xp": 300, "name": "Bébé (Bebé)", "emoji": "🦎"},
    {"max_xp": 600, "name": "Jeune (Adolescente)", "emoji": "🦖"},
    {"max_xp": 1000, "name": "Adulte (Adulto)", "emoji": "🐲"},
    {"max_xp": 99999, "name": "Légendaire", "emoji": "🐉"}
]

def get_evolution_stage(xp):
    for stage in EVOLUTION_STAGES:
        if xp < stage["max_xp"]:
            return stage
    return EVOLUTION_STAGES[-1]

# --- 5. NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state['page'] = 'login'
if 'current_user' not in st.session_state: st.session_state['current_user'] = None

def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- LOGIN / REGISTRO ---
if st.session_state['page'] == 'login':
    st.markdown("""
    <div class="hero-header">
        <h1>L'Académie des Dragons</h1>
        <p style="color:var(--accent);">Bienvenue, apprenti dresseur.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("<h3 style='text-align:center;'>Entrez votre nom</h3>", unsafe_allow_html=True)
        usuario = st.text_input("", placeholder="Ex: Arthur...")
        
        if st.form_submit_button("Entrer dans l'Académie"):
            if usuario:
                st.session_state['current_user'] = usuario
                if usuario in df_dragones['Propietario'].values:
                    nav('home')
                else:
                    nav('incubator')
            else:
                st.error("Le nom est requis.")

# --- LA INCUBADORA (SOLO PRIMERA VEZ) ---
elif st.session_state['page'] == 'incubator':
    st.markdown("<h1>La Couveuse Magique</h1>", unsafe_allow_html=True)
    
    with st.form("incubator_form"):
        st.markdown("### 1. Baptise ton dragon")
        nombre_dragon = st.text_input("Nom:", placeholder="Ex: Ignis, Aqualis...")
        
        st.markdown("### 2. Choisis son essence (Élément)")
        elemento = st.radio("", ["🔥 Feu (Fuego)", "💧 Eau (Agua)", "🌿 Plante (Planta)"], horizontal=True)
        
        if st.form_submit_button("Adopter l'Œuf"):
            if nombre_dragon:
                nuevo_dragon = pd.DataFrame([[st.session_state['current_user'], nombre_dragon, elemento, 0]], 
                                          columns=['Propietario', 'NombreDragon', 'Elemento', 'XP'])
                df_dragones = pd.concat([df_dragones, nuevo_dragon], ignore_index=True)
                save_data(df_dragones, FILE_DRAGONS)
                nav('home')
            else:
                st.error("Il lui faut un nom !")

# --- LA GUARIDA (EL DRAGÓN) ---
elif st.session_state['page'] == 'home':
    mi_dragon = df_dragones[df_dragones['Propietario'] == st.session_state['current_user']].iloc[0]
    xp_actual = mi_dragon['XP']
    stage = get_evolution_stage(xp_actual)
    
    st.markdown("""
    <div class="hero-header">
        <h1 style="font-size: 2rem;">Le Repaire</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:#2c1e16;'>{mi_dragon['NombreDragon']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><strong>Élément:</strong> {mi_dragon['Elemento']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='dragon-emoji'>{stage['emoji']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>Stade: {stage['name']}</h3>", unsafe_allow_html=True)
    
    # Barra de XP Mágica
    pct = min((xp_actual / stage['max_xp']) * 100, 100)
    st.markdown(f"""
    <div class="xp-container">
        <div class="xp-fill" style="width: {pct}%;"></div>
        <div class="xp-text">{xp_actual} / {stage['max_xp']} XP</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- EL GREMIO (MISIONES DE XP) ---
elif st.session_state['page'] == 'missions':
    st.markdown("<h1>La Guilde (Missions)</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.markdown("### 🔑 Code Secret du Maître")
    st.write("Entrez le code fourni par votre professeur pour gagner de l'expérience.")
    
    codigo = st.text_input("Code:", key="secret_code").upper()
    if st.button("Valider la Quête"):
        # Lógica sencilla de códigos
        valid_codes = {"FRANCAIS": 50, "DRAGON": 100, "MAGIE": 20}
        if codigo in valid_codes:
            idx = df_dragones.index[df_dragones['Propietario'] == st.session_state['current_user']].tolist()[0]
            df_dragones.at[idx, 'XP'] += valid_codes[codigo]
            save_data(df_dragones, FILE_DRAGONS)
            st.success(f"Quête accomplie ! +{valid_codes[codigo]} XP")
            st.balloons()
        else:
            st.error("Code invalide ou expiré.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- EL GRIMORIO (DIARIO) ---
elif st.session_state['page'] == 'journal':
    st.markdown("<h1>Le Grimoire (Journal)</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.write("Écrivez vos apprentissages du jour en français.")
    
    with st.form("grimoire_form"):
        reflexion = st.text_area("Vos pensées :", placeholder="Aujourd'hui j'ai appris...")
        if st.form_submit_button("Écrire dans le Grimoire (+10 XP)"):
            if reflexion:
                new_entry = pd.DataFrame([[st.session_state['current_user'], datetime.now().strftime("%d/%m %H:%M"), reflexion]], 
                                       columns=['Propietario', 'Date', 'Reflexion'])
                df_journal = pd.concat([new_entry, df_journal], ignore_index=True)
                save_data(df_journal, FILE_JOURNAL)
                
                # Recompensa por escribir
                idx = df_dragones.index[df_dragones['Propietario'] == st.session_state['current_user']].tolist()[0]
                df_dragones.at[idx, 'XP'] += 10
                save_data(df_dragones, FILE_DRAGONS)
                
                st.success("Page ajoutée avec succès !")
            else:
                st.error("Le parchemin est vide.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MENU INFERIOR (DOCK MEDIEVAL)
# ==========================================
# Mostramos el menú solo si el usuario ya ha pasado el login
if st.session_state['current_user'] and st.session_state['page'] != 'incubator':
    st.write("<br><br><br><br>", unsafe_allow_html=True) # Espaciador
    
    st.markdown("""
    <div class="dock-nav">
        <div class="dock-item" onclick="document.getElementById('btn-home').click()" title="Le Repaire">🐉</div>
        <div class="dock-item" onclick="document.getElementById('btn-missions').click()" title="La Guilde">⚔️</div>
        <div class="dock-item" onclick="document.getElementById('btn-journal').click()" title="Le Grimoire">📖</div>
        <div class="dock-item" onclick="document.getElementById('btn-logout').click()" title="Sortir">🚪</div>
    </div>
    """, unsafe_allow_html=True)

    # Botones invisibles de Streamlit para conectar el HTML con Python
    st.button("h", key="btn-home", on_click=nav, args=('home',), help="Hidden")
    st.button("m", key="btn-missions", on_click=nav, args=('missions',), help="Hidden")
    st.button("j", key="btn-journal", on_click=nav, args=('journal',), help="Hidden")
    def logout(): st.session_state['current_user'] = None; nav('login')
    st.button("l", key="btn-logout", on_click=logout, help="Hidden")
    
    st.markdown("<style>button[title='Hidden'] {display: none;}</style>", unsafe_allow_html=True)
