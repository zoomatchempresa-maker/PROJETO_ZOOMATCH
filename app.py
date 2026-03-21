import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# CSS Profissional
st.markdown("""
    <style>
    .stApp { background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop"); background-size: cover; background-position: center; background-attachment: fixed; }
    .stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.55); z-index: -1; }
    .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); }
    .content-card { background-color: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 20px; color: #1b4332; box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# Dados Técnicos
MAPA_AGRO = {
    "Zootecnista": ["Bovinocultura de Corte", "Bovinocultura de Leite", "Avicultura", "Suinocultura", "Nutrição Animal", "Melhoramento Genético", "Pastagens"],
    "Médico Veterinário": ["Reprodução Animal", "Sanidade", "Clínica de Grandes", "Cirurgia", "Inspeção"],
    "Engenheiro Agrônomo": ["Grãos (Soja/Milho)", "Fruticultura", "Solos", "Fitossanidade", "Irrigação"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado", ESTADOS)
        registro = st.text_input("Registro (CRMV/CREA)")
        especialidades = st.multiselect("Especialidades", MAPA_AGRO[prof_escolhida])
        contato = st.text_input("WhatsApp (ex: 5581999998888)")
        pretensao = st.number_input("Pretensão Salarial", min_value=0)
        bio = st.text_area("Bio/Resumo")
        
        if st.form_submit_button("Publicar Perfil"):
            if nome and contato and especialidades:
                try:
                    df_atual = carregar_dados()
                    novo = pd.DataFrame([{
                        "Nome": nome, "Profissão": prof_escolhida, "Estado": estado,
                        "Registro": registro, "Especialidades": ", ".join(especialidades),
                        "Contato": contato, "Pretensão": pretensao, "Bio": bio
                    }])
                    df_final = pd.concat([df_atual, novo], ignore_index=True)
                    conn.update(data=df_final)
                    st.cache_data.clear()
                    st.success("✅ Perfil publicado!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar. Verifique se o e-mail do secrets é EDITOR na planilha.")
            else:
                st.warning("Preencha os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)
