import streamlit as st
import time
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN E INYECCIÓN CSS (ESTILO APP MÓVIL MUSA + ARCADE) ---
st.set_page_config(page_title="Mon Cycle Français", layout="centered", page_icon="🐉")

# Colores suaves estilo wellness
TEMAS = {
    "Fuego": {"bg": "#FFF0EE", "accent": "#FF867C", "gradient": "linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 100%)"},
    "Agua":  {"bg": "#E3F2FD", "accent": "#64B5F6", "gradient": "linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)"},
    "Naturaleza": {"bg": "#E8F5E9", "accent": "#81C784", "gradient": "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)"}
}

st.markdown("""
    <style>
    /* RESET Y TIPOGRAFÍA */
    .stApp { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #4A4A4A; }
    
    /* ESTILOS DEL JUEGO DE MEMORIA (NUEVO) */
    .stButton button {
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: transform 0.1s !important;
        font-size: 24px !important;
        height: 80px !important; /* Altura fija para cartas */
        width: 100% !important;
    }
    .stButton button:active { transform: scale(0.95) !important; }
    
    /* BARRA DE PROGRESO (XP) */
    .xp-container {
        width: 100%; background-color: #F0F0F0; border-radius: 20px;
        margin: 15px 0; height: 8px; overflow: hidden;
    }
    .xp-bar { height: 100%; border-radius: 20px; transition: width 0.6s cubic-bezier(0.4, 0.0, 0.2, 1); }
    
    /* CÍRCULO CENTRAL */
    .dragon-circle {
        width: 260px; height: 260px; border-radius: 50%; margin: 30px auto;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08); border: 10px solid white;
        background: white; position: relative; transition: all 0.5s ease;
    }
    
    /* MENÚ DOCK INFERIOR */
    .dock {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
        padding: 15px 0; box-shadow: 0 -10px 30px rgba(0,0,0,0.05);
        display: flex; justify-content: space-around; z-index: 999;
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    
    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO (ROBUSTA) ---
if 'user' not in st.session_state:
    st.session_state.user = {}

# Valores por defecto del usuario
defaults = {
    'setup_complete': False,
    'nombre': 'Apprenti',
    'elemento': 'Fuego',
    'nivel': 1,
    'xp': 0,
    'xp_next': 50,
    'stats': {'input': 0, 'output': 0},
    'fase_actual': 'Éveil',
    'view': 'Home'
}

for key, val in defaults.items():
    if key not in st.session_state.user:
        st.session_state.user[key] = val

# --- 3. ESTADO ESPECÍFICO DEL MINIJUEGO ---
if 'memory_game' not in st.session_state:
    st.session_state.memory_game = {
        'cards': [],           # Lista de cartas barajadas
        'flipped': [],         # Índices de cartas volteadas actualmente (max 2)
        'matched': set(),      # Índices de cartas ya emparejadas permanentemente
        'game_over': False,
        'initialized': False
    }

# --- 4. BIBLIOTECA DE ASSETS ---
ASSETS = {
    "Fuego": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880228.png", 
        "Expansion": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", 
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203150.png",
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699313.png"
    },
    "Agua": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", 
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3093/3093608.png", 
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203158.png", 
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699298.png"
    },
    "Naturaleza": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880233.png", 
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png", 
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203164.png", 
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699276.png"
    }
}

# --- 5. LÓGICA DEL MINIJUEGO (MEMORY MATCH) ---
def init_game():
    # Vocabulario: Pares (Concepto, Emoji/Imagen)
    vocabulario = [
        ("Pomme", "🍎"), ("Chien", "🐶"), ("Maison", "🏠"),
        ("Soleil", "☀️"), ("Livre", "📖"), ("Chat", "🐱")
    ]
    # Creamos las cartas duplicando y barajando
    deck = []
    for id_pair, (fr, icon) in enumerate(vocabulario):
        deck.append({'id': id_pair, 'content': fr, 'type': 'text'})
        deck.append({'id': id_pair, 'content': icon, 'type': 'icon'})
    
    random.shuffle(deck)
    st.session_state.memory_game['cards'] = deck
    st.session_state.memory_game['flipped'] = []
    st.session_state.memory_game['matched'] = set()
    st.session_state.memory_game['game_over'] = False
    st.session_state.memory_game['initialized'] = True

def render_memory_game(accent_color):
    st.markdown(f"<h2 style='text-align:center; color:{accent_color};'>Memory Match 🧠</h2>", unsafe_allow_html=True)
    st.caption("Encuentra las parejas para ganar 50 XP")

    # Inicializar si es necesario
    if not st.session_state.memory_game['initialized']:
        init_game()

    # Botón de reinicio
    if st.button("🔄 Reiniciar Juego", type="secondary"):
        init_game()
        st.rerun()

    state = st.session_state.memory_game
    cards = state['cards']

    # Grid de 3 columnas
    cols = st.columns(3)
    
    # Renderizado de cartas
    for i, card in enumerate(cards):
        col = cols[i % 3]
        
        # Determinar qué mostrar
        is_flipped = i in state['flipped']
        is_matched = i in state['matched']
        
        # Diseño de la carta
        card_label = "❓"
        if is_flipped or is_matched:
            card_label = card['content']
        
        # Botón (La carta)
        # Deshabilitamos si ya está acertada o si ya hay 2 levantadas (y esta no es una de ellas)
        disabled = is_matched or (len(state['flipped']) >= 2 and not is_flipped)
        
        if col.button(card_label, key=f"card_{i}", disabled=disabled, use_container_width=True):
            if not is_flipped and not is_matched:
                state['flipped'].append(i)
                st.rerun()

    # Lógica de comprobación (se ejecuta tras el rerun del clic)
    if len(state['flipped']) == 2:
        idx1, idx2 = state['flipped']
        card1 = cards[idx1]
        card2 = cards[idx2]

        if card1['id'] == card2['id']:
            # ¡Pareja encontrada!
            state['matched'].add(idx1)
            state['matched'].add(idx2)
            state['flipped'] = [] # Limpiamos flipped inmediatamente
            st.toast("¡Pareja encontrada! 🎉", icon="✅")
            st.rerun()
        else:
            # Fallo: Esperamos un poco para que el usuario vea la carta y reseteamos
            time.sleep(0.7) 
            state['flipped'] = []
            st.rerun()

    # Condición de Victoria
    if len(state['matched']) == len(cards) and not state['game_over']:
        state['game_over'] = True
        xp_win = 50
        st.session_state.user['xp'] += xp_win
        st.balloons()
        st.success(f"¡Bravo! Has completado el entrenamiento. +{xp_win} XP")
        
        # Actualizamos nivel si corresponde
        if st.session_state.user['xp'] >= st.session_state.user['xp_next']:
            st.session_state.user['nivel'] += 1
            st.session_state.user['xp'] = 0
            st.session_state.user['xp_next'] = int(st.session_state.user['xp_next'] * 1.2)
            st.toast("¡NIVEL SUBIDO!", icon="🆙")

# --- 6. ONBOARDING ---
if not st.session_state.user['setup_complete']:
    st.title("Bienvenue ✨")
    st.write("Elige tu energía:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(ASSETS["Fuego"]["Éveil"], width=80)
        if st.button("Passion"):
            st.session_state.user['elemento'] = "Fuego"
            st.session_state.user['setup_complete'] = True
            st.rerun()
    with c2:
        st.image(ASSETS["Agua"]["Éveil"], width=80)
        if st.button("Calme"):
            st.session_state.user['elemento'] = "Agua"
            st.session_state.user['setup_complete'] = True
            st.rerun()
    with c3:
        st.image(ASSETS["Naturaleza"]["Éveil"], width=80)
        if st.button("Force"):
            st.session_state.user['elemento'] = "Naturaleza"
            st.session_state.user['setup_complete'] = True
            st.rerun()

# --- 7. APP PRINCIPAL ---
else:
    # Tema dinámico
    tema = TEMAS[st.session_state.user['elemento']]
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {tema['bg']}; }}
        .xp-bar {{ background: {tema['gradient']}; width: {(st.session_state.user['xp'] / st.session_state.user['xp_next']) * 100}%; }}
        .dragon-circle {{ background: {tema['gradient']}; }}
        h1, h2, h3 {{ color: {tema['accent']}; font-weight: 300; }}
        </style>
    """, unsafe_allow_html=True)

    view = st.session_state.user['view']

    # --- VISTA HOME (CICLO) ---
    if view == 'Home':
        st.markdown(f"<h2 style='text-align:center;'>Bonjour, {st.session_state.user['nombre']}</h2>", unsafe_allow_html=True)
        fase = st.session_state.user['fase_actual']
        
        st.markdown(f"""
            <div class="dragon-circle">
                <img src="{ASSETS[st.session_state.user['elemento']][fase]}" width="150" style="filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));">
            </div>
            <h3 style="text-align:center; margin-top:20px;">{fase}</h3>
        """, unsafe_allow_html=True)
        
        st.caption(f"Niveau {st.session_state.user['nivel']} ({st.session_state.user['xp']}/{st.session_state.user['xp_next']} XP)")
        st.markdown('<div class="xp-container"><div class="xp-bar"></div></div>', unsafe_allow_html=True)

    # --- VISTA REGISTRO (CHECK-IN) ---
    elif view == 'Registro':
        st.title("Check-in 📝")
        with st.container(border=True):
            with st.form("checkin"):
                st.markdown("### 📥 Input")
                i = st.multiselect("He...", ["Música", "Video", "Lectura"], key="i")
                st.markdown("### 📤 Output")
                o = st.multiselect("He...", ["Hablar", "Escribir", "Grabar"], key="o")
                mood = st.select_slider("Energía", ["😴 Baja", "😐 Normal", "✨ Alta"])
                
                if st.form_submit_button("Guardar"):
                    # Cálculo simplificado de fase
                    new_phase = "Éveil"
                    if mood == "😴 Baja": new_phase = "Repli"
                    elif len(o) > len(i): new_phase = "Expansion"
                    elif len(i) > 0: new_phase = "Renouveau"
                    
                    st.session_state.user['fase_actual'] = new_phase
                    st.session_state.user['xp'] += (len(i)*10 + len(o)*15)
                    st.success(f"Fase: {new_phase}")
                    time.sleep(1)
                    st.session_state.user['view'] = 'Home'
                    st.rerun()

    # --- VISTA ARCADE (JUEGOS) ---
    elif view == 'Arcade':
        render_memory_game(tema['accent'])

    # --- MENÚ DOCK INFERIOR (3 OPCIONES) ---
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⭕ Inicio", use_container_width=True):
            st.session_state.user['view'] = 'Home'
            st.rerun()
    with c2:
        if st.button("➕ Entrenar", use_container_width=True):
            st.session_state.user['view'] = 'Registro'
            st.rerun()
    with c3:
        # Destacamos Arcade si hay juego pendiente
        btn_label = "🎮 Juegos"
        if st.button(btn_label, use_container_width=True, type="primary" if view == 'Arcade' else "secondary"):
            st.session_state.user['view'] = 'Arcade'
            st.rerun()
    
