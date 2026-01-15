import streamlit as st
import pandas as pd
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mon Dragon de Français", layout="wide", page_icon="🐉")

# Estilo CSS personalizado para que se vea más amigable
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = {'puntos': 0, 'feedback': [], 'nombre_dragon': "Éclair"}

# --- LÓGICA DE EVOLUCIÓN ---
def obtener_estado_dragon(puntos):
    niveles = [
        (20, "🥚 Huevo", "https://cdn-icons-png.flaticon.com/512/3232/3232717.png"),
        (50, "👶 Dragón Bebé", "https://cdn-icons-png.flaticon.com/512/616/616554.png"),
        (100, "🔥 Dragón Joven", "https://cdn-icons-png.flaticon.com/512/616/616430.png"),
        (float('inf'), "👑 Dragón Maestro", "https://cdn-icons-png.flaticon.com/512/616/616613.png")
    ]
    for limite, nombre, url in niveles:
        if puntos < limite:
            return nombre, url

# --- NAVEGACIÓN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616430.png", width=100)
    st.title("Menú Principal")
    modo = st.radio("Secciones:", ["🏠 Mi Dragón", "📝 Examen", "💬 Feedback", "🔒 Profesor"])

# --- VISTA: MI DRAGÓN ---
if modo == "🏠 Mi Dragón":
    st.title(f"Salut ! Soy {st.session_state.db['nombre_dragon']}")
    estado, url = obtener_estado_dragon(st.session_state.db['puntos'])
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(url, use_container_width=True)
    with col2:
        st.subheader(f"Nivel actual: {estado}")
        st.metric(label="Experiencia Total", value=f"{st.session_state.db['puntos']} XP")
        # Barra de progreso dinámica
        progreso = min(st.session_state.db['puntos'] / 100, 1.0)
        st.progress(progreso, text=f"Progreso hacia la evolución: {int(progreso*100)}%")

# --- VISTA: EXAMEN ---
elif modo == "📝 Examen":
    st.title("📝 Challenge de Français")
    
    with st.container(border=True):
        with st.form("quiz"):
            q1 = st.radio("1. ¿Cuál es el artículo correcto para 'Table'?", ["Le", "La", "L'"])
            q2 = st.text_input("2. Traduce 'Hola' al francés:")
            
            if st.form_submit_button("Corregir"):
                puntos = 0
                if q1 == "La": puntos += 10
                if q2.lower().strip() in ["salut", "bonjour"]: puntos += 10
                
                if puntos > 0:
                    st.session_state.db['puntos'] += puntos
                    st.balloons()
                    st.success(f"¡Bravo! Ganaste {puntos} XP")
                else:
                    st.error("Sigue practicando, ¡tú puedes!")

# --- VISTA: PROFESOR ---
elif modo == "🔒 Profesor":
    st.title("👨‍🏫 Panel Docente")
    pwd = st.text_input("Contraseña:", type="password")
    if pwd == "profesor2024":
        st.success("Acceso concedido")
        # Visualización de datos rápida
        df = pd.DataFrame(st.session_state.db['feedback'])
        if not df.empty:
            st.subheader("Estado emocional de la clase")
            st.bar_chart(df['Animo'].value_counts())
            st.table(df)