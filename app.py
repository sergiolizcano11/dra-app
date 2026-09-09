import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from fpdf import FPDF
from gtts import gTTS
from st_audiorec import st_audiorec
import io
import qrcode
import tempfile
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Dragon Évolution : L'Alliance ODD",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🐉"
)

# --- FUNCIONES BACKEND (ZONA PROFESOR & DUA) ---
def create_dragon_diploma(name, element, trait):
    """Genera un diploma PDF del dragón (Gamificación tangible)."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(240, 245, 250)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_draw_color(40, 40, 80)
    pdf.set_line_width(2)
    pdf.rect(15, 15, 180, 267)
    
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(0, 30)
    pdf.cell(210, 15, "CERTIFICAT DE DRESSEUR ODD", 0, 1, 'C')
    
    pdf.set_font("Arial", 'B', 35)
    if element == 'Feu': pdf.set_text_color(200, 50, 50)
    elif element == 'Eau': pdf.set_text_color(0, 100, 200)
    else: pdf.set_text_color(34, 139, 34)
    pdf.cell(210, 25, name.upper(), 0, 1, 'C')
    
    pdf.set_font("Arial", 'I', 18)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(210, 10, f"Élément : Dragon d'{element}", 0, 1, 'C')
    pdf.cell(210, 10, f"ADN / Atout : {trait}", 0, 1, 'C')
    
    # Código QR de Validación del Profesor[cite: 2]
    qr = qrcode.make(f"Dresseur: {name} | Element: {element} | Agenda 2030")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        qr.save(tmpfile.name)
        pdf.image(tmpfile.name, x=75, y=120, w=60)
    os.remove(tmpfile.name)
    
    return pdf.output(dest='S').encode('latin-1')

# --- BARRA LATERAL (HERRAMIENTAS DUA & ADMIN) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐉</h1>", unsafe_allow_html=True)
    st.title("Outils DUA & Admin")
    
    # DUA: Text-to-Speech (Lecteur Immersif)[cite: 1, 2]
    with st.expander("🗣️ Lecteur (TTS)"):
        st.caption("Écrivez pour écouter en français.")
        text_to_speak = st.text_input("Texte:", "Bienvenue dresseur !")
        if st.button("Écouter 🔊"):
            try:
                tts = gTTS(text=text_to_speak, lang='fr')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except:
                st.error("Erreur audio.")

    # DUA: Grabadora (Micro d'Or)[cite: 1, 2]
    with st.expander("🎙️ Micro d'Or (Enregistrement)"):
        st.caption("Entraînement oral ou réflexion vocale.")
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')
            st.success("Audio enregistré ! Tu peux le sauvegarder.")

    st.divider()
    
    # Generador de Diplomas[cite: 2]
    st.markdown("### 🖨️ Diplôme Officiel")
    d_name = st.text_input("Nom du Dresseur (Élève):", "Apprenti")
    d_element = st.selectbox("Élément du Dragon:", ["Eau", "Feu", "Plante"])
    d_trait = st.selectbox("Atout principal:", ["Force", "Sagesse", "Vitesse", "Créativité"])
    if st.button("📄 Générer Diplôme PDF"):
        pdf_data = create_dragon_diploma(d_name, d_element, d_trait)
        st.download_button("📥 Télécharger le PDF", pdf_data, file_name="diplome_dragon.pdf", mime="application/pdf")

# --- CSS BASE PARA OCULTAR INTERFAZ DE STREAMLIT ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100%;}
        iframe {height: 100vh !important; width: 100vw !important; border: none;}
        [data-testid="stSidebar"] { background-color: #f4f6f9; border-right: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# --- FRONTEND (HTML / JS / CSS) ---
# Aquí reside el RPG, la evolución del dragón y el Diario de a Bordo restaurado[cite: 2].
html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --eau: #3498db; --feu: #e74c3c; --plante: #2ecc71;
            --bg-dark: #1a1a2e; --panel-bg: rgba(25, 30, 45, 0.9);
            --text-main: #f1f2f6; --accent: #f1c40f;
            --font-game: 'Nunito', sans-serif;
        }
        body {
            background-color: var(--bg-dark);
            background-image: radial-gradient(circle at top right, #16213e, #0f3460);
            color: var(--text-main); font-family: var(--font-game);
            margin: 0; padding: 0; overflow-x: hidden; padding-bottom: 90px; min-height: 100vh;
        }
        
        /* CONTENEDORES Y PANELES */
        .view { display: none; padding: 20px; animation: fadeIn 0.4s; }
        .active-view { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        
        .solid-panel {
            background-color: var(--panel-bg); border-radius: 20px; padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px); margin-bottom: 20px;
        }

        /* SELECCIÓN DE HUEVO (EL NACIMIENTO) */
        .element-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
        .element-card {
            background: rgba(0,0,0,0.4); border: 3px solid transparent; border-radius: 15px;
            padding: 20px 10px; text-align: center; cursor: pointer; transition: 0.2s;
        }
        .element-card i { font-size: 3rem; margin-bottom: 10px; }
        .element-card.eau { color: var(--eau); }
        .element-card.feu { color: var(--feu); }
        .element-card.plante { color: var(--plante); }
        .element-card.selected { transform: scale(1.05); background: rgba(255,255,255,0.1); }
        .element-card.eau.selected { border-color: var(--eau); box-shadow: 0 0 20px rgba(52,152,219,0.4); }
        .element-card.feu.selected { border-color: var(--feu); box-shadow: 0 0 20px rgba(231,76,60,0.4); }
        .element-card.plante.selected { border-color: var(--plante); box-shadow: 0 0 20px rgba(46,204,113,0.4); }

        .btn-game {
            background: linear-gradient(45deg, #f1c40f, #f39c12); color: #000; border: none;
            border-radius: 12px; padding: 15px; width: 100%; font-weight: 900; font-size: 1.1rem;
            text-transform: uppercase; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 0 #d35400;
        }
        .btn-game:active { transform: translateY(4px); box-shadow: none; }
        .game-input {
            background: rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.2);
            color: white; padding: 15px; border-radius: 12px; width: 100%; text-align: center;
            font-size: 1.2rem; margin-bottom: 15px; outline: none;
        }

        /* ESTADO DEL DRAGÓN */
        .dragon-stage-container { text-align: center; padding: 30px 0; }
        .dragon-emoji { font-size: 7rem; text-shadow: 0 0 30px rgba(255,255,255,0.2); animation: float 3s ease-in-out infinite; display: inline-block; }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
        
        .xp-container { background: rgba(0,0,0,0.5); border-radius: 20px; height: 30px; position: relative; overflow: hidden; border: 2px solid rgba(255,255,255,0.1); margin: 20px 0; }
        .xp-fill { background: linear-gradient(90deg, var(--plante), var(--eau)); height: 100%; width: 0%; transition: width 0.8s; }
        .xp-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.9rem; text-shadow: 1px 1px 2px black; }

        /* EL DIARIO (LE GRIMOIRE) */
        .mood-selector { display: flex; justify-content: space-between; margin-bottom: 15px; }
        .mood-btn { font-size: 2.5rem; background: rgba(255,255,255,0.05); border: 2px solid transparent; border-radius: 15px; padding: 5px; cursor: pointer; transition: 0.2s; flex: 1; text-align: center; margin: 0 5px; }
        .mood-btn.selected { background: rgba(241, 196, 15, 0.2); border-color: var(--accent); transform: scale(1.1); }
        .journal-entry { background: rgba(0,0,0,0.3); border-left: 4px solid var(--accent); padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        .btn-help { background: rgba(52, 152, 219, 0.2); color: #3498db; border: 1px solid #3498db; border-radius: 8px; padding: 5px 15px; font-size: 0.8rem; font-weight: bold; cursor: pointer; float: right; }

        /* MENÚ INFERIOR */
        .dock-nav { position: fixed; bottom: 0; left: 0; width: 100%; background-color: rgba(15, 20, 30, 0.95); border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-around; padding: 15px 0; z-index: 1000; backdrop-filter: blur(10px); }
        .dock-item { font-size: 1.5rem; color: #7f8fa6; cursor: pointer; transition: 0.2s; text-align: center; }
        .dock-item p { font-size: 0.6rem; margin: 5px 0 0 0; font-weight: bold; text-transform: uppercase; }
        .dock-item.active { color: var(--accent); transform: translateY(-5px); }
    </style>
</head>
<body>

    <!-- 1. NACIMIENTO: ELECCIÓN DEL DRAGÓN -->
    <section id="view-egg" class="view active-view">
        <div class="text-center mt-4 mb-4">
            <h1 style="font-weight: 900; color: var(--accent);">L'ÉCLOSERIE</h1>
            <p>Choisis l'œuf de ton futur dragon</p>
        </div>
        
        <div class="element-grid">
            <div class="element-card eau" onclick="app.selectElement('Eau', this)">
                <i class="fa-solid fa-droplet"></i><h5>Eau</h5><small>Fluide</small>
            </div>
            <div class="element-card feu" onclick="app.selectElement('Feu', this)">
                <i class="fa-solid fa-fire"></i><h5>Feu</h5><small>Énergie</small>
            </div>
            <div class="element-card plante" onclick="app.selectElement('Plante', this)">
                <i class="fa-solid fa-leaf"></i><h5>Plante</h5><small>Nature</small>
            </div>
        </div>

        <div class="solid-panel mt-4">
            <label class="small text-secondary mb-2 fw-bold">NOM DU DRAGON</label>
            <input type="text" id="dragon-name" class="game-input" placeholder="Ex: Aqualis, Ignis...">
            
            <label class="small text-secondary mb-2 fw-bold mt-2">ADN UNIQUE (Atout)</label>
            <select id="dragon-trait" class="game-input">
                <option value="Force">Force (Fuerza)</option>
                <option value="Sagesse">Sagesse (Sabiduría)</option>
                <option value="Vitesse">Vitesse (Velocidad)</option>
                <option value="Créativité">Créativité (Creatividad)</option>
            </select>
        </div>
        
        <button onclick="app.hatchEgg()" class="btn-game mt-2">ÉCLORE L'ŒUF <i class="fa-solid fa-sparkles"></i></button>
    </section>

    <!-- 2. HOME: ESTADO DEL DRAGÓN -->
    <section id="view-home" class="view">
        <div class="d-flex justify-content-between align-items-center mb-2 mt-2">
            <h2 id="display-dname" style="font-weight: 900; margin:0; text-transform: uppercase; color: var(--accent);">NOM</h2>
            <div class="badge bg-dark border border-secondary p-2"><span id="display-element">Élément</span></div>
        </div>
        <p class="text-secondary small fw-bold" id="display-trait">Atout</p>
        
        <div class="solid-panel dragon-stage-container mt-3">
            <h4 id="display-stage" class="text-secondary fw-bold" style="text-transform: uppercase; letter-spacing: 2px;">Stade</h4>
            <!-- VISUAL DEL DRAGÓN -->
            <div id="dragon-visual" class="dragon-emoji my-4">🥚</div>
            
            <div class="xp-container">
                <div id="xp-bar" class="xp-fill"></div>
                <div id="xp-text" class="xp-text">0 / 100 XP</div>
            </div>
            <p class="small text-secondary">Complète des missions et écris dans ton journal pour le faire grandir !</p>
        </div>
    </section>

    <!-- 3. MISIONES -->
    <section id="view-missions" class="view">
        <h2 style="font-weight: 900; color: var(--accent);" class="mb-4">MISSIONS</h2>
        
        <div class="solid-panel">
            <h5 class="fw-bold"><i class="fa-solid fa-qrcode text-info"></i> Codes Secrets ODD</h5>
            <p class="small text-secondary mb-2">Entrez un code donné par le professeur pour gagner de l'XP.</p>
            <div class="d-flex gap-2">
                <input type="text" id="secret-code-input" class="game-input mb-0 text-uppercase" placeholder="CODE..." style="padding:10px;">
                <button onclick="app.validateCode()" class="btn btn-info fw-bold" style="border-radius:12px;">VALIDER</button>
            </div>
        </div>
        <!-- Se pueden añadir más misiones aquí -->
    </section>

    <!-- 4. EL DIARIO RESTAURADO (RECOGIDA DE DATOS CUALITATIVOS) -->
    <section id="view-journal" class="view">
        <h2 style="font-weight: 900; color: var(--accent);" class="mb-4">LE GRIMOIRE</h2>
        
        <div class="solid-panel">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <label class="small text-secondary fw-bold mb-0">COMMENT TE SENS-TU ? (Météo)</label>
                <!-- DUA: Andamiaje cognitivo -->
                <button class="btn-help" onclick="app.helpJournal()"><i class="fa-solid fa-life-ring"></i> Aide ?</button>
            </div>
            
            <!-- REGISTRO EMOCIONAL -->
            <div class="mood-selector mt-3">
                <div class="mood-btn" onclick="app.setMood(this, '🤩')">🤩</div>
                <div class="mood-btn" onclick="app.setMood(this, '😊')">😊</div>
                <div class="mood-btn" onclick="app.setMood(this, '🤔')">🤔</div>
                <div class="mood-btn" onclick="app.setMood(this, '😫')">😫</div>
            </div>
            <input type="hidden" id="journal-mood">
            
            <!-- REFLEXIÓN -->
            <textarea id="journal-text" class="game-input text-start mt-3" rows="4" placeholder="Écris tes réflexions sur le projet aujourd'hui... Tu peux utiliser le Micro d'Or (Sidebar) si tu préfères l'audio !"></textarea>
            
            <button onclick="app.saveJournal()" class="btn-game" style="padding: 10px; font-size: 1rem;">POSTER DANS LE JOURNAL (+20 XP)</button>
        </div>
        
        <h5 class="fw-bold mt-4 mb-3">Mes Mémoires (Historique)</h5>
        <div id="journal-feed"></div>
    </section>

    <!-- NAVBAR INFERIOR -->
    <div id="app-dock" class="dock-nav" style="display:none;">
        <div class="dock-item active" onclick="app.nav('home', this)">
            <i class="fa-solid fa-dragon"></i><p>Dragon</p>
        </div>
        <div class="dock-item" onclick="app.nav('missions', this)">
            <i class="fa-solid fa-khanda"></i><p>Missions</p>
        </div>
        <div class="dock-item" onclick="app.nav('journal', this)">
            <i class="fa-solid fa-book-journal-whills"></i><p>Grimoire</p>
        </div>
    </div>

    <script>
        // --- BASE DE DATOS (Guardado Local en el navegador) ---
        let DB = {
            setup: false,
            dragon: { name: "", element: "", trait: "", xp: 0 },
            journal: []
        };

        // --- SISTEMA DE EVOLUCIÓN (5 FASES) ---
        const EVOLUTION = [
            { maxXP: 100, stage: "Œuf", emojiBase: "🥚" },
            { maxXP: 300, stage: "Bébé", emojiBase: "🦎" },
            { maxXP: 600, stage: "Adolescent", emojiBase: "🦖" },
            { maxXP: 1000, stage: "Adulte", emojiBase: "🐲" },
            { maxXP: 99999, stage: "Légendaire", emojiBase: "🐉" }
        ];

        const app = {
            init: () => {
                const saved = localStorage.getItem("dragon_rpg_db");
                if(saved) DB = JSON.parse(saved);

                if(DB.setup) {
                    app.updateUI();
                    app.showView('view-home');
                    document.getElementById('app-dock').style.display = 'flex';
                }
            },

            save: () => { localStorage.setItem("dragon_rpg_db", JSON.stringify(DB)); },

            // --- ONBOARDING ---
            selectElement: (el, card) => {
                document.querySelectorAll('.element-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                DB.dragon.element = el;
            },

            hatchEgg: () => {
                const name = document.getElementById('dragon-name').value.trim();
                const trait = document.getElementById('dragon-trait').value;
                if(!name || !DB.dragon.element) return alert("Choisis un élément et un nom !");
                
                DB.dragon.name = name;
                DB.dragon.trait = trait;
                DB.dragon.xp = 0;
                DB.setup = true;
                
                app.save();
                confetti();
                app.updateUI();
                app.showView('view-home');
                document.getElementById('app-dock').style.display = 'flex';
            },

            // --- LÓGICA DE EVOLUCIÓN Y UI ---
            updateUI: () => {
                document.getElementById('display-dname').innerText = DB.dragon.name;
                document.getElementById('display-element').innerText = DB.dragon.element;
                document.getElementById('display-trait').innerText = `Atout: ${DB.dragon.trait}`;
                
                // Calcular Fase actual según XP
                let currentStage = EVOLUTION[0];
                let prevMaxXP = 0;
                
                for(let i=0; i<EVOLUTION.length; i++) {
                    if(DB.dragon.xp < EVOLUTION[i].maxXP) {
                        currentStage = EVOLUTION[i];
                        break;
                    }
                    prevMaxXP = EVOLUTION[i].maxXP;
                }

                document.getElementById('display-stage').innerText = currentStage.stage;
                document.getElementById('dragon-visual').innerText = currentStage.emojiBase;
                
                // Color y efectos visuales según elemento
                let color = "white";
                if(DB.dragon.element === 'Eau') color = "var(--eau)";
                if(DB.dragon.element === 'Feu') color = "var(--feu)";
                if(DB.dragon.element === 'Plante') color = "var(--plante)";
                document.getElementById('dragon-visual').style.textShadow = `0 0 40px ${color}`;
                document.getElementById('display-element').style.color = color;
                
                // Color de la barra de XP
                document.getElementById('xp-bar').style.background = `linear-gradient(90deg, #555, ${color})`;

                // Calcular porcentaje de XP para el nivel actual
                let levelXP = DB.dragon.xp - prevMaxXP;
                let levelMax = currentStage.maxXP - prevMaxXP;
                let pct = Math.min((levelXP / levelMax) * 100, 100);
                
                document.getElementById('xp-bar').style.width = pct + "%";
                document.getElementById('xp-text').innerText = `${DB.dragon.xp} / ${currentStage.maxXP} XP`;
            },

            addXP: (pts) => {
                DB.dragon.xp += pts;
                app.save();
                app.updateUI();
                confetti({particleCount: 50, spread: 60});
            },

            // --- NAVEGACIÓN ---
            nav: (view, btn) => {
                document.querySelectorAll('.dock-item').forEach(i => i.classList.remove('active'));
                btn.classList.add('active');
                app.showView('view-' + view);
                if(view === 'journal') app.renderJournal();
            },
            showView: (id) => {
                document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
                document.getElementById(id).classList.add('active-view');
            },

            // --- VALIDACIÓN DE MISIONES POR CÓDIGO ---
            validateCode: () => {
                const code = document.getElementById('secret-code-input').value.trim().toUpperCase();
                // Ejemplos de códigos secretos para XP
                if(code === "FRANCAIS2030" || code === "ODD13" || code === "DRAGON") {
                    alert("Mission accomplie ! +50 XP");
                    app.addXP(50);
                    document.getElementById('secret-code-input').value = "";
                } else {
                    alert("Code incorrect.");
                }
            },

            // --- DIARIO METACOGNITIVO Y CUALITATIVO (DUA) ---
            setMood: (btn, m) => {
                document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                document.getElementById('journal-mood').value = m;
            },
            helpJournal: () => {
                // DUA: Andamiaje cognitivo (estructuras de frases prefabricadas)[cite: 2]
                const box = document.getElementById('journal-text');
                box.value = "Aujourd'hui, je me sens... parce que... \\n\\nMon point fort a été... \\n\\nJ'ai eu des difficultés avec...";
            },
            saveJournal: () => {
                const mood = document.getElementById('journal-mood').value;
                const txt = document.getElementById('journal-text').value;
                if(!mood || !txt) return alert("N'oublie pas ton humeur (émoji) et ton texte !");
                
                const entry = { date: new Date().toLocaleDateString(), mood: mood, text: txt };
                DB.journal.unshift(entry);
                
                // Bonificación de XP por reflexión[cite: 2]
                app.addXP(20); 
                app.save();
                app.renderJournal();
                
                // Limpiar inputs
                document.getElementById('journal-text').value = "";
                document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
                document.getElementById('journal-mood').value = "";
            },
            renderJournal: () => {
                const feed = document.getElementById('journal-feed');
                feed.innerHTML = "";
                DB.journal.forEach(j => {
                    feed.innerHTML += `
                        <div class="journal-entry">
                            <div class="d-flex justify-content-between mb-2">
                                <span class="fw-bold" style="color: var(--accent);">${j.date}</span>
                                <span style="font-size: 1.5rem;">${j.mood}</span>
                            </div>
                            <p class="mb-0 small">${j.text.replace(/\\n/g, '<br>')}</p>
                        </div>
                    `;
                });
            }
        };

        app.init();
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
