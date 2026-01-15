import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN E IMITACIÓN DE "MUSA" UI ---
st.set_page_config(page_title="Mon Cycle Français", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    /* ESTÉTICA SOFT/CLEAN TIPO MUSA */
    .stApp {
        background-color: #FAFAFA; /* Blanco roto muy limpio */
    }
    
    /* EL CÍRCULO CENTRAL (Símbolo del ciclo) */
    .cycle-ring {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 8px solid white;
        background: white;
        position: relative;
    }
    
    /* TEXTOS */
    h1, h2, h3 { color: #4A4A4A; font-family: 'Helvetica', sans-serif; font-weight: 300; }
    .subtitle { color: #9B9B9B; font-size: 0.9em; text-align: center; }
    
    /* BOTONES DE SÍNTOMAS (Tags redondeados) */
    div[data-baseweb="select"] > div {
        border-radius: 20px !important;
        background-color: #F0F2F6;
        border: none;
    }
    
    /* MENÚ INFERIOR FLOTANTE */
    .nav-bar {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        padding: 10px 30px;
        border-radius: 50px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        display: flex;
        gap: 40px;
        z-index: 999;
    }
    
    /* OCULTAR COSAS DEFAULT */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. BASE DE CONOCIMIENTO (SÍNTOMAS Y FASES) ---
# Aquí conectamos "Cómo me siento" con "En qué fase estoy"
SENSACIONES = {
    "Curieux 🧐": "Éveil",
    "Motivé 🚀": "Éveil",
    "Bavard 🗣️": "Expansion",
    "Créatif 🎨": "Expansion",
    "Confiant 😎": "Expansion",
    "Fatigué 😴": "Repli",
    "Perdu 🌫️": "Repli",
    "Bloqué 🧱": "Repli",
    "Calme 🧘": "Renouveau",
    "Satisfait ✅": "Renouveau"
}

FASES_DATA = {
    "Éveil": {
        "color": "linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%)", # Verdes suaves
        "consejo": "Hoy es buen día para escuchar y absorber vocabulario nuevo.",
        "img": "https://cdn-icons-png.flaticon.com/512/3232/3232717.png"
    },
    "Expansion": {
        "color": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)", # Rosas enérgicos
        "consejo": "¡Tienes la energía alta! Atrévete a participar en clase.",
        "img": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png"
    },
    "Repli": {
        "color": "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)", # Violetas calmados
        "consejo": "No te fuerces. Revisa tus apuntes tranquilamente.",
        "img": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png"
    },
    "Renouveau": {
        "color": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)", # Naranjas cálidos
        "consejo": "Organiza lo aprendido. Estás integrando el conocimiento.",
        "img": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png"
    }
}

# --- 3. ESTADO DEL USUARIO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'fase_actual': 'Éveil',
        'diario': [],
        'view': 'Ciclo'
    }

# --- 4. INTERFAZ PRINCIPAL ---

# A. PANTALLA DEL CICLO (HOME)
if st.session_state.user['view'] == 'Ciclo':
    fase = st.session_state.user['fase_actual']
    data = FASES_DATA[fase]
    
    # 1. Cabecera limpia
    st.markdown(f"<h3 style='text-align: center;'>Bonjour, Éleve</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>Tu es en phase <strong>{fase}</strong></p>", unsafe_allow_html=True)
    
    # 2. El Círculo Visual (La "Rueda" de MUSA)
    st.markdown(f"""
        <div class="cycle-ring" style="background: {data['color']};">
            <img src="{data['img']}" width="120">
        </div>
    """, unsafe_allow_html=True)
    
    # 3. El Consejo del Día (Tipo "Health Tip")
    st.write("")
    st.info(f"💡 **Conseil du jour:** {data['consejo']}")
    
    # 4. Botón de Acción Principal (El "+" de MUSA)
    st.write("")
    st.markdown("<p style='text-align: center; color: gray;'>¿Cómo sientes tu francés hoy?</p>", unsafe_allow_html=True)
    
    if st.button("Registrar mis sensaciones hoy (+)", type="primary"):
        st.session_state.user['view'] = 'Registro'
        st.rerun()

# B. PANTALLA DE REGISTRO (CHECK-IN)
elif st.session_state.user['view'] == 'Registro':
    st.markdown("<h2 style='text-align: center;'>Check-in Diario</h2>", unsafe_allow_html=True)
    
    # Formulario "Symptom Tracking"
    with st.container(border=True):
        st.write("Selecciona tus sensaciones de aprendizaje:")
        
        # Tags seleccionables
        sensaciones_seleccionadas = st.multiselect(
            "¿Qué sientes hoy?",
            list(SENSACIONES.keys()),
            placeholder="Selecciona palabras clave..."
        )
        
        nota = st.text_area("Nota personal (Opcional):", height=80)
        
        if st.button("Guardar Registro"):
            if sensaciones_seleccionadas:
                # ALGORITMO: Determinamos la fase según la mayoría de sensaciones
                conteo_fases = {}
                for s in sensaciones_seleccionadas:
                    f_sugerida = SENSACIONES[s]
                    conteo_fases[f_sugerida] = conteo_fases.get(f_sugerida, 0) + 1
                
                # La fase con más votos gana (si hay empate, se queda la primera)
                nueva_fase = max(conteo_fases, key=conteo_fases.get)
                st.session_state.user['fase_actual'] = nueva_fase
                
                # Guardar en historial
                entry = {
                    "fecha": datetime.now().strftime("%d/%m"),
                    "sensaciones": ", ".join(sensaciones_seleccionadas),
                    "fase": nueva_fase,
                    "nota": nota
                }
                st.session_state.user['diario'].insert(0, entry)
                
                st.success(f"Ciclo actualizado: Ahora estás en {nueva_fase}")
                time.sleep(1.5)
                st.session_state.user['view'] = 'Ciclo'
                st.rerun()
            else:
                st.warning("Selecciona al menos una sensación.")
        
        if st.button("Cancelar", type="secondary"):
            st.session_state.user['view'] = 'Ciclo'
            st.rerun()

# C. PANTALLA CALENDARIO/HISTORIAL
elif st.session_state.user['view'] == 'Historial':
    st.markdown("<h2 style='text-align: center;'>Mi Calendario</h2>", unsafe_allow_html=True)
    
    for item in st.session_state.user['diario']:
        color_borde = FASES_DATA[item['fase']]['color']
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid gray; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <small>{item['fecha']} | <strong>{item['fase']}</strong></small><br>
            <span style="font-size: 1.1em;">{item['sensaciones']}</span>
            <p style="color: gray; font-size: 0.9em; margin-top: 5px;"><em>{item['nota']}</em></p>
        </div>
        """, unsafe_allow_html=True)

# --- 5. MENÚ DE NAVEGACIÓN FLOTANTE (ESTILO APP NATIVA) ---
import time

col1, col2, col3 = st.columns(3)
# Usamos un contenedor fijo con CSS, pero necesitamos botones de Streamlit para la lógica
# Truco: Ponemos los botones al final de la página normal, pero el CSS 'nav-bar' visualmente no funciona con botones directos de streamlit fácilmente sin componentes extra.
# Usaremos columnas normales de Streamlit abajo del todo para simular el dock.

st.write("---")
c1, c2, c3 = st.columns([1,1,1])

with c1:
    if st.button("⭕ Ciclo"):
        st.session_state.user['view'] = 'Ciclo'
        st.rerun()
with c2:
    if st.button("➕ Registro"):
        st.session_state.user['view'] = 'Registro'
        st.rerun()
with c3:
    if st.button("📅 Historial"):
        st.session_state.user['view'] = 'Historial'
        st.rerun()
