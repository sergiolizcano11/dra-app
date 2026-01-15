{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab560
\pard\pardeftab560\slleading20\pardirnatural\partightenfactor0

\f0\fs26 \cf0 app.py\
\
import streamlit as st\
import pandas as pd\
import time\
\
# --- CONFIGURACI\'d3N ---\
st.set_page_config(page_title="Mon Dragon de Fran\'e7ais", layout="wide", page_icon="\uc0\u55357 \u56329 ")\
\
# Estilo CSS personalizado para que se vea m\'e1s amigable\
st.markdown("""\
    <style>\
    .main \{ background-color: #f0f2f6; \}\
    .stMetric \{ background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); \}\
    </style>\
    """, unsafe_allow_html=True)\
\
if 'db' not in st.session_state:\
    st.session_state.db = \{'puntos': 0, 'feedback': [], 'nombre_dragon': "\'c9clair"\}\
\
# --- L\'d3GICA DE EVOLUCI\'d3N ---\
def obtener_estado_dragon(puntos):\
    niveles = [\
        (20, "\uc0\u55358 \u56666  Huevo", "https://cdn-icons-png.flaticon.com/512/3232/3232717.png"),\
        (50, "\uc0\u55357 \u56438  Drag\'f3n Beb\'e9", "https://cdn-icons-png.flaticon.com/512/616/616554.png"),\
        (100, "\uc0\u55357 \u56613  Drag\'f3n Joven", "https://cdn-icons-png.flaticon.com/512/616/616430.png"),\
        (float('inf'), "\uc0\u55357 \u56401  Drag\'f3n Maestro", "https://cdn-icons-png.flaticon.com/512/616/616613.png")\
    ]\
    for limite, nombre, url in niveles:\
        if puntos < limite:\
            return nombre, url\
\
# --- NAVEGACI\'d3N ---\
with st.sidebar:\
    st.image("https://cdn-icons-png.flaticon.com/512/616/616430.png", width=100)\
    st.title("Men\'fa Principal")\
    modo = st.radio("Secciones:", ["\uc0\u55356 \u57312  Mi Drag\'f3n", "\u55357 \u56541  Examen", "\u55357 \u56492  Feedback", "\u55357 \u56594  Profesor"])\
\
# --- VISTA: MI DRAG\'d3N ---\
if modo == "\uc0\u55356 \u57312  Mi Drag\'f3n":\
    st.title(f"Salut ! Soy \{st.session_state.db['nombre_dragon']\}")\
    estado, url = obtener_estado_dragon(st.session_state.db['puntos'])\
    \
    col1, col2 = st.columns([1, 2])\
    with col1:\
        st.image(url, use_container_width=True)\
    with col2:\
        st.subheader(f"Nivel actual: \{estado\}")\
        st.metric(label="Experiencia Total", value=f"\{st.session_state.db['puntos']\} XP")\
        # Barra de progreso din\'e1mica\
        progreso = min(st.session_state.db['puntos'] / 100, 1.0)\
        st.progress(progreso, text=f"Progreso hacia la evoluci\'f3n: \{int(progreso*100)\}%")\
\
# --- VISTA: EXAMEN ---\
elif modo == "\uc0\u55357 \u56541  Examen":\
    st.title("\uc0\u55357 \u56541  Challenge de Fran\'e7ais")\
    \
    with st.container(border=True):\
        with st.form("quiz"):\
            q1 = st.radio("1. \'bfCu\'e1l es el art\'edculo correcto para 'Table'?", ["Le", "La", "L'"])\
            q2 = st.text_input("2. Traduce 'Hola' al franc\'e9s:")\
            \
            if st.form_submit_button("Corregir"):\
                puntos = 0\
                if q1 == "La": puntos += 10\
                if q2.lower().strip() in ["salut", "bonjour"]: puntos += 10\
                \
                if puntos > 0:\
                    st.session_state.db['puntos'] += puntos\
                    st.balloons()\
                    st.success(f"\'a1Bravo! Ganaste \{puntos\} XP")\
                else:\
                    st.error("Sigue practicando, \'a1t\'fa puedes!")\
\
# --- VISTA: PROFESOR ---\
elif modo == "\uc0\u55357 \u56594  Profesor":\
    st.title("\uc0\u55357 \u56424 \u8205 \u55356 \u57323  Panel Docente")\
    pwd = st.text_input("Contrase\'f1a:", type="password")\
    if pwd == "profesor2024":\
        st.success("Acceso concedido")\
        # Visualizaci\'f3n de datos r\'e1pida\
        df = pd.DataFrame(st.session_state.db['feedback'])\
        if not df.empty:\
            st.subheader("Estado emocional de la clase")\
            st.bar_chart(df['Animo'].value_counts())\
            st.table(df)}