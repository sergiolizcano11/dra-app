import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

### --- 1. CONFIGURACIÓN VISUAL Y APP ---
st.set_page_config(
    page_title="L'Alliance Olympique",
    page_icon="🐉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

### --- 2. CSS AVANZADO (DISEÑO GEN Z) ---
st.markdown("""
<style>
    :root { --blue: #4D79FF; --yellow: #FFD93D; --green: #6BCB77; --red: #FF6B6B; --bg: #F4F7F6; }
    .stApp { background-color: var(--bg); font-family: 'Segoe UI', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* TARJETAS */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"], .solid-panel {
        background: white; border-radius: 24px; padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); border: none; margin-bottom: 15px;
    }
    
    /* BOTONES */
    .stButton > button {
        background: linear-gradient(90deg, var(--blue), #3a60d0); color: white;
        border-radius: 15px; border: none; padding: 10px; font-weight: 700; width: 100%;
    }
    
    /* AVATAR */
    .avatar-circle {
        font-size: 60px; background: #EFF3FF; width: 100px; height: 100px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px auto; border: 3px solid var(--blue);
    }
    
    /* MENÚ INFERIOR */
    .dock-nav {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: white; border-top: 1px solid #eee;
        display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

### --- 3. GESTIÓN DE DATOS (DATABASE ACTUALIZADA) ---
FILE_ELEVES = 'eleves.csv'
FILE_PROPOSALS = 'propositions.csv'
FILE_VOTES = 'votes_finaux.csv'
FILE_EVAL_PROF = 'evaluation_prof.csv'

def init_db():
    # AÑADIDO: 'XP' a cols_eleves para guardar la experiencia del dragón
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID', 'XP']
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve']
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie']
    cols_eval = ['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire']

    # 1. Alumnos
    if not os.path.exists(FILE_ELEVES):
        pd.DataFrame(columns=cols_eleves).to_csv(FILE_ELEVES, index=False)
    else:
        df = pd.read_csv(FILE_ELEVES)
        if 'XP' not in df.columns:
            df['XP'] = 0
            df.to_csv(FILE_ELEVES, index=False)

    # 2. Propuestas
    if not os.path.exists(FILE_PROPOSALS):
        pd.DataFrame(columns=cols_props).to_csv(FILE_PROPOSALS, index=False)
        
    # 3. Votos Finales
    if not os.path.exists(FILE_VOTES):
        pd.DataFrame(columns=cols_votes).to_csv(FILE_VOTES, index=False)

    # 4. Evaluación Profesor
    if not os.path.exists(FILE_EVAL_PROF):
        pd.DataFrame(columns=cols_eval).to_csv(FILE_EVAL_PROF, index=False)

def load_data(file): return pd.read_csv(file)
def save_data(df, file): df.to_csv(file, index=False)

init_db()
df_eleves = load_data(FILE_ELEVES)

### --- 4. FUNCIÓN GENERADOR DE CARNET ---
def create_badge(pseudo, avatar, role="Athlète"):
    W, H = 400, 600
    img = Image.new('RGB', (W, H), color='white')
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 150)], fill='#4D79FF')
    try: font = ImageFont.truetype("arial.ttf", 40)
    except: font = ImageFont.load_default()
    d.text((20, 50), "ACADÉMIE DRAGON", fill="white", font=font)
    d.text((150, 200), avatar, fill="black", font=font)
    d.text((50, 300), pseudo, fill="black", font=font)
    
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(f"ID:{pseudo}")
    qr.make(fit=True)
    img.paste(qr.make_image(fill_color="black", back_color="white"), (100, 420))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

### --- 5. ENRUTAMIENTO Y ESTADO GLOBAL ---
if 'page' not in st.session_state: 
    st.session_state['page'] = 'profile'
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

def ganar_xp(cantidad):
    if st.session_state['current_user']:
        idx = df_eleves.index[df_eleves['Pseudo'] == st.session_state['current_user']].tolist()[0]
        df_eleves.at[idx, 'XP'] += cantidad
        save_data(df_eleves, FILE_ELEVES)
        st.toast(f"¡+{cantidad} XP ganada!", icon="🐉")

# ==========================================
#              VISTAS DE LA APP
# ==========================================

# --- VISTA 1: CREACIÓN DE PERFIL (SOLO 1 DRAGÓN) ---
if st.session_state['page'] == 'profile':
    st.markdown("<h2 style='text-align:center;'>Choisis ton Dragon 🥚</h2>", unsafe_allow_html=True)
    
    with st.form("profile_maker"):
        pseudo = st.text_input("Ton Pseudo (Nombre):", placeholder="Ex: Apprenti_01")
        
        st.markdown("### L'Élément de ton Dragon")
        st.caption("Selecciona solo uno. Tu elección definirá tu elemento ODS.")
        # SELECCIÓN ÚNICA DE DRAGÓN
        avatar = st.radio("Tipos de Dragón:", [
            "💧 Dragon d'Eau (Adaptabilidad - ODS 14)", 
            "🌿 Dragon de Plante (Ecología - ODS 15)", 
            "🔥 Dragon de Feu (Energía - ODS 7)"
        ], label_visibility="collapsed")
        
        forces = st.selectbox("Ton Super-Pouvoir:", ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠"])
        
       if st.form_submit_button("Éclore l'Œuf (Empezar)"):
            if pseudo:
                # Extraemos solo el emoji del dragón elegido
                emoji_dragon = avatar.split(" ")[0] 
                
                # Comprobar si ya existe
                if pseudo not in df_eleves['Pseudo'].values:
                    new_user = pd.DataFrame([[pseudo, emoji_dragon, forces, "Aucune", "Prêt", "None", 0]], 
                                          columns=df_eleves.columns)
                    
                    # AQUÍ ESTABA EL ERROR: Hemos eliminado la línea "global df_eleves"
                    df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
                    save_data(df_eleves, FILE_ELEVES)
                
                st.session_state['current_user'] = pseudo
                nav('home')
            else:
                st.error("¡Debes introducir un nombre!")
# --- VISTA 2: HOME / DASHBOARD ---
elif st.session_state['page'] == 'home':
    if not st.session_state['current_user']:
        nav('profile')
        
    user_data = df_eleves[df_eleves['Pseudo'] == st.session_state['current_user']].iloc[0]
    nivel = int(user_data['XP'] / 100) + 1
    
    st.markdown(f"<div class='avatar-circle'>{user_data['Avatar']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>{user_data['Pseudo']}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Niveau (Nivel)", f"Lvl {nivel}")
    col2.metric("Expérience", f"{user_data['XP']} XP")
    
    st.progress(min((user_data['XP'] % 100) / 100, 1.0))
    st.caption(f"Faltan {100 - (user_data['XP'] % 100)} XP para el próximo nivel.")
    
    st.markdown("---")
    img = create_badge(user_data['Pseudo'], user_data['Avatar'])
    st.download_button("⬇️ Télécharger ma Carte (PDF/PNG)", img, file_name="mon_dragon.png", mime="image/png")

# --- VISTA 3: MISIONES (ODS) ---
elif st.session_state['page'] == 'missions':
    st.markdown("<h2>Missions ODD 🌍</h2>", unsafe_allow_html=True)
    st.info("Completa retos ecológicos en clase para ganar XP para tu dragón.")
    
    with st.container(border=True):
        st.markdown("#### ♻️ Gardiens de la Terre")
        st.caption("Recicla 3 envases en el instituto y escribe sus nombres en francés.")
        if st.button("Valider Mission (+50 XP)", key="m1"):
            ganar_xp(50)
            st.rerun()

    with st.container(border=True):
        st.markdown("#### 💧 L'Eau c'est la vie")
        st.caption("Trae una botella reutilizable a clase durante toda la semana.")
        if st.button("Valider Mission (+100 XP)", key="m2"):
            ganar_xp(100)
            st.rerun()

# --- VISTA 4: ARCADE (MINIJUEGOS) ---
elif st.session_state['page'] == 'arcade':
    st.markdown("<h2>Salle d'Arcade 🎮</h2>", unsafe_allow_html=True)
    st.info("Entrena tu gramática francesa para fortalecer a tu dragón.")
    
    st.markdown("#### Quiz: Le Futur Simple")
    q1 = st.radio("Demain, je _____ (manger) sain.", ["mangerais", "mangerai", "mange"], index=None)
    if st.button("Comprobar Respuesta"):
        if q1 == "mangerai":
            st.success("¡Correcto!")
            ganar_xp(20)
        else:
            st.error("Incorrecto. Intenta de nuevo.")

# ==========================================
# MENÚ INFERIOR DE NAVEGACIÓN
# ==========================================
st.write("<br><br><br><br>", unsafe_allow_html=True) # Espacio para el menú fijo
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("👤\nPerfil"): nav('profile')
with c2:
    if st.button("🏠\nInicio"): nav('home')
with c3:
    if st.button("🌍\nMisiones"): nav('missions')
with c4:
    if st.button("🎮\nArcade"): nav('arcade')
