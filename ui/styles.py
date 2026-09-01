import streamlit as st

TEMAS = {
    "Fuego": {"bg": "#FFF0EE", "accent": "#D84315", "gradient": "linear-gradient(135deg, #FF9A9E 0%, #FAD0C4 100%)"},
    "Agua":  {"bg": "#E3F2FD", "accent": "#1565C0", "gradient": "linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)"},
    "Naturaleza": {"bg": "#E8F5E9", "accent": "#2E7D32", "gradient": "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)"}
}

def apply_styles(elemento):
    tema = TEMAS.get(elemento, TEMAS["Fuego"])
    xp_percent = (st.session_state.user['xp'] / st.session_state.user['xp_next']) * 100 if st.session_state.user['xp_next'] > 0 else 0
    
    st.markdown(f"""
        <style>
        .stApp {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1A1A1A; background-color: {tema['bg']}; }}
        .stButton button {{ border-radius: 15px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important; }}
        .xp-container {{ width: 100%; background-color: #D3D3D3; border-radius: 20px; margin: 15px 0; height: 12px; overflow: hidden; }}
        .xp-bar {{ height: 100%; border-radius: 20px; transition: width 0.6s; background: {tema['gradient']}; width: {xp_percent}%; }}
        .dragon-circle {{ width: 260px; height: 260px; border-radius: 50%; margin: 30px auto; display: flex; align-items: center; justify-content: center; background: {tema['gradient']}; box-shadow: 0 20px 40px rgba(0,0,0,0.08); border: 10px solid white; }}
        h1, h2, h3 {{ color: {tema['accent']} !important; font-weight: bold; }}
        .dock {{ position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255, 255, 255, 0.95); padding: 15px 0; display: flex; justify-content: space-around; z-index: 999; border-top: 1px solid rgba(0,0,0,0.05); }}
        #MainMenu, footer, header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)
    return tema
