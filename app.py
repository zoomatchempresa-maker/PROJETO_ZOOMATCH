import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# --- 🎨 ESTILIZAÇÃO VISUAL (Design Premium e Limpo) ---
st.markdown("""
    <style>
    /* Fundo Principal */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.55); z-index: -1;
    }
    
    /* Títulos */
    .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); margin-bottom: 5px; }
    .sub-title { text-align: center; color: #fdfdfd; font-size: 20px; font-weight: 400; text-shadow: 2px 2px 5px rgba(0,0,0,0.7); margin-bottom: 40px; }
    
    /* Card de Conteúdo */
    .content-card { 
        background-color: rgba(255, 255, 255, 0.98); 
        padding: 30px; 
        border-radius: 20px; 
        color: #1b4332; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); 
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Estilização dos Inputs (Bonito e Sem Bugs) */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #f8f9fa !important;
        border: 2px solid #e9ecef !important;
        border-radius: 12px !important;
        color: #1b4332 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2d6a4f !important;
        box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.2) !important;
        background-color: #ffffff !important;
    }

    /* Labels */
    label {
        color: #2d6a4f !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
    }

    /* Botões Premium */
    div.stButton > button { 
        background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%) !important;
        color: white !important; 
        border-radius: 12px !important; 
        font-weight: bold !important; 
        padding: 12px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        filter: brightness(1.1);
    }
    
    /* Expander e Mensagens */
    .streamlit-expanderHeader { background-color: #f1f8f5 !important; border-radius: 10px !important; color: #1b4332 !important; font-weight: bold !important; }
    .stAlert { border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados e Configurações
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Pets", "Nutrição Animal", "Melhoramento Genético", "Pastagens"],
    "Médico Veterinário": ["Reprodução e IATF", "Sanidade Animal", "Clínica de Grandes", "Clínica de Pequenos (Pets)", "Cirurgia", "Inspeção de Origem Animal"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Fruticultura", "Olericultura", "Manejo de Solos", "Fitossanidade", "Tecnologia de Aplicação", "Irrigação"],
    "Engenheiro Ambiental": ["Licenciamento Ambiental", "CAR", "Outorga de Água", "Recuperação de Áreas Degradadas", "Gestão de Resíduos", "Sustentabilidade/ESG"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventário Florestal", "Sistemas Agroflorestais", "Produção de Mudas"]
}
SENHA_MESTRA = "Z00-M4tch-2026#Px"

# 3. Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None: df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# 4. Títulos
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

# --- PÁGINAS ---
if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 O Agro conectado</h2><p>Escolha uma opção no menu lateral para começar sua jornada.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_final_clean"):
        nome = st.text_input("Nome Completo")
        
        c1, c2 = st.columns(2)
        with c1:
            label_reg = "CRMV" if prof_escolhida in ["Zootecnista", "Médico Veterinário"] else "CREA"
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
            
        bio = st.text_area("Descreva sua experiência")
        
        if st.form_submit_button("Finalizar Cadastro"):
            if nome and contato and especialidades:
                novo = pd.DataFrame([{"Nome": nome, "Profissão": prof_escolhida, "Registro": registro, "Especialidades": ", ".join(especialidades), "Contato": contato, "Pretensão": pretensao, "Bio": bio}])
                conn.update(data=pd.concat([carregar_dados(), novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✨ Perfil cadastrado com sucesso!")
            else:
                st.warning("⚠️ Preencha os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if
