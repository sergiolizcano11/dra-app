import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="App Dragonne", layout="centered", page_icon="🐉")

# --- 2. ESTILOS CSS "MOBILE APP" (iOS/Android Look) ---
st.markdown("""
    <style>
    /* RESET Y FONDO APP */
    .stApp {
        background-color: #F2F4F8; /* Gris azulado muy suave tipo iOS */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* MENÚ DE NAVEGACIÓN INFERIOR (FIXED BOTTOM BAR) */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 999;
        border-top: 1px solid #E5E5EA;
        padding: 10px 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
    }
    
    /* Ajuste para que el contenido no quede tapado por el menú */
    .block-container {
        padding-bottom: 100px;
        max-width: 600px; /* Ancho máximo tipo móvil */
    }

    /* TARJETAS (CARDS) */
    .app-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #F0F0F0;
    }

    /* CABECERAS Y TEXTO */
    h1, h2, h3 { color: #1C1C1E; }
    p, label { color: #3A3A3C; }
    
    /* BOTONES ESTILO APP */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        background-color: #007AFF; /* Azul iOS */
        color: white;
        border: none;
    }
    .stButton>button:hover { background-color: #0062CC; color: white; }

    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. ESTADO Y DATOS (Imágenes de Dragones) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'current_phase': 'Éveil', 
        'journal': [],
        'view': 'Inicio' # Controla qué pantalla vemos
    }

# URLs de Dragones para cada fase
DRAGONS = {
    "Éveil": {
        "img": "https://cdn-icons-png.flaticon.com/512/3232/3232717.png", # Huevo rompiéndose
        "color": "#34C759", # Verde iOS
        "title": "Phase 1: Éveil",
        "desc": "Tu observas. La curiosidad es tu guía."
    },
    "Expansion": {
        "img": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", # Dragón volando rojo
        "color": "#FF3B30", # Rojo iOS
        "title": "Phase 2: Expansion",
        "desc": "Tu actúas. Te atreves a hablar y crear."
    },
    "Repli": {
        "img": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", # Dragón azul durmiendo
        "color": "#5856D6", # Violeta iOS
        "title": "Phase 3: Repli",
        "desc": "Descanso necesario. Momento de reflexionar."
    },
    "Renouveau": {
        "img": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png", # Dragón dorado/majestuoso
        "color": "#FF9500", # Naranja iOS
        "title": "Phase 4: Renouveau",
        "desc": "Has integrado lo aprendido. Brillas con luz propia."
    }
}

# --- 4. FUNCIÓN DE MENÚ PERSONALIZADO ---
def mostrar_menu_inferior():
    # Usamos columnas para simular botones de app
    st.write("---") # Separador invisible al final
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Inicio"):
            st.session_state.user['view'] = 'Inicio'
            st.rerun()
    with col2:
        if st.button("📝 Diario"):
            st.session_state.user['view'] = 'Diario'
            st.rerun()
    with col3:
        if st.button("📜 Historial"):
            st.session_state.user['view'] = 'Historial'
            st.rerun()

# --- 5. VISTAS DE LA APLICACIÓN ---

# A. VISTA INICIO (EL DRAGÓN)
if st.session_state.user['view'] == 'Inicio':
    st.title("Ma Dragonne 🐉")
    
    # Selector de Fase (Tipo Dropdown App)
    phase_keys = list(DRAGONS.keys())
    current_index = phase_keys.index(st.session_state.user['current_phase'])
    
    st.caption("¿Cómo te sientes esta semana?")
    nueva_fase = st.selectbox("Selecciona tu fase:", phase_keys, index=current_index)
    
    if nueva_fase != st.session_state.user['current_phase']:
        st.session_state.user['current_phase'] = nueva_fase
        st.rerun()

    # DATOS DE LA FASE ACTUAL
    data = DRAGONS[st.session_state.user['current_phase']]
    
    # TARJETA DEL DRAGÓN (La parte visual potente)
    st.markdown(f"""
    <div class="app-card" style="text-align: center; border-top: 5px solid {data['color']};">
        <h2 style="color: {data['color']}; margin-top:0;">{data['title']}</h2>
        <p style="font-size: 1.1em; color: gray;">{data['desc']}</p>
        <img src="{data['img']}" width="200" style="margin: 20px 0;">
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Consejo: Si cambias la fase arriba, la imagen de tu dragona evolucionará contigo.")

# B. VISTA DIARIO (REGISTRO)
elif st.session_state.user['view'] == 'Diario':
    st.title("Nouveau Bilan 📝")
    
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    with st.form("entry_form"):
        st.subheader("1. Tu logro semanal")
        tipo = st.radio("¿Qué has trabajado?", ["🧠 Compréhension", "💬 Expression", "🌱 Effort"], horizontal=True)
        texto = st.text_area("Completa: 'Aujourd'hui j'ai...'", height=80)
        
        st.write("---")
        st.subheader("2. (Opcional) Dificultad")
        dificultad = st.text_input("Me costó trabajo...")
        
        submitted = st.form_submit_button("Guardar en mi Diario")
        if submitted:
            if texto:
                nuevo_registro = {
                    "fecha": datetime.now().strftime("%d/%m"),
                    "fase": st.session_state.user['current_phase'],
                    "tipo": tipo,
                    "texto": texto,
                    "dificultad": dificultad
                }
                st.session_state.user['journal'].insert(0, nuevo_registro)
                st.success("¡Guardado!")
                st.balloons()
            else:
                st.error("Escribe tu logro primero.")
    st.markdown('</div>', unsafe_allow_html=True)

# C. VISTA HISTORIAL (FEED)
elif st.session_state.user['view'] == 'Historial':
    st.title("Mes Traces 📜")
    
    if not st.session_state.user['journal']:
        st.markdown('<div class="app-card" style="text-align:center;">📭 Tu diario está vacío aún.</div>', unsafe_allow_html=True)
    
    for entry in st.session_state.user['journal']:
        color_borde = DRAGONS[entry['fase']]['color']
        img_mini = DRAGONS[entry['fase']]['img']
        
        st.markdown(f"""
        <div class="app-card" style="border-left: 5px solid {color_borde}; display: flex; align-items: center; gap: 15px;">
            <div style="text-align: center;">
                <img src="{img_mini}" width="40" style="border-radius: 50%;">
                <br><small>{entry['fecha']}</small>
            </div>
            <div>
                <h4 style="margin:0; color: {color_borde};">{entry['tipo']}</h4>
                <p style="margin: 5px 0 0 0;">"{entry['texto']}"</p>
                {f'<p style="color:red; font-size:0.8em; margin-top:5px;">☁️ {entry["dificultad"]}</p>' if entry['dificultad'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 6. RENDERIZAR MENÚ AL FINAL ---
# Esto hace que aparezca visualmente abajo gracias a CSS, pero lógica se ejecuta aquí.
mostrar_menu_inferior()
