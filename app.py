import streamlit as st
import streamlit.components.v1 as components
import json

# ==========================================================
# BLOQUE 1: CONFIGURACIÓN BÁSICA Y FIREBASE
# ==========================================================
st.set_page_config(page_title="Académie des Dragons", layout="wide", page_icon="🐉")

# IMPORTANTE: Debes ir a firebase.google.com, crear un proyecto web gratuito y pegar aquí tus claves reales.
FIREBASE_CONFIG = """
  apiKey: "TU_API_KEY",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "TUS_SENDER_ID",
  appId: "TU_APP_ID"
"""

# ==========================================================
# BLOQUE 2: ESTILOS VISUALES (CSS)
# ==========================================================
# Usaremos un diseño tipo "Glassmorphism" para una interfaz moderna y atractiva[cite: 2].
CSS_CODE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
    body { font-family: 'Poppins', sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    
    .dragon-grid { display: flex; justify-content: space-around; gap: 15px; flex-wrap: wrap; }
    
    .dragon-card {
        background: white; border-radius: 15px; padding: 20px; width: 30%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 2px solid transparent; transition: 0.3s;
    }
    .dragon-card.eau { border-color: #00C4CC; }
    .dragon-card.plante { border-color: #4CAF50; }
    .dragon-card.feu { border-color: #FF5722; }
    
    .xp-bar-bg { background: #eee; height: 15px; border-radius: 10px; overflow: hidden; margin-top: 10px; }
    .xp-bar-fill { height: 100%; transition: width 0.5s; }
    .eau-fill { background: #00C4CC; }
    .plante-fill { background: #4CAF50; }
    .feu-fill { background: #FF5722; }
    
    .btn-action { background: #333; color: white; border: none; border-radius: 10px; padding: 10px 15px; width: 100%; margin-top: 15px; cursor: pointer; font-weight: bold; }
    .btn-action:hover { background: #555; }
</style>
"""

# ==========================================================
# BLOQUE 3: LÓGICA BACKEND Y BASE DE DATOS (JAVASCRIPT)
# ==========================================================
# Aquí importamos los módulos ES6 oficiales de Firebase y gestionamos la subida de nivel[cite: 2].
JS_CODE = f"""
<script type="module">
    import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
    import {{ getFirestore, doc, setDoc, getDoc }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

    // Conectar con Firestore[cite: 2]
    const firebaseConfig = {{ {FIREBASE_CONFIG} }};
    let db = null;
    try {{
        const app = initializeApp(firebaseConfig);
        db = getFirestore(app);
        console.log("🔥 Firebase Firestore Conectado!");
    }} catch (e) {{
        console.error("Error al conectar Firebase:", e);
    }}

    // Estado inicial del alumno
    window.studentData = {{
        id: "ALUMNO_DEMO_01",
        dragons: {{
            eau: {{ xp: 0, level: 1, name: "Goutte" }},
            plante: {{ xp: 0, level: 1, name: "Feuille" }},
            feu: {{ xp: 0, level: 1, name: "Flamme" }}
        }}
    }};

    window.app = {{
        init: async () => {{
            if (!db) return;
            // Recuperar datos de la nube al entrar[cite: 2]
            const docRef = doc(db, "students", window.studentData.id);
            const docSnap = await getDoc(docRef);
            
            if (docSnap.exists()) {{
                window.studentData = docSnap.data();
            }} else {{
                // Si es nuevo, lo guardamos por primera vez
                await setDoc(docRef, window.studentData);
            }}
            window.app.updateUI();
        }},

        addXP: async (type, amount) => {{
            let dragon = window.studentData.dragons[type];
            dragon.xp += amount;
            
            // Lógica de subida de nivel (cada 100 XP sube de fase)
            if (dragon.xp >= dragon.level * 100) {{
                dragon.xp = 0;
                dragon.level += 1;
                alert(`¡Felicidades! Tu dragón de ${{type}} ha evolucionado al Nivel ${{dragon.level}}`);
            }}
            
            window.app.updateUI();
            
            // Guardar progreso en la nube Firestore de forma segura[cite: 2]
            if (db) {{
                await setDoc(doc(db, "students", window.studentData.id), window.studentData);
            }}
        }},

        updateUI: () => {{
            const types = ['eau', 'plante', 'feu'];
            types.forEach(type => {{
                let data = window.studentData.dragons[type];
                document.getElementById(`lvl-${{type}}`).innerText = `Niv. ${{data.level}}`;
                document.getElementById(`xp-${{type}}`).innerText = `${{data.xp}} / ${{data.level * 100}} XP`;
                
                let pct = (data.xp / (data.level * 100)) * 100;
                document.getElementById(`bar-${{type}}`).style.width = `${{pct}}%`;
            }});
        }}
    }};

    // Iniciar la app cuando cargue la página
    setTimeout(() => window.app.init(), 300);
</script>
"""

# ==========================================================
# BLOQUE 4: ESTRUCTURA VISUAL (HTML)
# ==========================================================
HTML_CODE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {CSS_CODE}
</head>
<body>
    <div class="glass-panel">
        <h1>🐲 Tes Dragons de la 2030</h1>
        <p>Gana experiencia cumpliendo misiones ODS para evolucionarlos.</p>
    </div>

    <div class="dragon-grid">
        <!-- DRAGÓN DE AGUA -->
        <div class="dragon-card eau">
            <h2><i class="fa-solid fa-droplet" style="color: #00C4CC;"></i> Eau</h2>
            <h4 id="lvl-eau">Niv. 1</h4>
            <div class="xp-bar-bg"><div id="bar-eau" class="xp-bar-fill eau-fill" style="width: 0%;"></div></div>
            <p id="xp-eau" style="font-size: 0.8rem; text-align: center; margin-top:5px;">0 / 100 XP</p>
            <button class="btn-action" onclick="window.app.addXP('eau', 25)">+25 XP (Misión ODS 14)</button>
        </div>

        <!-- DRAGÓN DE PLANTA -->
        <div class="dragon-card plante">
            <h2><i class="fa-solid fa-leaf" style="color: #4CAF50;"></i> Plante</h2>
            <h4 id="lvl-plante">Niv. 1</h4>
            <div class="xp-bar-bg"><div id="bar-plante" class="xp-bar-fill plante-fill" style="width: 0%;"></div></div>
            <p id="xp-plante" style="font-size: 0.8rem; text-align: center; margin-top:5px;">0 / 100 XP</p>
            <button class="btn-action" onclick="window.app.addXP('plante', 25)">+25 XP (Misión ODS 13)</button>
        </div>

        <!-- DRAGÓN DE FUEGO -->
        <div class="dragon-card feu">
            <h2><i class="fa-solid fa-fire" style="color: #FF5722;"></i> Feu</h2>
            <h4 id="lvl-feu">Niv. 1</h4>
            <div class="xp-bar-bg"><div id="bar-feu" class="xp-bar-fill feu-fill" style="width: 0%;"></div></div>
            <p id="xp-feu" style="font-size: 0.8rem; text-align: center; margin-top:5px;">0 / 100 XP</p>
            <button class="btn-action" onclick="window.app.addXP('feu', 25)">+25 XP (Misión ODS 7)</button>
        </div>
    </div>

    {JS_CODE}
</body>
</html>
"""

# Renderizar toda la interfaz en Streamlit[cite: 2]
components.html(HTML_CODE, height=600, scrolling=True)
