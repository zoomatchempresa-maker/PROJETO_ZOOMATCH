import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# --- 🎨 ESTILIZAÇÃO VISUAL ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.6); z-index: -1;
    }
    .main-title { color: white; text-align: center; font-size: 50px; font-weight: 900; text-shadow: 4px 4px 10px black; }
    .sub-title { text-align: center; color: #f0f0f0; font-size: 18px; text-shadow: 2px 2px 5px black; margin-bottom: 30px; }
    .content-card { background-color: rgba(255, 255, 255, 0.98); padding: 25px; border-radius: 15px; color: #1b4332; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
    div.stButton > button { background-color: #2d6a4f !important; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Mapa de Especialidades (Sincronizado e Corrigido)
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Pets", "Nutrição Animal", "Melhoramento Genético"],
    "Médico Veterinário": ["Clínica de Grandes", "Clínica de Pequenos (Pets)", "Reprodução", "Sanidade Animal", "Cirurgia", "Inspeção de Alimentos"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Hortifrúti", "Solo e Adubação", "Irrigação", "Defensivos Agrícolas"],
    "Engenheiro Florestal": ["Reflorestamento", "Manejo Sustentável", "Recuperação de Áreas", "Inventário Florestal", "Silvicultura"]
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

# 4. Interface Principal
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 Bem-vindo ao AgroMatch</h2><p>O hub de talentos para o agronegócio moderno. Cadastre seu perfil ou encontre o especialista ideal para sua propriedade.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
        
        c1, c2 = st.columns(2)
        with c1:
            label_reg = "CRMV" if "Veterinário" in prof_escolhida or "Zootecnista" in prof_escolhida else "CREA"
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            # Pega as especialidades certas baseadas na profissão acima
            lista_esp = MAPA_AGRO[prof_escolhida]
            especialidades = st.multiselect("Suas Especialidades", lista_esp)
            pretensao = st.number_input("Pretensão Salarial (R$)", min_value=0)
            
        bio = st.text_area("Resumo de Qualificações")
        
        if st.form_submit_button("Cadastrar Perfil"):
            if nome and contato and especialidades:
                novo_df = pd.DataFrame([{
                    "Nome": nome, "Profissão": prof_escolhida, "Registro": registro,
                    "Especialidades": ", ".join(especialidades), "Contato": contato,
                    "Pretensão": pretensao, "Bio": bio
                }])
                conn.update(data=pd.concat([carregar_dados(), novo_df], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil publicado com sucesso!")
            else:
                st.warning("Preencha todos os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Área do Produtor")
        senha = st.text_input("Senha de Acesso", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Acessar"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha incorreta")
        with c2:
            # TROQUE PELO SEU NÚMERO
            seu_whatsapp = "5581999998888" 
            st.link_button("🔑 Solicitar Senha", f"https://wa.me/{seu_whatsapp}?text=Quero%20a%20senha%20do%20AgroMatch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Buscar Profissionais")
        
        p_busca = st.selectbox("Qual profissional você procura?", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        
        esp_filtro = "Todas"
        if p_busca != "Ver Todos":
            # Filtro dinâmico: mostra as especialidades da profissão selecionada
            esp_filtro = st.selectbox(f"Especialidade em {p_busca}:", ["Todas"] + MAPA_AGRO[p_busca])
        
        dados = carregar_dados()
        if not dados.empty:
            df_final = dados
