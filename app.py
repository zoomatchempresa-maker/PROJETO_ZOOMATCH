import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch | O Elo do Campo", page_icon="🐄", layout="centered")

# --- 🎨 DESIGN PROFISSIONAL (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.6); z-index: -1;
    }
    .main-title { 
        color: white; text-align: center; font-size: 52px; font-weight: 900; 
        text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0;
    }
    .sub-title { 
        text-align: center; color: #fdfdfd; font-size: 20px; 
        text-shadow: 2px 2px 5px rgba(0,0,0,0.7); margin-bottom: 40px; 
    }
    .content-card { 
        background-color: rgba(255, 255, 255, 0.95); 
        padding: 35px; border-radius: 20px; color: #1b4332; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 30px;
    }
    /* Estilo dos Botões */
    .stButton>button {
        width: 100%; background-color: #2d6a4f; color: white;
        border-radius: 10px; height: 50px; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #1b4332; color: #d8f3dc; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ LÓGICA DE DADOS ---
MAPA_AGRO = {
    "Zootecnista": ["Bovinos de Corte", "Bovinos de Leite", "Avicultura", "Suinocultura", "Piscicultura", "Nutrição Animal", "Melhoramento Genético", "Pastagens"],
    "Médico Veterinário": ["Reprodução/IATF", "Sanidade Animal", "Clínica de Grandes", "Clínica de Pequenos", "Cirurgia", "Inspeção"],
    "Engenheiro Agrônomo": ["Grãos (Soja/Milho)", "Fruticultura", "Manejo de Solos", "Fitossanidade", "Irrigação", "Mecanização"],
    "Engenheiro Ambiental": ["Licenciamento", "CAR/Georreferenciamento", "Gestão de Resíduos"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- 🏠 INTERFACE PRINCIPAL ---
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Seu Perfil Técnico")
    
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_agro"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
            estado = st.selectbox("Estado (UF)", ESTADOS)
            contato = st.text_input("WhatsApp (Ex: 5581999998888)")
        with col2:
            registro = st.text_input("Registro (CRMV/CREA)")
            pretensao = st.number_input("Pretensão Salarial (R$)", min_value=0)
            especialidades = st
