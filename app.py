import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Le Nid du Dragon",
    page_icon="🐉",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- FUNCIÓN PARA LEER TUS IMÁGENES LOCALES (.PNG) ---
def get_local_img(path):
    """Busca tus archivos .png y los codifica para la web."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            ext = path.split('.')[-1]
            return f"data:image/{ext};base64,{base64.b64encode(f.read()).decode()}"
    # Huevo genérico por si falla la ruta
    return "https://cdn-icons-png.flaticon.com/512/528/528098.png"

# Conectamos las imágenes asegurando la extensión .png
egg_feu_b64 = get_local_img("huevo_fuego.png")
egg_eau_b64 = get_local_img("huevo_agua.png")
egg_plante_b64 = get_local_img("huevo_planta.png")

# --- 2. CSS "FANTASÍA MEDIEVAL" ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=MedievalSharp&display=swap');

    :root {
        --primary: #8B0000;
        --accent: #D4AF37;
        --text: #2c1e16;
        --parchment: rgba(244, 238, 224, 0.95);
    }

    .stApp {
        background-image: url('https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'MedievalSharp', cursive;
    }
    
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4); 
        z-index: -1;
    }

    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .solid-panel {
        background: var(--parchment);
        border-radius: 8px;
        padding: 25px;
        border: 2px solid var(--accent);
        box-shadow: inset 0 0 15px rgba(139, 69, 19, 0.2), 5px 5px 15px rgba(0,0,0,0.6);
        margin-bottom: 25px;
        color: var(--text);
    }

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
        font-family: 'Cinzel', serif; font-weight: 900; font-size: 2.8rem;
        text-transform: uppercase; letter-spacing: 3px; text-shadow: 2px 2px 5px #000; margin-bottom: 5px;
    }

    h1, h2, h3, h4 { color: var(--primary) !important; font-family: 'Cinzel', serif; font-weight: 900 !important; }
    p, label, .stMarkdown { color: var(--text) !important; font-size: 1.1rem; }

    .stButton > button {
        background: linear-gradient(to bottom, #8B0000, #4a0000);
        color: var(--accent); border-radius: 5px; border: 2px solid var(--accent);
        padding: 12px; font-family: 'Cinzel', serif; font-weight: 700; font-size: 1.1rem;
        text-transform: uppercase; width: 100%; transition: all 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    
    .stButton > button:hover { background: linear-gradient(to bottom, #a30000, #5c0000); transform: translateY(-2px); }
    .stButton > button:active { transform: translateY(2px); }

    .dragon-emoji { font-size: 8rem; text-align: center; display: block; margin: 20px 0; animation: float 3s infinite ease-in-out; }
    
    /* --- HUEVOS 2D GAMING --- */
    .dragon-egg {
        width: 220px;
        height: 250px;
        margin: 20px auto;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        animation: float 3s infinite ease-in-out;
        mix-blend-mode: normal; /* Al ser PNG sin fondo, no hace falta multiply */
    }

    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    
    /* --- MEJORAS DE LECTURA EN LAS PREGUNTAS (ARCADE) --- */
    #game-question {
        font-size: 1.8rem !important;
        color: #1a1a1a !important;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid var(--primary);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .game-opt {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 1.3rem;
        padding: 18px;
        margin-bottom: 15px;
        border-radius: 8px;
        border: 2px solid #8B0000;
        cursor: pointer;
        text-align: center;
        font-weight: 900;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.1s, background 0.2s;
    }
    .game-opt:hover {
        background: #fdf5e6 !important;
        transform: scale(1.02);
    }

    .xp-container { background: #1a1a1a; border-radius: 10px; height: 25px; position: relative; border: 2px solid var(--accent); margin-top: 15px;}
    .xp-fill { background: linear-gradient(90deg, #4b0082, #8a2be2, #00ffff); height: 100%; width: 0%; transition: width 0.8s; border-radius: 8px;}
    .xp-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: sans-serif; font-weight: bold; font-size: 0.8rem; color: white;}

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    div[data-testid="column"] { display: flex; flex-direction: column; align-items: center; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# Inyectamos tus imágenes base64 .png
st.markdown(f"""
<style>
    .egg-feu {{ background-image: url('{egg_feu_b64}'); }}
    .egg-eau {{ background-image: url('{egg_eau_b64}'); }}
    .egg-plante {{ background-image: url('{egg_plante_b64}'); }}
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

# --- 4. LÓGICA DE EVOLUCIÓN ---
def get_dragon_visual(xp, elemento):
    if xp < 100:
        if "Feu" in elemento: return "<div class='dragon-egg egg-feu'></div>", "L'Œuf de Magma"
        elif "Eau" in elemento: return "<div class='dragon-egg egg-eau'></div>", "L'Œuf Océanique"
        else: return "<div class='dragon-egg egg-plante'></div>", "L'Œuf Sylvestre"
    elif xp < 300: return "<div class='dragon-emoji'>🦎</div>", "Bébé Dragon"
    elif xp < 600: return "<div class='dragon-emoji'>🦖</div>", "Jeune Dragon"
    elif xp < 1000: return "<div class='dragon-emoji'>🐲</div>", "Dragon Adulte"
    else: return "<div class='dragon-emoji'>🐉</div>", "Dragon Légendaire"

def get_max_xp(xp):
    if xp < 100: return 100
    elif xp < 300: return 300
    elif xp < 600: return 600
    elif xp < 1000: return 1000
    else: return 99999

# --- 5. NAVEGACIÓN Y ESTADO ---
if 'page' not in st.session_state: st.session_state['page'] = 'login'
if 'current_user' not in st.session_state: st.session_state['current_user'] = None

def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

def ganar_xp(cantidad):
    idx = df_dragones.index[df_dragones['Propietario'] == st.session_state['current_user']].tolist()[0]
    df_dragones.at[idx, 'XP'] += cantidad
    save_data(df_dragones, FILE_DRAGONS)
    st.toast(f"Merveilleux! +{cantidad} XP", icon="✨")
    st.rerun()

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- LOGIN ---
if st.session_state['page'] == 'login':
    st.markdown("<div class='hero-header'><h1>L'Académie des Dragons</h1><p style='color:var(--accent);'>Bienvenue, apprenti dresseur.</p></div>", unsafe_allow_html=True)
    with st.form("login_form"):
        st.markdown("<h3 style='text-align:center;'>Entrez votre nom</h3>", unsafe_allow_html=True)
        usuario = st.text_input("", placeholder="Ex: Arthur...")
        if st.form_submit_button("Entrer dans l'Académie"):
            if usuario:
                st.session_state['current_user'] = usuario
                if usuario in df_dragones['Propietario'].values: nav('home')
                else: nav('incubator')
            else: st.error("Le nom est requis.")

# --- LA INCUBADORA (NUEVO DRAGÓN) ---
elif st.session_state['page'] == 'incubator':
    st.markdown("<h1>La Couveuse Magique</h1>", unsafe_allow_html=True)
    with st.form("incubator_form"):
        st.markdown("### 1. Baptise ton dragon")
        nombre_dragon = st.text_input("Nom:", placeholder="Ex: Ignis, Aqualis...")
        st.markdown("### 2. Choisis son essence (Élément)")
        elemento = st.radio("", ["🔥 Feu (Fuego)", "💧 Eau (Agua)", "🌿 Plante (Planta)"], horizontal=True)
        if st.form_submit_button("Adopter l'Œuf"):
            if nombre_dragon:
                nuevo_dragon = pd.DataFrame([[st.session_state['current_user'], nombre_dragon, elemento, 0]], columns=['Propietario', 'NombreDragon', 'Elemento', 'XP'])
                df_dragones = pd.concat([df_dragones, nuevo_dragon], ignore_index=True)
                save_data(df_dragones, FILE_DRAGONS)
                nav('home')
            else: st.error("Il lui faut un nom !")

# --- LA GUARIDA (EL DRAGÓN) ---
elif st.session_state['page'] == 'home':
    mi_dragon = df_dragones[df_dragones['Propietario'] == st.session_state['current_user']].iloc[0]
    xp_actual = mi_dragon['XP']
    emoji, nombre_fase = get_dragon_visual(xp_actual, mi_dragon['Elemento'])
    max_xp = get_max_xp(xp_actual)
    
    st.markdown("<div class='hero-header'><h1 style='font-size: 2rem;'>Le Repaire</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:#2c1e16;'>{mi_dragon['NombreDragon']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><strong>Élément:</strong> {mi_dragon['Elemento']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"{emoji}", unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align:center;'>Stade: {nombre_fase}</h3>", unsafe_allow_html=True)
    
    pct = min((xp_actual / max_xp) * 100, 100)
    st.markdown(f"""
    <div class="xp-container">
        <div class="xp-fill" style="width: {pct}%;"></div>
        <div class="xp-text">{xp_actual} / {max_xp} XP</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- EL GREMIO (10 MISIONES ARCADE) ---
elif st.session_state['page'] == 'missions':
    st.markdown("<h1>La Guilde (Missions)</h1>", unsafe_allow_html=True)
    
    with st.expander("🗝️ Code Secret du Maître", expanded=False):
        codigo = st.text_input("Code:").upper()
        if st.button("Valider la Quête Secrète"):
            if codigo == "DRAGON": ganar_xp(100)
            else: st.error("Code invalide.")
            
    st.markdown("### ⚔️ Entraînement Quotidien")
    
    with st.expander("🔢 123 Les Nombres"):
        st.markdown("<div id='game-question'>10 stylos = 20€. 1 stylo = ?</div>", unsafe_allow_html=True)
        if st.button("2€", key="n1"): ganar_xp(10)
        if st.button("5€", key="n2"): st.error("Incorrect")
    
    with st.expander("🚀 Futur Simple"):
        st.markdown("<div id='game-question'>Demain je ___ (manger)</div>", unsafe_allow_html=True)
        if st.button("mangerai", key="f1"): ganar_xp(10)
        if st.button("mange", key="f2"): st.error("Incorrect")
        
    with st.expander("🍕 Partitifs"):
        st.markdown("<div id='game-question'>Je veux ___ eau</div>", unsafe_allow_html=True)
        if st.button("de l'", key="p1"): ganar_xp(10)
        if st.button("du", key="p2"): st.error("Incorrect")
        
    with st.expander("🏃 Sport"):
        st.markdown("<div id='game-question'>Le sport dans l'eau ?</div>", unsafe_allow_html=True)
        if st.button("Natation", key="s1"): ganar_xp(10)
        if st.button("Tennis", key="s2"): st.error("Incorrect")
        
    with st.expander("📣 Impératif"):
        st.markdown("<div id='game-question'>(Courir) ___ vite !</div>", unsafe_allow_html=True)
        if st.button("Cours", key="i1"): ganar_xp(10)
        if st.button("Courir", key="i2"): st.error("Incorrect")
        
    with st.expander("🌍 Quiz ODD"):
        st.markdown("<div id='game-question'>L'ODD 13 concerne...</div>", unsafe_allow_html=True)
        if st.button("Le Climat", key="o1"): ganar_xp(10)
        if st.button("L'Eau", key="o2"): st.error("Incorrect")
        
    with st.expander("🌿 SVT (ODD)"):
        st.markdown("<div id='game-question'>Où jeter une bouteille plastique ?</div>", unsafe_allow_html=True)
        if st.button("Poubelle Jaune", key="v1"): ganar_xp(10)
        if st.button("Poubelle Bleue", key="v2"): st.error("Incorrect")
        
    with st.expander("🗺️ Géo & Hist"):
        st.markdown("<div id='game-question'>Où sont nés les JO ?</div>", unsafe_allow_html=True)
        if st.button("En Grèce", key="g1"): ganar_xp(10)
        if st.button("En Italie", key="g2"): st.error("Incorrect")
        
    with st.expander("📐 Maths"):
        st.markdown("<div id='game-question'>100m en 10s. Vitesse ?</div>", unsafe_allow_html=True)
        if st.button("10 m/s", key="m1"): ganar_xp(10)
        if st.button("100 m/s", key="m2"): st.error("Incorrect")
        
    with st.expander("📚 Français"):
        st.markdown("<div id='game-question'>Synonyme de Gagner :</div>", unsafe_allow_html=True)
        if st.button("Remporter", key="r1"): ganar_xp(10)
        if st.button("Échouer", key="r2"): st.error("Incorrect")

# --- EL GRIMORIO (DIARIO) ---
elif st.session_state['page'] == 'journal':
    st.markdown("<h1>Le Grimoire (Journal)</h1>", unsafe_allow_html=True)
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.write("Écrivez vos apprentissages du jour en français.")
    
    with st.form("grimoire_form"):
        reflexion = st.text_area("Vos pensées :", placeholder="Aujourd'hui j'ai appris...")
        if st.form_submit_button("Écrire dans le Grimoire (+10 XP)"):
            if reflexion:
                new_entry = pd.DataFrame([[st.session_state['current_user'], datetime.now().strftime("%d/%m %H:%M"), reflexion]], columns=['Propietario', 'Date', 'Reflexion'])
                df_journal = pd.concat([new_entry, df_journal], ignore_index=True)
                save_data(df_journal, FILE_JOURNAL)
                ganar_xp(10)
            else: 
                st.error("Le parchemin est vide.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    mis_entradas = df_journal[df_journal['Propietario'] == st.session_state['current_user']]
    for i, row in mis_entradas.iterrows():
        st.markdown(f"<div class='solid-panel' style='padding:15px;'><small style='color:#8B0000;'>{row['Date']}</small><br><i>{row['Reflexion']}</i></div>", unsafe_allow_html=True)

# ==========================================
# MENU INFERIOR
# ==========================================
if st.session_state['current_user'] and st.session_state['page'] != 'incubator':
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🐉\nGuarida"): nav('home')
    with c2:
        if st.button("⚔️\nGremio"): nav('missions')
    with c3:
        if st.button("📖\nGrimorio"): nav('journal')
    with c4:
        if st.button("🚪\nSalir"): 
            st.session_state['current_user'] = None
            nav('login')
