import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN INICIAL Y CSS AVANZADO ---
st.set_page_config(page_title="L'Odyssée du Dragon", layout="centered", page_icon="🐉")

# Inyección de CSS para transformar Streamlit en una "App Móvil"
st.markdown("""
    <style>
    /* Fondo general con degradado suave */
    .stApp {
        background: linear-gradient(180deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Contenedores tipo Tarjeta (Card UI) */
    .css-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #f0f0f0;
    }
    
    /* Botones estilo App */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 50px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Colores dinámicos para botones */
    .primary-btn { background-color: #6C63FF; color: white; }
    
    /* Títulos centrados */
    h1, h2, h3 { text-align: center; color: #2C3E50; }
    
    /* Ocultar menú hamburguesa estándar para limpieza */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO (BASE DE DATOS EN MEMORIA) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'setup_complete': False,
        'name': '',
        'dragon': {
            'name': '',
            'element': '', # feu, eau, nature
            'stage': 0, # 0: Huevo, 1: Bebé, 2: Joven, 3: Maestro
            'xp': 0,
            'lvl': 1,
            'energy': 100 # Barra de energía
        },
        'inventory': [],
        'history': [] # Registro de respuestas para el profesor
    }

# --- 3. RECURSOS: IMÁGENES Y PREGUNTAS ---
# Diccionario de Assets (URLs estables)
ASSETS = {
    'egg': {
        'feu': 'https://cdn-icons-png.flaticon.com/512/7880/7880228.png', # Rojo/Dorado
        'eau': 'https://cdn-icons-png.flaticon.com/512/7880/7880222.png', # Azul/Escamas
        'nature': 'https://cdn-icons-png.flaticon.com/512/7880/7880233.png' # Verde/Hojas
    },
    'dragon': {
        'feu': ['https://cdn-icons-png.flaticon.com/512/4699/4699313.png', 'https://cdn-icons-png.flaticon.com/512/1625/1625348.png'],
        'eau': ['https://cdn-icons-png.flaticon.com/512/4699/4699298.png', 'https://cdn-icons-png.flaticon.com/512/3093/3093608.png'],
        'nature': ['https://cdn-icons-png.flaticon.com/512/4699/4699276.png', 'https://cdn-icons-png.flaticon.com/512/3715/3715097.png']
    }
}

# Banco de Preguntas (Sistema complejo)
QUESTIONS = [
    {"id": 1, "type": "choice", "q": "Complète la phrase: 'Hier, je ___ allé au cinéma.'", "options": ["suis", "ai", "as"], "ans": "suis", "exp": "Verbe aller utilise l'auxiliaire 'être' au passé composé."},
    {"id": 2, "type": "text", "q": "Traduis en français: 'The red car'.", "ans": ["la voiture rouge", "une voiture rouge"], "exp": "Adjectif de couleur après le nom."},
    {"id": 3, "type": "bool", "q": "Vrai ou Faux: 'Le fromage' est féminin.", "options": ["Vrai", "Faux"], "ans": "Faux", "exp": "C'est masculin: LE fromage."},
    {"id": 4, "type": "choice", "q": "Quel mot n'appartient pas à la famille? (L'intrus)", "options": ["Pomme", "Banane", "Chaise", "Orange"], "ans": "Chaise", "exp": "Les autres sont des fruits."},
]

# --- 4. FUNCIONES DEL SISTEMA ---
def level_up_check():
    xp_needed = st.session_state.user['dragon']['lvl'] * 50
    if st.session_state.user['dragon']['xp'] >= xp_needed:
        st.session_state.user['dragon']['lvl'] += 1
        st.session_state.user['dragon']['xp'] -= xp_needed
        st.balloons()
        st.toast(f"🎉 Niveau Supérieur! Niveau {st.session_state.user['dragon']['lvl']} atteint!", icon="🆙")
        # Evolución visual
        if st.session_state.user['dragon']['lvl'] == 3:
            st.session_state.user['dragon']['stage'] = 1
        elif st.session_state.user['dragon']['lvl'] == 5:
            st.session_state.user['dragon']['stage'] = 2

def get_dragon_image():
    dragon = st.session_state.user['dragon']
    if dragon['stage'] == 0:
        return ASSETS['egg'][dragon['element']]
    else:
        # Usa índice 0 para bebé, 1 para adulto (lógica simplificada)
        idx = 0 if dragon['stage'] == 1 else 1
        return ASSETS['dragon'][dragon['element']][idx]

# --- 5. INTERFAZ DE USUARIO (VISTAS) ---

# --- A. ONBOARDING (Creación del Dragón) ---
if not st.session_state.user['setup_complete']:
    st.markdown("<h1>🥚 L'Écloserie Magique</h1>", unsafe_allow_html=True)
    st.write("Bienvenue, élève. Pour commencer ton aventure en français, choisis ton œuf.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(ASSETS['egg']['feu'], width=100)
        if st.button("FEU (Courage)"):
            st.session_state.user['dragon']['element'] = 'feu'
            st.session_state.user['dragon']['name'] = "Ignis"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col2:
        st.image(ASSETS['egg']['eau'], width=100)
        if st.button("EAU (Sagesse)"):
            st.session_state.user['dragon']['element'] = 'eau'
            st.session_state.user['dragon']['name'] = "Aqua"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col3:
        st.image(ASSETS['egg']['nature'], width=100)
        if st.button("TERRE (Force)"):
            st.session_state.user['dragon']['element'] = 'nature'
            st.session_state.user['dragon']['name'] = "Terra"
            st.session_state.user['setup_complete'] = True
            st.rerun()

# --- B. DASHBOARD PRINCIPAL ---
else:
    # Sidebar de Navegación Estilizada
    with st.sidebar:
        st.title(f"🏰 Menu")
        menu = st.radio("", ["Mon Dragon", "Entraînement (Quiz)", "Journal (Feedback)", "Zone Professeur"])
        
        st.divider()
        st.caption("Statistiques Rapides")
        st.write(f"🏷️ Nom: **{st.session_state.user['dragon']['name']}**")
        st.write(f"⚡ Énergie: {st.session_state.user['dragon']['energy']}%")

    # --- VISTA: MON DRAGON ---
    if menu == "Mon Dragon":
        st.markdown(f"<h1>Antre de {st.session_state.user['dragon']['name']}</h1>", unsafe_allow_html=True)
        
        # Tarjeta principal del Dragón
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        col_img, col_stats = st.columns([1, 2])
        
        with col_img:
            st.image(get_dragon_image(), use_container_width=True)
            st.caption(f"Élément: {st.session_state.user['dragon']['element'].capitalize()}")
            
        with col_stats:
            lvl = st.session_state.user['dragon']['lvl']
            xp = st.session_state.user['dragon']['xp']
            xp_next = lvl * 50
            
            st.metric("Niveau Actuel", f"Lvl {lvl}")
            st.write(f"**Progression XP ({xp}/{xp_next})**")
            st.progress(min(xp / xp_next, 1.0))
            
            if st.session_state.user['dragon']['energy'] < 30:
                st.warning("⚠️ Ton dragon est fatigué ! Fais un quiz pour gagner de l'énergie.")
            else:
                st.success("Tu es prêt pour apprendre !")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VISTA: ENTRAÎNEMENT (QUIZ COMPLEJO) ---
    elif menu == "Entraînement (Quiz)":
        st.markdown("<h1>⚔️ Arène de Connaissance</h1>", unsafe_allow_html=True)
        
        # Seleccionar pregunta aleatoria
        q = random.choice(QUESTIONS)
        
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("Question:")
        st.markdown(f"### {q['q']}")
        
        user_ans = None
        check = False
        
        # Renderizado según tipo de pregunta
        if q['type'] == 'choice' or q['type'] == 'bool':
            user_ans = st.radio("Choisis la bonne réponse:", q['options'], index=None)
            check = st.button("Valider la réponse")
        elif q['type'] == 'text':
            user_ans = st.text_input("Écris ta réponse ici:")
            check = st.button("Valider la réponse")
            
        if check:
            is_correct = False
            # Lógica de validación
            if q['type'] == 'text':
                if user_ans.lower().strip() in [a.lower() for a in q['ans']]:
                    is_correct = True
            else:
                if user_ans == q['ans']:
                    is_correct = True
            
            # Resultado
            if is_correct:
                st.success("✅ Excellent ! Bonne réponse.")
                st.write(f"💡 *{q['exp']}*")
                # Recompensa
                st.session_state.user['dragon']['xp'] += 20
                st.session_state.user['dragon']['energy'] = min(100, st.session_state.user['dragon']['energy'] + 10)
                level_up_check()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Aïe... essaie encore !")
                st.session_state.user['dragon']['energy'] = max(0, st.session_state.user['dragon']['energy'] - 5)
                st.info(f"Indice: La réponse contient {len(str(q['ans']))} caractères/mots.")
                
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VISTA: JOURNAL (DUA / EMOCIONAL) ---
    elif menu == "Journal (Feedback)":
        st.markdown("<h1>🧠 Mon Journal de Bord</h1>", unsafe_allow_html=True)
        
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.write("Pour apprendre, il faut se sentir bien. Comment ça va ?")
        
        mood = st.select_slider("", options=["😫", "😕", "😐", "🙂", "🤩"], value="😐")
        tags = st.multiselect("Je me sens...", ["Motivé", "Fatigué", "Confiant", "Perdu", "Curieux", "Stressé"])
        note = st.text_area("Journal personnel (Optionnel):", placeholder="Aujourd'hui, j'ai appris...")
        
        if st.button("Enregistrer mon état"):
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "mood": mood,
                "tags": ", ".join(tags),
                "note": note
            }
            st.session_state.user['history'].append(entry)
            st.toast("Journal mis à jour !", icon="📓")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VISTA: PROFESOR (DATOS) ---
    elif menu == "Zone Professeur":
        st.markdown("<h1>👨‍🏫 Tableau de Bord Enseignant</h1>", unsafe_allow_html=True)
        
        pwd = st.text_input("Mot de passe:", type="password")
        if pwd == "admin": # En producción usa st.secrets
            st.success("Accès autorisé")
            
            tab1, tab2 = st.tabs(["📊 Données Classe", "📜 Historique Élève"])
            
            with tab1:
                st.metric("Niveau Moyen", "Lvl 4.2")
                st.caption("Basé sur les compétences du LOMLOE")
                # Simulación de gráfica
                chart_data = pd.DataFrame({'Compétence': ['Grammaire', 'Vocabulaire', 'Oral'], 'Score': [80, 65, 40]})
                st.bar_chart(chart_data, x='Compétence', y='Score')
                
            with tab2:
                if st.session_state.user['history']:
                    df_hist = pd.DataFrame(st.session_state.user['history'])
                    st.dataframe(df_hist, use_container_width=True)
                else:
                    st.info("Aucune donnée de journal enregistrée.")
        elif pwd:
            st.error("Mot de passe incorrect")