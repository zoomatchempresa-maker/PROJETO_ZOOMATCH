import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🚜", layout="centered")

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
    .content-card { background-color: rgba(255, 255, 255, 0.98); padding: 25px; border-radius: 15px; color: #1b4332; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
    div.stButton > button { background-color: #2d6a4f !important; color: white !important; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão e Dados
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None: df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

SENHA_MESTRA = "Z00-M4tch-2026#Px"
profissoes = ["Zootecnista", "Médico Veterinário", "Engenheiro Agrônomo", "Engenheiro Florestal"]

especialidades_map = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Nutrição Animal", "Melhoramento Genético"],
    "Médico Veterinário": ["Clínica de Grandes", "Reprodução", "Sanidade Animal", "Cirurgia", "Inspeção de Alimentos"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Hortifrúti", "Solo e Adubação", "Irrigação", "Defensivos"],
    "Engenheiro Florestal": ["Reflorestamento", "Manejo Sustentável", "Recuperação de Áreas", "Inventário Florestal"]
}

# 3. Cabeçalho
st.markdown("<div class='main-title'>🌱 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>O Ponto de Encontro do Profissional do Campo</div>", unsafe_allow_html=True)

# 4. Menu Lateral
menu = st.sidebar.selectbox("📍 Menu", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Talentos"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 Conectando Talentos ao Agronegócio</h2><p>Seja você um especialista ou um produtor, o AgroMatch é o lugar onde a tecnologia encontra a prática no campo.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Seu Perfil Profissional")
    with st.form("form_agro"):
        nome = st.text_input("Nome Completo")
        prof = st.selectbox("Sua Profissão", profissoes)
        
        c1, c2 = st.columns(2)
        with c1:
            label_registro = "CRMV" if "Veterinário" in prof or "Zootecnista" in prof else "CREA"
            registro = st.text_input(f"Registro Profissional ({label_registro})")
            contato = st.text_input("WhatsApp (DDD + Número)")
        with c2:
            esp = st.multiselect("Suas Especialidades", especialidades_map[prof])
            pretenso = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
            
        bio = st.text_area("Resumo de Qualificações e Experiências")
        
        if st.form_submit_button("Finalizar Cadastro"):
            if nome and contato and esp:
                novo = pd.DataFrame([{"Nome": nome, "Profissão": prof, "Registro": registro, "Especialidades": ", ".join(esp), "Contato": contato, "Pretensão": pretenso, "Bio": bio}])
                conn.update(data=pd.concat([carregar_dados(), novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil publicado com sucesso!")
            else: st.warning("Preencha Nome, Contato e Especialidades.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Talentos":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Acesso ao Produtor")
        senha = st.text_input("Senha de Acesso", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Entrar"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha incorreta")
        with c2:
            # AJUSTE SEU WHATSAPP AQUI
            seu_zap = "5581999998888"
            st.link_button("🔑 Solicitar Senha", f"https://wa.me/{seu_zap}?text=Quero%20acesso%20ao%20AgroMatch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 O que você procura hoje?")
        
        # FILTRO DUPLO
        prof_busca = st.selectbox("Selecione a Profissão:", ["Ver Todos"] + profissoes)
        
        if prof_busca != "Ver Todos":
            esp_busca = st.selectbox(f"Qual especialidade em {prof_busca}?", ["Todas"] + especialidades_map[prof_busca])
        
        dados = carregar_dados()
        if not dados.empty:
            df_f = dados
            if prof_busca != "Ver Todos":
                df_f = df_f[df_f['Profissão'] == prof_busca]
                if esp_busca != "Todas":
                    df_f = df_f[df_f['Especialidades'].str.contains(esp_busca, na=False)]
            
            st.write(f"--- {len(df_f)} profissionais encontrados ---")
            for i, r in df_f.iterrows():
                with st.expander(f"{r['Nome']} - {r['Profissão']}"):
                    st.write(f"📌 **Especialidades:** {r['Especialidades']}")
                    st.write(f"💳 **Registro:** {r['Registro']}")
                    st.write(f"💰 **Pretensão:** R$ {r['Pretensão']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    st.link_button(f"💬 Falar com {r['Nome']}", f"https://wa.me/55{str(r['Contato']).replace('.0','').strip()}")
        st.markdown("</div>", unsafe_allow_html=True)
