import streamlit as st
import pandas as pd
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

### --- 1. CONFIGURACIÓN VISUAL Y APP ---
st.set_page_config(
    page_title="L'Alliance Olympique",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="expanded" 
)

### --- 2. CSS AVANZADO (DISEÑO GEN Z) ---
st.markdown("""
<style>
    /* PALETA DE COLORES */
    :root {
        --blue: #4D79FF;
        --yellow: #FFD93D;
        --green: #6BCB77;
        --red: #FF6B6B;
        --bg: #F4F7F6;
        --card-bg: #FFFFFF;
    }

    /* FONDO GENERAL */
    .stApp {
        background-color: var(--bg);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ESCONDER ELEMENTOS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ESTILO DE TARJETAS (CARDS) */
    .css-1r6slb0, .stDataFrame, .stForm, div[data-testid="stExpander"] {
        background: var(--card-bg);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border: none;
        margin-bottom: 15px;
    }

    /* BOTONES PRINCIPALES */
    .stButton > button {
        background: linear-gradient(90deg, var(--blue), #3a60d0);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 12px 25px;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 4px 15px rgba(77, 121, 255, 0.3);
        transition: all 0.2s;
    }
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* INPUTS DE TEXTO */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #EEE;
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--blue);
    }

    /* AVATAR GRANDE */
    .avatar-circle {
        font-size: 60px;
        background: #EFF3FF;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        border: 4px solid var(--blue);
        box-shadow: 0 5px 15px rgba(77, 121, 255, 0.2);
    }

    /* TEXTOS */
    h1 {
        color: #2D3436;
        font-weight: 800;
        text-align: center;
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

### --- 3. GESTIÓN DE DATOS (DATABASE ACTUALIZADA) ---
FILE_ELEVES = 'eleves.csv' 
FILE_PROPOSALS = 'propositions.csv' 
FILE_VOTES = 'votes_finaux.csv' 
FILE_EVAL_PROF = 'evaluation_prof.csv' # NUEVO ARCHIVO DOCENTE

def init_db(): 
    # Definición de columnas 
    cols_eleves = ['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID'] 
    # AÑADIDO: 'Nom_Epreuve' 
    cols_props = ['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve'] 
    cols_votes = ['Votante', 'Equite', 'FairPlay', 'Innovation', 'Francophonie'] 
    # NUEVO: Tabla de Evaluación Docente 
    cols_eval = ['Equipe', 'Nom_Epreuve', 'Stars_Epreuve', 'Stars_Eleve1', 'Stars_Eleve2', 'Commentaire']

    # 1. Alumnos 
    if not os.path.exists(FILE_ELEVES): 
        pd.DataFrame(columns=cols_eleves).to_csv(FILE_ELEVES, index=False) 
    else: 
        df = pd.read_csv(FILE_ELEVES) 
        if not set(cols_eleves).issubset(df.columns): 
            pd.DataFrame(columns=cols_eleves).to_csv(FILE_ELEVES, index=False)

    # 2. Propuestas (Actualización con columna Nom_Epreuve) 
    if not os.path.exists(FILE_PROPOSALS): 
        pd.DataFrame(columns=cols_props).to_csv(FILE_PROPOSALS, index=False) 
    else: 
        df = pd.read_csv(FILE_PROPOSALS) 
        # Reparación automática si falta la columna nueva 
        if 'Nom_Epreuve' not in df.columns: 
            df['Nom_Epreuve'] = "Non défini" 
            df.to_csv(FILE_PROPOSALS, index=False) 
        if 'Status' not in df.columns: 
            df['Status'] = 'Pending' 
            df.to_csv(FILE_PROPOSALS, index=False) 
            
    # 3. Votos Finales 
    if not os.path.exists(FILE_VOTES): 
        pd.DataFrame(columns=cols_votes).to_csv(FILE_VOTES, index=False)

    # 4. Evaluación Profesor (NUEVO) 
    if not os.path.exists(FILE_EVAL_PROF): 
        pd.DataFrame(columns=cols_eval).to_csv(FILE_EVAL_PROF, index=False)

def load_data(file): return pd.read_csv(file) 
def save_data(df, file): df.to_csv(file, index=False)

init_db() 
df_eleves = load_data(FILE_ELEVES) 
df_proposals = load_data(FILE_PROPOSALS) 
df_votes = load_data(FILE_VOTES) 
df_eval = load_data(FILE_EVAL_PROF)

### --- 4. FUNCIÓN GENERADOR DE CARNET ---
def create_badge(pseudo, avatar, role="Athlète"): 
    W, H = 400, 600 
    img = Image.new('RGB', (W, H), color='white') 
    d = ImageDraw.Draw(img) 
    d.rectangle([(0, 0), (W, 150)], fill='#4D79FF') 
    try: font = ImageFont.truetype("arial.ttf", 40) 
    except: font = ImageFont.load_default() 
    d.text((20, 50), "JO AVENIR", fill="white", font=font) 
    d.text((150, 200), avatar, fill="black", font=font) 
    d.text((50, 300), pseudo, fill="black", font=font) 
    
    qr = qrcode.QRCode(box_size=4, border=1) 
    qr.add_data(f"ID:{pseudo}") 
    qr.make(fit=True) 
    img.paste(qr.make_image(fill_color="black", back_color="white"), (100, 420)) 
    
    img_byte_arr = io.BytesIO() 
    img.save(img_byte_arr, format='PNG') 
    return img_byte_arr.getvalue()

### --- 5. NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state['page'] = 'profile' 
def nav(page_name): 
    st.session_state['page'] = page_name
    st.rerun()

# ==========================================
#              PÁGINAS DE LA APP
# ==========================================

# --- PÁGINA 1: PERFIL ---
if st.session_state['page'] == 'profile':
    st.markdown("<h1>👤 Mon Profil</h1>", unsafe_allow_html=True)
    
    with st.form("profile_maker"):
        st.markdown("<div class='avatar-circle'>😎</div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>Choisis ton visage</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1,3])
        with c1:
            avatar = st.selectbox("Emoji", ["🦊", "🦁", "🦄", "⚡", "👽", "🤖", "🔥", "🚀"], label_visibility="collapsed")
        with c2:
            pseudo = st.text_input("Ton Bledger (Pseudo)", placeholder="Ex: Flash_Gordon", label_visibility="collapsed")
        
        st.markdown("### ⚡ Mes Super-Pouvoirs (Max 2)")
        forces = st.multiselect("Forces", 
                              ["Vitesse 🏃‍♂️", "Force 💪", "Stratégie 🧠", "Endurance 🔋", "Mental 🧘", "Organisation 📋"],
                              label_visibility="collapsed")
        
        st.markdown("### 🐢 Mon Point Faible")
        faiblesse = st.text_input("Weakness", placeholder="Ex: Je suis désordonné...", label_visibility="collapsed")
        
        st.markdown("### 📢 Slogan / Devise")
        slogan = st.text_input("Slogan", placeholder="Toujours plus loin !", label_visibility="collapsed")

        if st.form_submit_button("💾 Sauvegarder"):
            if pseudo and len(forces) > 0:
                new_user = pd.DataFrame([[pseudo, avatar, ", ".join(forces), faiblesse, slogan, "None"]], 
                                      columns=['Pseudo', 'Avatar', 'Forces', 'Faiblesse', 'Slogan', 'TeamID'])
                df_eleves = pd.concat([df_eleves, new_user], ignore_index=True)
                save_data(df_eleves, FILE_ELEVES)
                st.success("Profil Créé ! Va au Marché.")
            else:
                st.error("Remplis ton nom et tes forces !")

# --- PÁGINA 2: MERCADO (MATCHING) ---
elif st.session_state['page'] == 'market':
    st.markdown("<h1>🤝 Le Marché</h1>", unsafe_allow_html=True)
    st.info("💡 Cherche quelqu'un qui complète tes faiblesses.")

    if df_eleves.empty:
        st.warning("Personne ici... Crée ton profil d'abord !")
    else:
        for i, row in df_eleves.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"<div style='font-size:40px; text-align:center;'>{row['Avatar']}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{row['Pseudo']}**")
                    st.caption(f"⚡ {row['Forces']} | 🐢 {row['Faiblesse']}")
                
                with st.expander(f"💌 Faire équipe avec {row['Pseudo']}"):
                    with st.form(f"form_{i}"):
                        me = st.text_input("Ton Pseudo", placeholder="Qui es-tu ?")
                        epreuve = st.text_input("Nom de l'épreuve à créer ensemble", placeholder="Ex: Course de recyclage")
                        
                        st.markdown("**Pourquoi ce choix ? (Aide-toi de ces phrases) :**")
                        st.caption("• *Je te choisis parce que tu es fort en...*")
                        st.caption("• *Je suis rapide mais tu es organisé...*")
                        
                        justif = st.text_area("Ta justification", placeholder="Écris ici...")
                        
                        if st.form_submit_button("🚀 Envoyer Proposition"):
                            if len(justif) > 10 and epreuve:
                                # Las 7 columnas definidas en cols_props
                                new_p = pd.DataFrame([[me, row['Pseudo'], justif, 0, 0, "Pending", epreuve]],
                                                   columns=['Demandeur', 'Partenaire', 'Justification', 'Votes_Pour', 'Votes_Contre', 'Status', 'Nom_Epreuve'])
                                df_proposals = pd.concat([df_proposals, new_p], ignore_index=True)
                                save_data(df_proposals, FILE_PROPOSALS)
                                st.success("Envoyé au Conseil !")
                            else:
                                st.error("Remplis le nom de l'épreuve et explique bien ton choix !")

# --- PÁGINA 3: CONSEJO (VOTACIÓN) ---
elif st.session_state['page'] == 'council':
    st.markdown("<h1>⚖️ Le Conseil</h1>", unsafe_allow_html=True)
    
    pending = df_proposals[df_proposals['Status'] == 'Pending']
    
    if pending.empty:
        st.info("Rien à voter pour l'instant.")
    else:
        for i, row in pending.iterrows():
            st.markdown(f"### ⚔️ Duo: {row['Demandeur']} + {row['Partenaire']}")
            st.markdown(f"**Épreuve Proposée :** {row['Nom_Epreuve']}")
            st.info(f"🗣️ \"{row['Justification']}\"")
            
            c1, c2 = st.columns(2)
            if c1.button(f"👍 Validé ({row['Votes_Pour']})", key=f"y{i}"):
                df_proposals.at[i, 'Votes_Pour'] += 1
                if df_proposals.at[i, 'Votes_Pour'] >= 3:
                    df_proposals.at[i, 'Status'] = 'Approved'
                    st.balloons()
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()
                
            if c2.button(f"👎 Revoir ({row['Votes_Contre']})", key=f"n{i}"):
                df_proposals.at[i, 'Votes_Contre'] += 1
                save_data(df_proposals, FILE_PROPOSALS)
                st.rerun()
            st.markdown("---")

# --- PÁGINA 4: MI CARNET (BADGE) ---
elif st.session_state['page'] == 'badge':
    st.markdown("<h1>🆔 Mon Passeport</h1>", unsafe_allow_html=True)
    st.write("Télécharge ton accréditation officielle pour la Gymkhana.")
    
    user_check = st.text_input("Vérifie ton pseudo pour générer le badge:")
    
    if user_check:
        user_data = df_eleves[df_eleves['Pseudo'] == user_check]
        if not user_data.empty:
            avatar = user_data.iloc[0]['Avatar']
            badge_bytes = create_badge(user_check, avatar)
            
            st.image(badge_bytes, caption="Ton Badge Officiel")
            
            st.download_button(
                label="⬇️ Télécharger Image (PNG)",
                data=badge_bytes,
                file_name=f"badge_{user_check}.png",
                mime="image/png"
            )
        else:
            st.error("Pseudo introuvable.")

# ==========================================
#        BARRA DE NAVEGACIÓN INFERIOR
# ==========================================
st.markdown("---")
nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("👤\nProfil"): nav('profile')
with nav2:
    if st.button("🤝\nMarché"): nav('market')
with nav3:
    if st.button("⚖️\nConseil"): nav('council')
with nav4:
    if st.button("🆔\nBadge"): nav('badge')
