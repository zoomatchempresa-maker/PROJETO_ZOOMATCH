import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="ZooMatch", page_icon="🐄", layout="centered")

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
    .main-title { color: white; text-align: center; font-size: 55px; font-weight: 900; text-shadow: 4px 4px 10px black; }
    .sub-title { text-align: center; color: #f0f0f0; font-size: 20px; text-shadow: 2px 2px 5px black; margin-bottom: 30px; }
    .welcome-box {
        background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(12px); padding: 35px; 
        border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2); text-align: center; margin-bottom: 30px;
    }
    div.stButton > button { background-color: #2d6a4f !important; color: white !important; border-radius: 10px; font-weight: bold; height: 3em; width: 100%; }
    [data-testid="stSidebar"] { background-color: #1b4332; }
    [data-testid="stSidebar"] * { color: white !important; }
    .content-card { background-color: rgba(255, 255, 255, 0.98); padding: 25px; border-radius: 15px; color: #1b4332; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None: df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Formação", "Espécie de interesse", "Pretensão Salarial", "Contato", "Biografia"])

especies_lista = ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos"]
SENHA_MESTRA = "Z00-M4tch-2026#Px"

# 3. Cabeçalho
st.markdown("<div class='main-title'>🐄 ZooMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Zootecnistas e Produtores Rurais</div>", unsafe_allow_html=True)

# 4. Menu
menu = st.sidebar.selectbox("📍 Menu", ["🏠 Início", "🎓 Cadastro Zootecnista", "🚜 Buscar Profissionais"])

if menu == "🏠 Início":
    st.markdown('<div class="welcome-box"><div style="color:white; font-size:30px; font-weight:bold;">🏆 Bem-vindo ao ZooMatch!</div><div style="color:white; font-size:18px;">Conectamos o conhecimento técnico da Zootecnia com as necessidades reais do produtor rural.</div></div>', unsafe_allow_html=True)

elif menu == "🎓 Cadastro Zootecnista":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📝 Cadastro Profissional")
    with st.form("form_zoo"):
        nome = st.text_input("Nome Completo")
        c1, c2 = st.columns(2)
        with c1:
            formacao = st.selectbox("Formação", ["Graduado", "Mestre", "Doutor"])
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            pretensao = st.number_input("Pretensão Salarial", min_value=0)
            especies = st.multiselect("Especialidades", especies_lista)
        bio = st.text_area("Resumo Profissional")
        if st.form_submit_button("Cadastrar"):
            if nome and contato and especies:
                novo = pd.DataFrame([{"Nome": nome, "Formação": formacao, "Espécie de interesse": ", ".join(especies), "Pretensão Salarial": pretensao, "Contato": contato, "Biografia": bio}])
                conn.update(data=pd.concat([carregar_dados(), novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Cadastrado com sucesso!")
            else: st.warning("Por favor, preencha os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Profissionais":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🚜 Área do Produtor")
        st.subheader("🔒 Acesso Restrito")
        senha = st.text_input("Digite a Senha de Acesso", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Liberar Banco"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha incorreta!")
        with col2:
            # COLOQUE SEU WHATSAPP ABAIXO (Apenas números com DDD)
            seu_whatsapp = "5581999046156" 
            msg = "Olá! Gostaria de solicitar a senha de acesso ao ZooMatch."
            link_zap = f"https://wa.me/{seu_whatsapp}?text={msg.replace(' ', '%20')}"
            st.link_button("🔑 Solicitar Senha", link_zap)
            
        st.info("Somente produtores autorizados podem visualizar os contatos.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Banco de Talentos")
        dados = carregar_dados()
        if not dados.empty:
            f = st.selectbox("Filtrar por Especialidade:", ["Todos"] + especies_lista)
            df_f = dados[dados['Espécie de interesse'].astype(str).str.contains(f, case=False, na=False)] if f != "Todos" else dados
            for i, r in df_f.iterrows():
                with st.expander(str(r['Nome'])):
                    st.write("🎓 Formação: " + str(r['Formação']))
                    st.write("💰 Pretensão: R$ " + str(r['Pretensão Salarial']))
                    st.write("📝 Bio: " + str(r['Biografia']))
                    link_final = "https://wa.me/55" + str(r['Contato']).replace(".0","").strip()
                    st.link_button("💬 Entrar em contato", link_final)
        st.markdown("</div>", unsafe_allow_html=True)
