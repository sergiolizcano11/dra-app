import streamlit as st

def render_dock():
    st.write("<br><br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    view = st.session_state.user['view']
    
    with c1:
        if st.button("⭕ Inicio", use_container_width=True, type="primary" if view == 'Home' else "secondary"):
            st.session_state.user['view'] = 'Home'
            st.rerun()
    with c2:
        if st.button("➕ Entrenar", use_container_width=True, type="primary" if view == 'Registro' else "secondary"):
            st.session_state.user['view'] = 'Registro'
            st.rerun()
    with c3:
        if st.button("🎮 Juegos", use_container_width=True, type="primary" if view == 'Arcade' else "secondary"):
            st.session_state.user['view'] = 'Arcade'
            st.rerun()
