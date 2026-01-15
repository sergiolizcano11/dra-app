import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN CORREGIDA ---
# CAMBIO: layout="centered" es lo correcto. El CSS se encarga del resto.
st.set_page_config(page_title="Mon Dragon Français", layout="centered", page_icon="🐉")

# CSS PRO PARA TRANSFORMAR STREAMLIT EN APP MÓVIL
st.markdown("""
    <style>
    /* Ajuste del cuerpo principal */
    .block-container {
        padding-bottom: 100px; /* Espacio para el menú inferior */
        padding-top: 20px;
        max-width: 500px; /* Forzar anchura tipo móvil incluso en PC */
    }
    
    /* MENÚ FIJO ABAJO (Navigation Bar) */
    div[data-testid="stRadio"] > div {
        display: flex;
        justify-content: space-around;
        width: 100%;
        background-color: white;
        padding: 15px 0;
        position: fixed;
        bottom: 0;
        left: 0;
        z-index: 9999;
        box-shadow: 0px -5px 15px rgba(0,0,0,0.1);
        border-top: 1px solid #eee;
    }
    
    /* Estilo de los botones del menú */
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none;
        font-size: 24px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    div[data-testid="stRadio"] label:hover {
        transform: scale(1.2);
        color: #6C63FF;
    }
    
    /* TARJETAS (Cards) */
    .dragon-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #e1e4e8;
        text-align: center;
    }
    
    /* BARRA DE PROGRESO PERSONALIZADA */
    .xp-text {
        font-weight: bold;
        color: #555;
        font-size: 0.9em;
        margin-bottom: 5px;
    }
    
    /* Ocultar elementos nativos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'setup_complete': False,
        'nombre_dragon': "",
        'elemento': "", # feu, eau, nature
        'xp': 0,
        'nivel': 1,
        'energia': 100
    }

# --- 3. RECURSOS VISUALES (HUEVOS POR COLOR) ---
ASSETS = {
    'huevo': {
        'feu': 'https://cdn-icons-png.flaticon.com/512/7880/7880228.png',   # Rojo
        'eau': 'https://cdn-icons-png.flaticon.com/512/7880/7880222.png',   # Azul
        'nature': 'https://cdn-icons-png.flaticon.com/512/7880/7880233.png' # Verde
    },
    'dragon': {
        'feu': 'https://cdn-icons-png.flaticon.com/512/1625/1625348.png',
        'eau': 'https://cdn-icons-png.flaticon.com/512/3093/3093608.png',
        'nature': 'https://cdn-icons-png.flaticon.com/512/3715/3715097.png'
    }
}

# --- 4. LÓGICA DE JUEGO ---
def calcular_nivel(xp_actual, nivel_actual):
    # Coste para subir de nivel: Nivel * 100 XP
    xp_necesaria = nivel_actual * 100
    return xp_necesaria

def get_imagen_actual():
    # Si es nivel 1, es huevo. Si es > 1, es dragón.
    if st.session_state.db['nivel'] == 1:
        return ASSETS['huevo'][st.session_state.db['elemento']]
    else:
        return ASSETS['dragon'][st.session_state.db['elemento']]

# --- 5. ONBOARDING (PRIMERA VEZ) ---
if not st.session_state.db['setup_complete']:
    st.title("🥚 Choisis ton Destin")
    st.write("Selecciona el color de tu huevo para comenzar:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(ASSETS['huevo']['feu'], width=80)
        if st.button("Rouge (Feu)"):
            st.session_state.db['elemento'] = 'feu'
            st.session_state.db['setup_complete'] = True
            st.rerun()
    with col2:
        st.image(ASSETS['huevo']['nature'], width=80)
        if st.button("Vert (Nature)"):
            st.session_state.db['elemento'] = 'nature'
            st.session_state.db['setup_complete'] = True
            st.rerun()
    with col3:
        st.image(ASSETS['huevo']['eau'], width=80)
        if st.button("Bleu (Eau)"):
            st.session_state.db['elemento'] = 'eau'
            st.session_state.db['setup_complete'] = True
            st.rerun()

# --- 6. APLICACIÓN PRINCIPAL ---
else:
    # --- MENÚ DE NAVEGACIÓN INFERIOR ---
    menu_options = ["🏠 Accueil", "⚔️ Quiz", "📊 Stats"]
    selection = st.radio(
        "", 
        menu_options, 
        horizontal=True, 
        label_visibility="collapsed",
        key="nav_menu"
    )

    # --- VISTA: HOME (ACCUEIL) ---
    if selection == "🏠 Accueil":
        st.header(f"Tu Dragon: {st.session_state.db['elemento'].capitalize()}")
        
        # Tarjeta Visual del Dragón
        st.markdown('<div class="dragon-card">', unsafe_allow_html=True)
        st.image(get_imagen_actual(), width=150)
        
        # Lógica de XP
        xp_total = st.session_state.db['xp']
        nivel = st.session_state.db['nivel']
        meta = calcular_nivel(xp_total, nivel)
        
        # Barra de Progreso Matemática
        progreso = min(xp_total / meta, 1.0)
        falta = meta - xp_total
        
        st.subheader(f"Niveau {nivel}")
        st.markdown(f"""
            <div class="xp-text">
                XP: {xp_total} / {meta} <br>
                <span style='color:#FF4B4B; font-size:0.8em;'>Il te manque {falta} XP pour évoluer!</span>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progreso)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VISTA: QUIZ (TEST) ---
    elif selection == "⚔️ Quiz":
        st.header("📝 Le Challenge")
        st.caption("Responde correctamente para ganar XP y evolucionar.")
        
        with st.container():
            st.markdown('<div class="dragon-card">', unsafe_allow_html=True)
            st.markdown("### Question du jour")
            st.write("Transforma la frase al **Passé Composé**:")
            st.info("Je mange une pomme.")
            
            opcion = st.radio("Selecciona:", 
                             ["J'ai mangé une pomme", 
                              "Je suis mangé une pomme", 
                              "Je mangeai une pomme"])
            
            if st.button("Vérifier Réponse"):
                if opcion == "J'ai mangé une pomme":
                    puntos = 20
                    st.session_state.db['xp'] += puntos
                    st.balloons()
                    st.success(f"¡Correcto! +{puntos} XP")
                    
                    # Chequeo de nivel
                    meta = calcular_nivel(st.session_state.db['xp'], st.session_state.db['nivel'])
                    if st.session_state.db['xp'] >= meta:
                        st.session_state.db['nivel'] += 1
                        st.session_state.db['xp'] = 0 
                        st.toast("¡Has subido de nivel!", icon="🆙")
                    
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Incorrect. Recuerda: Manger usa el auxiliar Avoir.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- VISTA: STATS (PROFESOR) ---
    elif selection == "📊 Stats":
        st.header("📊 Tes Compétences")
        st.markdown('<div class="dragon-card">', unsafe_allow_html=True)
        
        # Datos visuales
        stats = {
            'Grammaire': 80,
            'Vocabulaire': 45,
            'Oral': 60
        }
        st.bar_chart(stats)
        
        st.markdown("---")
        st.caption("Objetivo de Desarrollo Sostenible (ODS 4)")
        st.write("🎓 **Éducation de Qualité**")
        st.info("Estás en el percentil superior de tu clase esta semana.")
        st.markdown('</div>', unsafe_allow_html=True)