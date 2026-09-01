import streamlit as st
from core.state_manager import init_state, get_assets
from ui.styles import apply_styles
from ui.components import render_dock
# Aquí importaríamos las vistas (Home, Checkin, Arcade)
# from views import home, checkin, arcade 

st.set_page_config(page_title="Mon Cycle Français", layout="centered", page_icon="🐉")

# 1. Inicializar estado
init_state()

# 2. Onboarding (si es la primera vez)
if not st.session_state.user['setup_complete']:
    st.title("Bienvenue ✨")
    st.write("Elige tu energía:")
    c1, c2, c3 = st.columns(3)
    assets = get_assets()
    
    with c1:
        st.image(assets["Fuego"]["Éveil"], width=80)
        if st.button("Passion (Fuego)"):
            st.session_state.user['elemento'] = "Fuego"
            st.session_state.user['setup_complete'] = True
            st.rerun()
    # (Repetir para Agua y Naturaleza...)

# 3. Aplicación Principal
else:
    # Aplicar estilos basados en el elemento elegido
    apply_styles(st.session_state.user['elemento'])
    
    view = st.session_state.user['view']
    
    if view == 'Home':
        st.markdown(f"<h2 style='text-align:center;'>Bonjour, {st.session_state.user['nombre']}</h2>", unsafe_allow_html=True)
        # Aquí iría el contenido de home.py
    elif view == 'Registro':
        st.title("Check-in 📝")
        # Aquí iría el contenido de checkin.py
    elif view == 'Arcade':
        st.title("Memory Match 🧠")
        # Aquí iría el contenido de arcade.py
        
    # Renderizar siempre el menú inferior
    render_dock()
