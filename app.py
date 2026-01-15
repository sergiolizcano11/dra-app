import streamlit as st
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN VISUAL (ESTÉTICA TIPO MUSA) ---
st.set_page_config(page_title="Ma Dragonne Français", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    /* FONDO Y TIPOGRAFÍA LIMPIA */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* EL CÍRCULO CENTRAL (EL CORAZÓN DE LA APP) */
    .dragon-ring {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        margin: 20px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 6px solid white;
        background: white;
        transition: all 0.5s ease;
    }
    
    /* TEXTOS */
    h1 { color: #2D3436; font-weight: 700; font-size: 1.8rem; text-align: center; }
    p { color: #636E72; text-align: center; }
    
    /* BOTONES DE ACTIVIDAD (TAGS) */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
    }
    
    /* TARJETAS DE CONSEJO */
    .advice-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #6C5CE7;
    }

    /* MENÚ FLOTANTE INFERIOR */
    .dock-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 15px 0;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        z-index: 1000;
    }
    
    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. LÓGICA PEDAGÓGICA (NO BIOLÓGICA) ---

# FASES DEL APRENDIZAJE (LOS ESTADOS DE LA DRAGONA)
FASES = {
    "Éveil": { # Fase de entrada / pasiva
        "color": "linear-gradient(135deg, #55efc4 0%, #00b894 100%)", # Verde Mentar
        "img": "https://cdn-icons-png.flaticon.com/512/3232/3232717.png", # Huevo/Bebé
        "titulo": "Mode Éponge",
        "desc": "Estás absorbiendo información. Escucha y lee."
    },
    "Expansion": { # Fase de salida / activa
        "color": "linear-gradient(135deg, #ff7675 0%, #d63031 100%)", # Rojo Coral
        "img": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", # Dragón Volando
        "titulo": "Mode Feu",
        "desc": "Estás produciendo. ¡Habla sin miedo al error!"
    },
    "Repli": { # Fase de bloqueo / descanso
        "color": "linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)", # Azul
        "img": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", # Dragón Dormido
        "titulo": "Mode Grotte",
        "desc": "El cerebro necesita descanso para consolidar."
    }
}

# --- 3. ESTADO DE SESIÓN (ROBUSTO / AUTO-REPARABLE) ---
if 'user' not in st.session_state:
    st.session_state.user = {}

# Verificamos clave por clave. Si falta alguna (porque vienes de una versión vieja), la crea.
defaults = {
    'view': 'Home',
    'fase_actual': 'Éveil',
    'historial': []
}

for key, value in defaults.items():
    if key not in st.session_state.user:
        st.session_state.user[key] = value

# --- 4. VISTAS DE LA APP ---

# A. HOME (EL CÍRCULO PRINCIPAL)
if st.session_state.user['view'] == 'Home':
    fase_actual = st.session_state.user['fase_actual']
    datos_fase = FASES[fase_actual]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h1>Bonjour, Apprenti 🎓</h1>", unsafe_allow_html=True)
    
    # EL CÍRCULO VISUAL (Visualización del estado actual)
    st.markdown(f"""
        <div class="dragon-ring" style="background: {datos_fase['color']};">
            <img src="{datos_fase['img']}" width="130" style="filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2));">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h3>{datos_fase['titulo']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>{datos_fase['desc']}</p>", unsafe_allow_html=True)
    
    # CONSEJO PEDAGÓGICO AUTOMÁTICO
    st.markdown(f"""
    <div class="advice-card">
        <strong>💡 Conseil du jour:</strong><br>
        {"Si hoy solo escuchas música en francés, ya estás sumando." if fase_actual == 'Éveil' else 
         "Aprovecha esta energía para grabar un audio o hablar en clase." if fase_actual == 'Expansion' else 
         "No te frustres. Relee vocabulario antiguo y descansa."}
    </div>
    """, unsafe_allow_html=True)

    # BOTÓN DE ACCIÓN PRINCIPAL (Check-in)
    st.write("")
    if st.button("➕ Registrar Actividad de Hoy", type="primary", use_container_width=True):
        st.session_state.user['view'] = 'Registro'
        st.rerun()

# B. REGISTRO (INPUT DE DATOS)
elif st.session_state.user['view'] == 'Registro':
    st.markdown("<h1>Qu'as-tu fait ? 🇫🇷</h1>", unsafe_allow_html=True)
    st.caption("Selecciona tus interacciones con el francés hoy:")
    
    with st.form("checkin_form"):
        # Categorías pedagógicas claras
        st.markdown("**👂 Input (Lo que recibí)**")
        input_tags = st.multiselect("He...", ["Escuchado música", "Visto una serie/video", "Leído un texto", "Escuchado al profe"], key="input")
        
        st.markdown("**🗣️ Output (Lo que produje)**")
        output_tags = st.multiselect("He...", ["Hablado en clase", "Escrito una frase/texto", "Cantado", "Repetido pronunciación"], key="output")
        
        st.markdown("**🧠 Sensación (Cómo me sentí)**")
        mood = st.select_slider("", options=["😫 Bloqueado", "😐 Normal", "🙂 Bien", "🤩 ¡Top!"], value="😐 Normal")
        
        submitted = st.form_submit_button("Guardar mi día", use_container_width=True)
        
        if submitted:
            # LÓGICA DE DETERMINACIÓN DE FASE
            # Si hay más output -> Expansion. Si hay más input -> Éveil. Si hay bloqueo -> Repli.
            nueva_fase = "Éveil" # Por defecto
            
            if "😫 Bloqueado" in mood:
                nueva_fase = "Repli"
            elif len(output_tags) >= len(input_tags) and len(output_tags) > 0:
                nueva_fase = "Expansion"
            else:
                nueva_fase = "Éveil"
                
            # Guardar
            registro = {
                "fecha": datetime.now().strftime("%d/%m"),
                "fase": nueva_fase,
                "resumen": f"{len(input_tags)} Inputs / {len(output_tags)} Outputs",
                "mood": mood
            }
            st.session_state.user['historial'].insert(0, registro)
            st.session_state.user['fase_actual'] = nueva_fase
            
            st.success("¡Registro completado!")
            time.sleep(1)
            st.session_state.user['view'] = 'Home'
            st.rerun()
            
    if st.button("Cancelar"):
        st.session_state.user['view'] = 'Home'
        st.rerun()

# C. HISTORIAL (CALENDARIO)
elif st.session_state.user['view'] == 'Historial':
    st.markdown("<h1>Mon Calendrier 📅</h1>", unsafe_allow_html=True)
    
    if not st.session_state.user['historial']:
        st.info("Aún no hay registros. ¡Empieza hoy!")
    
    for item in st.session_state.user['historial']:
        color = FASES[item['fase']]['color']
        st.markdown(f"""
        <div style="background:white; border-radius:15px; padding:15px; margin-bottom:10px; border-left: 6px solid gray; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display:flex; justify-content:space-between; align-items:center;">
            <div>
                <strong style="color:#2D3436;">{item['fecha']}</strong><br>
                <small style="color:gray;">{item['resumen']}</small>
            </div>
            <div style="text-align:right;">
                <span style="background: #f1f2f6; padding: 5px 10px; border-radius: 10px; font-size: 0.8em;">{item['fase']}</span><br>
                <span style="font-size:1.2em;">{item['mood'].split(' ')[0]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 5. MENÚ DE NAVEGACIÓN INFERIOR (Dock Falso) ---
st.write("<br><br><br>", unsafe_allow_html=True) # Espacio para que no tape contenido

# Usamos columnas de Streamlit al final para simular la barra
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Inicio"):
        st.session_state.user['view'] = 'Home'
        st.rerun()
with col2:
    if st.button("➕ Check-in"):
        st.session_state.user['view'] = 'Registro'
        st.rerun()
with col3:
    if st.button("📜 Diario"):
        st.session_state.user['view'] = 'Historial'
        st.rerun()
