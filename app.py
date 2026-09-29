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
    return "https://cdn-icons-png.flaticon.com/512/528/528098.png"

# Conectamos las imágenes de los huevos y bebés personalizados
egg_feu_b64 = get_local_img("huevo_fuego.png")
egg_eau_b64 = get_local_img("huevo_agua.png")
egg_plante_b64 = get_local_img("huevo_planta.png")

bebe_feu_b64 = get_local_img("bebe_fuego.png")
bebe_eau_b64 = get_local_img("bebe_agua.png")
bebe_plante_b64 = get_local_img("bebe_planta.png")

# --- 2. CSS "CÓMIC / POP-ART" (ALTA VISIBILIDAD Y COLOR) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Poppins:wght@400;700;900&display=swap');

    :root {
        --primary: #0066CC;
        --accent: #FFD93D;
        --success: #28a745;
        --text: #1A1A1A; /* Texto oscuro de máxima legibilidad */
        --card-bg: #FFFFFF;
    }

    /* Fondo general claro y colorido con patrón alegre */
    .stApp {
        background-color: #F0F4F8;
        background-image: radial-gradient(#d0d9e5 1.5px, transparent 1.5px);
        background-size: 24px 24px;
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.6); 
        z-index: -1;
    }

    /* Tarjetas limpias estilo cómic con bordes definidos */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .solid-panel {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 22px;
        border: 2px solid #1A1A1A;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.8);
        margin-bottom: 25px;
        color: var(--text);
    }

    /* Cabecera principal muy viva */
    .hero-header {
        background: linear-gradient(135deg, #0066CC, #00C6FF);
        padding: 30px 20px;
        border-radius: 0 0 25px 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 4px solid #1A1A1A;
        box-shadow: 0 8px 0 rgba(0,0,0,0.15);
    }
    .hero-header h1 { 
        font-family: 'Bangers', cursive; 
        font-size: 3rem;
        letter-spacing: 2px;
        text-shadow: 3px 3px 0px #1A1A1A;
        color: white !important;
        margin-bottom: 5px;
    }

    /* Textos oscuros garantizados para lectura óptima */
    h1, h2, h3, h4, p, label, .stMarkdown { 
        color: var(--text) !important; 
    }

    /* Botones dinámicos y coloridos */
    .stButton > button {
        background: var(--accent);
        color: #1A1A1A;
        border-radius: 12px;
        border: 2px solid #1A1A1A;
        border-bottom: 5px solid #1A1A1A;
        padding: 12px;
        font-family: 'Bangers', cursive;
        font-size: 1.3rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.1s;
    }
    
    .stButton > button:hover {
        background: #ffe65c;
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(3px);
        border-bottom: 2px solid #1A1A1A;
    }

    /* --- HUEVOS Y BEBÉS 2D GAMING --- */
    .dragon-egg {
        width: 180px;
        height: 180px;
        margin: 20px auto;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        animation: float 3s infinite ease-in-out;
    }
    
    .dragon-baby {
        width: 180px;
        height: 180px;
        margin: 20px auto;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        animation: float 3s infinite ease-in-out;
    }

    .glow-feu { filter: drop-shadow(0px 10px 15px rgba(255, 69, 0, 0.5)); }
    .glow-eau { filter: drop-shadow(0px 10px 15px rgba(0, 191, 255, 0.5)); }
    .glow-plante { filter: drop-shadow(0px 10px 15px rgba(50, 205, 50, 0.5)); }

    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    
    .xp-container { background: #FFFFFF; border-radius: 12px; height: 28px; position: relative; border: 2px solid #1A1A1A; margin-top: 15px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }
    .xp-fill { background: linear-gradient(90deg, #FFD93D, #FF6B6B); height: 100%; width: 0%; transition: width 0.8s; border-radius: 8px;}
    .xp-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: 'Poppins', sans-serif; font-weight: 900; font-size: 0.85rem; color: #1A1A1A;}

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    div[data-testid="column"] { display: flex; flex-direction: column; align-items: center; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# Inyectamos las imágenes base64 en CSS de manera dinámica
st.markdown(f"""
<style>
    .egg-feu {{ background-image: url('{egg_feu_b64}'); }}
    .egg-eau {{ background-image: url('{egg_eau_b64}'); }}
    .egg-plante {{ background-image: url('{egg_plante_b64}'); }}
    
    .baby-feu {{ background-image: url('{bebe_feu_b64}'); }}
    .baby-eau {{ background-image: url('{bebe_eau_b64}'); }}
    .baby-plante {{ background-image: url('{bebe_plante_b64}'); }}
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

# --- 4. LÓGICA DE EVOLUCIÓN (FASES CON ASSETS PROPIOS) ---
def get_dragon_visual(xp, elemento):
    if xp < 100:
        if "Feu" in elemento: return "<div class='dragon-egg egg-feu glow-feu'></div>", "L'Œuf de Lave"
        elif "Eau" in elemento: return "<div class='dragon-egg egg-eau glow-eau'></div>", "L'Œuf des Courants"
        else: return "<div class='dragon-egg egg-plante glow-plante'></div>", "L'Œuf des Racines"
    elif xp < 300:
        if "Feu" in elemento: return "<div class='dragon-baby baby-feu glow-feu'></div>", "Bébé de Feu"
        elif "Eau" in elemento: return "<div class='dragon-baby baby-eau glow-eau'></div>", "Bébé d'Eau"
        else: return "<div class='dragon-baby baby-plante glow-plante'></div>", "Bébé de Plante"
    elif xp < 600: return "<div class='dragon-emoji'>🦖</div>", "Jeune Dragon (Adolescent)"
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
    st.markdown("<div class='hero-header'><h1>L'Académie des Dragons</h1><p style='color:#FFF; font-weight:bold;'>Bienvenue, apprenti dresseur.</p></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='hero-header'><h1>La Couveuse Magique</h1></div>", unsafe_allow_html=True)
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
    visual_html, nombre_fase = get_dragon_visual(xp_actual, mi_dragon['Elemento'])
    max_xp = get_max_xp(xp_actual)
    
    st.markdown("<div class='hero-header'><h1 style='font-size: 2rem;'>Le Repaire</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='solid-panel'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>{mi_dragon['NombreDragon']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><strong>Élément:</strong> {mi_dragon['Elemento']}</p>", unsafe_allow_html=True)
    
    st.markdown(f"{visual_html}", unsafe_allow_html=True)
    
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
    st.markdown("<div class='hero-header'><h1>La Guilde</h1></div>", unsafe_allow_html=True)
    
    with st.expander("🗝️ Code Secret du Maître", expanded=False):
        codigo = st.text_input("Code:").upper()
        if st.button("Valider la Quête Secrète"):
            if codigo == "DRAGON": ganar_xp(100)
            else: st.error("Code invalide.")
            
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
    st.markdown("<div class='hero-header'><h1>Le Grimoire</h1></div>", unsafe_allow_html=True)
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
        st.markdown(f"<div class='solid-panel' style='padding:15px;'><small style='color:#0066CC;'>{row['Date']}</small><br><i>{row['Reflexion']}</i></div>", unsafe_allow_html=True)

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
