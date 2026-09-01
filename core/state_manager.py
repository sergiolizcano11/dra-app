import streamlit as st
import random

def init_state():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'setup_complete': False,
            'nombre': 'Apprenti',
            'elemento': 'Fuego',
            'nivel': 1,
            'xp': 0,
            'xp_next': 50,
            'fase_actual': 'Éveil',
            'view': 'Home'
        }
        
    if 'memory_game' not in st.session_state:
        st.session_state.memory_game = {
            'cards': [],
            'flipped': [],
            'matched': set(),
            'game_over': False,
            'initialized': False
        }

def get_assets():
    return {
        "Fuego": {
            "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880228.png", 
            "Expansion": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", 
            "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203150.png",
            "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699313.png"
        },
        "Agua": {
            "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", 
            "Expansion": "https://cdn-icons-png.flaticon.com/512/3093/3093608.png", 
            "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203158.png"
        },
        "Naturaleza": {
            "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880233.png", 
            "Expansion": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png", 
            "Repli": "https://cdn-icons-png.flaticon.com/512/4203/4203164.png"
        }
    }
