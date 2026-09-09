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
        font-family: 'Cinzel', serif; 
        font-weight: 900; 
        font-size: 2.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 2px 2px 5px #000;
        margin-bottom: 5px;
    }

    h1, h2, h3, h4 { color: var(--primary) !important; font-family: 'Cinzel', serif; font-weight: 900 !important; }
    p, label, .stMarkdown { color: var(--text) !important; font-size: 1.1rem; }

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
    
    .stButton > button:hover { background: linear-gradient(to bottom, #a30000, #5c0000); transform: translateY(-2px); }
    .stButton > button:active { transform: translateY(2px); }

    .dragon-emoji { font-size: 8rem; text-align: center; display: block; margin: 20px 0; animation: float 3s infinite ease-in-out; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    
    .xp-container { background: #1a1a1a; border-radius: 10px; height: 25px; position: relative; border: 2px solid var(--accent); margin-top: 15px;}
    .xp-fill { background: linear-gradient(90deg, #4b0082, #8a2be2, #00ffff); height: 100%; width: 0%; transition: width 0.8s; border-radius: 8px;}
    .xp-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: sans-serif; font-weight: bold; font-size: 0.8rem; color: white;}

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* MENÚ NATIVO STREAMLIT (FANTASÍA) */
    div[data-testid="column"] { display: flex; flex-direction: column; align-items: center; justify-content: center; }
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

# --- 4. LÓGICA DE EVOLUCIÓN (HUEVOS PERSONALIZADOS) ---
def get_dragon_visual(xp, elemento):
    if xp < 100:
        if "Feu" in elemento: return "🌋", "L'Œuf de Lave"
        elif "Eau" in elemento: return "🌀", "L'Œuf des Courants"
        else: return "🌿", "L'Œuf des Racines"
    elif xp < 300: return "🦎", "Bébé Dragon"
    elif xp < 600: return "🦖", "Jeune Dragon"
    elif xp < 1000: return "🐲", "Dragon Adulte"
    else: return "🐉", "Dragon Légendaire"

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
    
    st.markdown(f"<div class='dragon-emoji'>{emoji}</div>", unsafe_allow_html=True)
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
    
    # 1. Códigos Secretos
    with st.expander("🗝️ Code Secret du Maître", expanded=False):
        codigo = st.text_input("Code:").upper()
        if st.button("Valider la Quête Secrète"):
            if codigo == "DRAGON": ganar_xp(100)
            else: st.error("Code invalide.")
            
    # 2. Las 10 Misiones Arcade[cite: 1]
    st.markdown("### ⚔️ Entraînement Quotidien")
    
    with st.expander("🔢 123 Les Nombres"):
        if st.button("Valider: 10 stylos = 20€. 1 stylo = 2€"): ganar_xp(10)
    
    with st.expander("🚀 Futur Simple"):
        if st.button("Valider: Demain je mangerai"): ganar_xp(10)
        
    with st.expander("🍕 Partitifs"):
        if st.button("Valider: Je veux de l'eau"): ganar_xp(10)
        
    with st.expander("🏃 Sport"):
        if st.button("Valider: Le sport dans l'eau c'est la natation"): ganar_xp(10)
        
    with st.expander("📣 Impératif"):
        if st.button("Valider: (Courir) Cours vite !"): ganar_xp(10)
        
    with st.expander("🌍 Quiz ODD"):
        if st.button("Valider: ODD 13 = Le Climat"): ganar_xp(10)
        
    with st.expander("🌿 SVT (ODD)"):
        if st.button("Valider: Bouteille plastique = Poubelle Jaune"): ganar_xp(10)
        
    with st.expander("🗺️ Géo & Hist"):
        if st.button("Valider: Les JO sont nés en Grèce"): ganar_xp(10)
        
    with st.expander("📐 Maths"):
        if st.button("Valider: 100m en 10s = 10m/s"): ganar_xp(10)
        
    with st.expander("📚 Français"):
        if st.button("Valider: Synonyme de Gagner = Remporter"): ganar_xp(10)

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
                
                # AQUÍ ESTABA EL ERROR: Hemos eliminado la línea "global df_journal"
                df_journal = pd.concat([new_entry, df_journal], ignore_index=True)
                save_data(df_journal, FILE_JOURNAL)
                ganar_xp(10)
            else: 
                st.error("Le parchemin est vide.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mostrar el historial del grimorio
    mis_entradas = df_journal[df_journal['Propietario'] == st.session_state['current_user']]
    for i, row in mis_entradas.iterrows():
        st.markdown(f"<div class='solid-panel' style='padding:15px;'><small style='color:#8B0000;'>{row['Date']}</small><br><i>{row['Reflexion']}</i></div>", unsafe_allow_html=True)
# ==========================================
# MENU INFERIOR NATIVO DE STREAMLIT
# ==========================================
if st.session_state['current_user'] and st.session_state['page'] != 'incubator':
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Barra de botones pura en Python (evita "dos menús" de iframes HTML)
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
