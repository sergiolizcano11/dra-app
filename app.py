import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Dragonne - Journal d'Apprentissage", layout="centered", page_icon="🐉")

# --- 2. ESTILOS CSS (Visualización Calmada y No Competitiva) ---
st.markdown("""
    <style>
    /* Fondo que cambia sutilmente */
    .stApp {
        background: linear-gradient(180deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* Tarjetas de reflexión */
    .journal-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #6C63FF;
    }
    
    /* Estilos para las Fases */
    .phase-badge {
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        color: white;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Botones suaves */
    .stButton>button {
        border-radius: 20px;
        background-color: #f0f2f6;
        color: #31333F;
        border: 1px solid #d0d2d6;
    }
    .stButton>button:hover {
        border-color: #6C63FF;
        color: #6C63FF;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (La Memoria de la App) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Élève',
        'dragon_name': 'Lumière',
        'current_phase': 'Éveil', # Fase inicial
        'journal': [], # Historial de registros
        'stats': {'Compréhension': 0, 'Expression': 0, 'Effort': 0} # Contadores internos invisibles para cambiar forma
    }

# --- 4. LÓGICA DE LAS FASES Y EVOLUCIÓN ---
PHASES = {
    "Éveil": {
        "desc": "🌱 Curiosité et Observation", 
        "color": "#a8e6cf", 
        "msg": "Ta dragonne s'éveille. Elle observe le monde avec calme.",
        "icon": "https://cdn-icons-png.flaticon.com/512/3232/3232717.png" # Huevo/Bebé
    },
    "Expansion": {
        "desc": "🔥 Action et Courage", 
        "color": "#ffaaa5", 
        "msg": "Ta dragonne déploie ses ailes. Elle veut voler et s'exprimer.",
        "icon": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png" # Dragón Rojo/Fuego
    },
    "Repli": {
        "desc": "🌙 Pause et Réflexion", 
        "color": "#8aaae5", 
        "msg": "Ta dragonne se repose. Elle reprend des forces pour mieux comprendre.",
        "icon": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png" # Dragón Azul/Dormido o Huevo Azul
    },
    "Renouveau": {
        "desc": "✨ Intégration et Lumière", 
        "color": "#ffd3b6", 
        "msg": "Ta dragonne brille. Elle a compris et se sent prête pour la suite.",
        "icon": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png" # Dragón Dorado/Verde
    }
}

def guardar_entrada(tipo, texto, dificultad, emocion, mejora):
    # Guardamos la entrada
    entry = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "phase": st.session_state.user['current_phase'],
        "type": tipo,
        "text": texto,
        "difficulty": dificultad,
        "emotion": emocion,
        "improvement": mejora
    }
    st.session_state.user['journal'].insert(0, entry) # El más reciente primero
    
    # Evolución invisible (modifica sutilmente la dragona internamente)
    if tipo == "🧠 Compréhension": st.session_state.user['stats']['Compréhension'] += 1
    elif tipo == "💬 Expression": st.session_state.user['stats']['Expression'] += 1
    elif tipo == "🌱 Effort personnel": st.session_state.user['stats']['Effort'] += 1

# --- 5. INTERFAZ DE USUARIO ---

# --- CABECERA ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(f"🐉 {st.session_state.user['dragon_name']}")
with col_h2:
    # Selector de Fase (Metacognición: El alumno decide dónde está)
    st.caption("Mon Cycle Actuel")
    fase_seleccionada = st.selectbox(
        "Fase", 
        options=list(PHASES.keys()), 
        index=list(PHASES.keys()).index(st.session_state.user['current_phase']),
        label_visibility="collapsed"
    )
    if fase_seleccionada != st.session_state.user['current_phase']:
        st.session_state.user['current_phase'] = fase_seleccionada
        st.rerun()

# --- VISUALIZACIÓN DE LA DRAGONA (CENTRO DEL PROYECTO) ---
current_p_data = PHASES[st.session_state.user['current_phase']]

st.markdown(f"""
    <div style="background-color: {current_p_data['color']}; padding: 20px; border-radius: 20px; text-align: center; box-shadow: inset 0 0 20px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">{st.session_state.user['current_phase']}</h2>
        <p style="color: white; font-style: italic;">{current_p_data['desc']}</p>
    </div>
""", unsafe_allow_html=True)

col_img, col_txt = st.columns([1, 2])
with col_img:
    st.image(current_p_data['icon'], width=130)
with col_txt:
    st.info(f"🗨️ {current_p_data['msg']}")
    
    # Feedback Sutil basado en acumulado (Sin números)
    stats = st.session_state.user['stats']
    feedback_text = []
    if stats['Expression'] > stats['Compréhension']:
        feedback_text.append("Ses ailes semblent fortes (Expression).")
    if stats['Compréhension'] > stats['Expression']:
        feedback_text.append("Son regard est profond (Compréhension).")
    if stats['Effort'] > 2:
        feedback_text.append("Elle a une aura brillante (Effort).")
        
    if feedback_text:
        st.caption("Observations: " + " ".join(feedback_text))

st.divider()

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["📝 Journal Hebdo", "📖 Mon Histoire", "ℹ️ Le Projet"])

# --- TAB 1: REGISTRO SEMANAL (REFLEXIÓN) ---
with tab1:
    st.subheader("Bilan de la Semaine")
    with st.form("journal_form"):
        st.markdown("### 1. Qu'est-ce qui a brillé ? (Obligatoire)")
        tipo_avance = st.radio(
            "Choisis ton type d'avancée :",
            ["🧠 Compréhension (J'ai compris)", "💬 Expression (J'ai dit/écrit)", "🌱 Effort personnel (J'ai persévéré)"],
            horizontal=False
        )
        
        texto_avance = st.text_input(
            "Complète la phrase (en français) :",
            placeholder="Aujourd'hui j'ai compris que... / J'ai réussi à..."
        )
        
        st.markdown("---")
        st.markdown("### 2. Un nuage à dissiper ? (Optionnel)")
        
        tiene_dificultad = st.checkbox("Je veux noter une difficulté (pour m'améliorer)")
        dificultad_txt = ""
        emocion = ""
        intencion = ""
        
        if tiene_dificultad:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                dificultad_txt = st.text_input("J'ai eu du mal à...", placeholder="ex: prononcer le 'R'")
            with col_d2:
                emocion = st.select_slider("Je me suis senti(e)...", options=["😕", "😤", "😰", "😴"])
            
            intencion = st.text_input("La prochaine fois...", placeholder="ex: Je vais écouter l'audio deux fois")

        submit = st.form_submit_button("Enregistrer dans mon Journal")
        
        if submit:
            if len(texto_avance) > 3:
                guardar_entrada(tipo_avance.split(" ")[0] + " " + tipo_avance.split(" ")[1], texto_avance, dificultad_txt, emocion, intencion)
                st.balloons()
                st.success("C'est noté ! Ta dragonne intègre cette expérience.")
            else:
                st.error("N'oublie pas d'écrire ta phrase en français.")

# --- TAB 2: HISTORIA (VISUALIZACIÓN DEL PROCESO) ---
with tab2:
    st.subheader("Mes Traces")
    if not st.session_state.user['journal']:
        st.info("Ton journal est vide. Fais ton premier bilan !")
    
    for entry in st.session_state.user['journal']:
        # Estilo de tarjeta diferente según si hubo dificultad o no
        border_color = "#6C63FF" if not entry['difficulty'] else "#FFAAA5"
        
        st.markdown(f"""
        <div class="journal-card" style="border-left: 5px solid {border_color};">
            <small style="color: gray;">📅 {entry['date']} | Phase: <strong>{entry['phase']}</strong></small>
            <h4>{entry['type']}</h4>
            <p style="font-size: 1.1em; font-style: italic;">"{entry['text']}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        if entry['difficulty']:
            st.markdown(f"""
            <div style="margin-left: 20px; margin-bottom: 20px; padding: 10px; background-color: #fff0f0; border-radius: 10px;">
                <p><strong>☁️ Point à soigner:</strong> {entry['difficulty']} {entry['emotion']}</p>
                <p>👉 <em>Objectif: {entry['improvement']}</em></p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 3: FILOSOFÍA (PARA EL ALUMNO) ---
with tab3:
    st.markdown("""
    ### 🐉 Comment ça marche ?
    
    Cette application est ton **miroir d'apprentissage**. 
    
    1. **Pas de notes, pas de compétition.** Ta dragonne est unique.
    2. **Les Cycles (Phases) :** L'apprentissage n'est pas une ligne droite.
        - **🌱 Éveil :** Tu découvres, tu observes.
        - **🔥 Expansion :** Tu te lances, tu parles, tu écris !
        - **🌙 Repli :** C'est difficile ? C'est normal. On ralentit pour mieux comprendre.
        - **✨ Renouveau :** Tu as intégré, tu es prêt pour la suite.
    
    *C'est toi qui décides dans quelle phase tu te trouves en haut à droite.*
    """)
