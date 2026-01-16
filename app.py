import streamlit as st
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN E INYECCIÓN CSS (ESTILO APP MÓVIL MUSA) ---
st.set_page_config(page_title="Mon Cycle Français", layout="centered", page_icon="🐉")

# Colores suaves estilo wellness
TEMAS = {
    # Fuego: Tonos salmón/coral suaves en vez de rojo agresivo
    "Fuego": {"bg": "#FFF0EE", "accent": "#FF867C", "gradient": "linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 100%)"},
    # Agua: Tonos azul cielo/menta suaves
    "Agua":  {"bg": "#E3F2FD", "accent": "#64B5F6", "gradient": "linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)"},
    # Naturaleza: Tonos verde salvia/lima suaves
    "Naturaleza": {"bg": "#E8F5E9", "accent": "#81C784", "gradient": "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)"}
}

st.markdown("""
    <style>
    /* RESET Y TIPOGRAFÍA LIMPIA */
    .stApp {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #4A4A4A; /* Texto gris oscuro suave */
    }
    
    /* BARRA DE PROGRESO (XP) MINIMALISTA */
    .xp-container {
        width: 100%;
        background-color: #F0F0F0;
        border-radius: 20px; /* Más redondeado */
        margin: 15px 0;
        height: 8px;
        overflow: hidden;
    }
    .xp-bar {
        height: 100%;
        border-radius: 20px;
        transition: width 0.6s cubic-bezier(0.4, 0.0, 0.2, 1); /* Animación suave */
    }
    
    /* EL CÍRCULO CENTRAL (TIPO MUSA) */
    .dragon-circle {
        width: 260px;
        height: 260px;
        border-radius: 50%;
        margin: 30px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        /* Sombra muy suave y difuminada */
        box-shadow: 0 20px 40px rgba(0,0,0,0.08); 
        border: 10px solid white;
        background: white;
        position: relative;
        transition: all 0.5s ease;
    }
    
    /* TARJETAS DE CONSEJO LIMPIAS */
    .advice-card {
        background-color: white;
        border-radius: 25px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid rgba(0,0,0,0.02);
    }
    
    /* MENÚ DOCK INFERIOR */
    .dock {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.95); /* Ligeramente transparente */
        backdrop-filter: blur(10px); /* Efecto cristal */
        padding: 15px 0;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        z-index: 999;
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    
    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = {}

valores_por_defecto = {
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

for key, val in valores_por_defecto.items():
    if key not in st.session_state.user:
        st.session_state.user[key] = val

# --- 3. BIBLIOTECA DE IMÁGENES (¡AQUÍ PEGAS TUS ENLACES!) ---
# INSTRUCCIONES:
# Sustituye los enlaces de Flaticon por los enlaces de tus imágenes generadas por IA.
# Asegúrate de que sean enlaces directos a la imagen (deben terminar en .png o .jpg).

ASSETS = {
    "Fuego": {
        # Fase 1: El Huevo o Bebé suave
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880228.png", # <-- ¡CAMBIA ESTE ENLACE!
        # Fase 2: Volando / Activo (Output)
        "Expansion": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", # <-- ¡CAMBIA ESTE ENLACE!
        # Fase 3: Durmiendo / Hecho una bolita (Bloqueo)
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203150.png", # <-- ¡CAMBIA ESTE ENLACE! (He puesto uno durmiendo)
        # Fase 4: Majestuoso / Equilibrado
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699313.png" # <-- ¡CAMBIA ESTE ENLACE!
    },
    "Agua": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", # <-- ¡CAMBIA ESTE!
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3093/3093608.png", # <-- ¡CAMBIA ESTE!
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203158.png", # <-- ¡CAMBIA ESTE! (Durmiendo)
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699298.png" # <-- ¡CAMBIA ESTE!
    },
    "Naturaleza": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880233.png", # <-- ¡CAMBIA ESTE!
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png", # <-- ¡CAMBIA ESTE!
        "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203164.png", # <-- ¡CAMBIA ESTE! (Durmiendo)
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699276.png" # <-- ¡CAMBIA ESTE!
    }
}

# --- 4. ONBOARDING (ELECCIÓN SUAVE) ---
if not st.session_state.user['setup_complete']:
    st.title("Bienvenue ✨")
    st.write("Elige el compañero que mejor represente tu energía para aprender francés.")
    
    st.write("<br>", unsafe_allow_html=True) # Espacio
    
    col1, col2, col3 = st.columns(3)
    # Usamos los iconos de la fase "Éveil" (Huevo/Bebé) para elegir
    with col1:
        st.image(ASSETS["Fuego"]["Éveil"], width=80)
        if st.button("Passion (Fuego)"):
            st.session_state.user['elemento'] = "Fuego"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col2:
        st.image(ASSETS["Agua"]["Éveil"], width=80)
        if st.button("Calme (Agua)"):
            st.session_state.user['elemento'] = "Agua"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col3:
        st.image(ASSETS["Naturaleza"]["Éveil"], width=80)
        if st.button("Force (Tierra)"):
            st.session_state.user['elemento'] = "Naturaleza"
            st.session_state.user['setup_complete'] = True
            st.rerun()

# --- 5. APP PRINCIPAL ---
else:
    # Recuperamos tema visual del usuario
    tema = TEMAS[st.session_state.user['elemento']]
    
    # Inyectamos el color de fondo personalizado y suave
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {tema['bg']}; }}
        .xp-bar {{ background: {tema['gradient']}; width: {(st.session_state.user['xp'] / st.session_state.user['xp_next']) * 100}%; }}
        .dragon-circle {{ background: {tema['gradient']}; }}
        h1, h2, h3 {{ color: {tema['accent']}; font-weight: 300; }}
        .big-phase-text {{ color: {tema['accent']}; font-size: 1.5em; font-weight: 500; margin-top:15px; }}
        </style>
    """, unsafe_allow_html=True)

    # --- VISTA: HOME (EL CÍRCULO CENTRAL) ---
    if st.session_state.user['view'] == 'Home':
        
        st.markdown(f"<h2 style='text-align:center;'>Bonjour, {st.session_state.user['nombre']}</h2>", unsafe_allow_html=True)
        
        # 1. EL CÍRCULO DEL DRAGÓN (Elemento central tipo MUSA)
        fase = st.session_state.user['fase_actual']
        img_url = ASSETS[st.session_state.user['elemento']][fase]
        
        # Textos de fase más amigables
        fase_display = {
            "Éveil": "Mode Éponge (Curiosité)",
            "Expansion": "Mode Feu (Action)",
            "Repli": "Mode Doux (Repos)",
            "Renouveau": "Mode Lumière (Intégration)"
        }.get(fase, fase)
        
        st.markdown(f"""
            <div class="dragon-circle">
                <img src="{img_url}" width="150" style="filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); transition: transform 0.5s ease-in-out;">
            </div>
            <p style="text-align:center;" class="big-phase-text">{fase_display}</p>
        """, unsafe_allow_html=True)

        # 2. BARRA DE PROGRESO SUTIL
        st.write("<br>", unsafe_allow_html=True)
        st.caption(f"Progression Niveau {st.session_state.user['nivel']} ({st.session_state.user['xp']}/{st.session_state.user['xp_next']} XP)")
        st.markdown('<div class="xp-container"><div class="xp-bar"></div></div>', unsafe_allow_html=True)

        # 3. TARJETA DE CONSEJO (Pedagogía)
        st.write("<br>", unsafe_allow_html=True)
        consejo = ""
        if fase == "Éveil": consejo = "Hoy tu cerebro absorbe como una esponja. Es el día perfecto para escuchar música o podcasts en francés sin presión."
        elif fase == "Expansion": consejo = "¡Tienes mucha energía creativa hoy! Atrévete a hablar en clase o escribir esa frase difícil. Es tu momento."
        elif fase == "Repli": consejo = "Es normal sentirse bloqueado. No fuerces la máquina. Relee algo sencillo y descansa, mañana será otro día."
        elif fase == "Renouveau": consejo = "Has superado dificultades y estás integrando lo aprendido. Siéntete orgulloso de tu constancia."

        st.markdown(f"""
            <div class="advice-card">
                <strong style="color:{tema['accent']};">💡 Conseil du jour</strong><br><br>
                {consejo}
            </div>
        """, unsafe_allow_html=True)
        
    # --- VISTA: REGISTRO (CHECK-IN DIARIO) ---
    elif st.session_state.user['view'] == 'Registro':
        st.markdown(f"<h2 style='text-align:center;'>Check-in du jour 📝</h2>", unsafe_allow_html=True)
        st.caption("¿Cómo has conectado con el francés hoy?")
        
        with st.container(border=True):
            with st.form("training_form"):
                st.markdown("### 🌱 Input (Lo que recibí)")
                inputs = st.multiselect("He...", ["Escuchado música", "Visto video/serie", "Leído un texto", "Atendido al profe"], key="in")
            
                st.write("<br>", unsafe_allow_html=True)
                st.markdown("### 🔥 Output (Lo que produje)")
                outputs = st.multiselect("He...", ["Hablado en clase", "Grabado un audio", "Escrito frases", "Practicado pronunciación"], key="out")
            
                st.write("<br>", unsafe_allow_html=True)
                st.markdown("### 🧠 Sensación")
                mood = st.select_slider("Me siento...", options=["😴 Bloqueado/Cansado", "😐 Normal", "✨ Motivado/Creativo"])
            
                submit = st.form_submit_button("Guardar mi día", use_container_width=True)
            
                if submit:
                    # CÁLCULO DE FASE PEDAGÓGICA (Algoritmo MUSA)
                    nueva_fase = "Éveil" # Por defecto
                    
                    if mood == "😴 Bloqueado/Cansado":
                        nueva_fase = "Repli" # Priorizamos el descanso si se siente mal
                    elif len(outputs) > len(inputs) and mood == "✨ Motivado/Creativo":
                        nueva_fase = "Expansion" # Mucha acción y energía
                    elif len(inputs) >= len(outputs) and mood != "😴 Bloqueado/Cansado":
                        nueva_fase = "Éveil" # Más absorción que acción
                    else:
                        nueva_fase = "Renouveau" # Equilibrio
                        
                    st.session_state.user['fase_actual'] = nueva_fase

                    # CÁLCULO DE XP (Gamificación suave)
                    xp_ganada = (len(inputs) * 10) + (len(outputs) * 15) + 5
                    st.session_state.user['xp'] += xp_ganada
                    if st.session_state.user['xp'] >= st.session_state.user['xp_next']:
                        st.session_state.user['nivel'] += 1
                        st.session_state.user['xp'] = 0
                        st.session_state.user['xp_next'] = int(st.session_state.user['xp_next'] * 1.15)
                        st.balloons()
                    
                    st.success(f"✨ Ciclo actualizado a: {nueva_fase}")
                    time.sleep(1.5)
                    st.session_state.user['view'] = 'Home'
                    st.rerun()

    # --- MENÚ DOCK INFERIOR (NAVEGACIÓN) ---
    st.write("<br><br><br>", unsafe_allow_html=True) # Espacio para el menú
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⭕ Mi Ciclo", use_container_width=True):
            st.session_state.user['view'] = 'Home'
            st.rerun()
    with c2:
        # Usamos un estilo diferente para el botón de acción principal
        if st.button("➕ Check-in", use_container_width=True, type="primary"):
            st.session_state.user['view'] = 'Registro'
            st.rerun()
