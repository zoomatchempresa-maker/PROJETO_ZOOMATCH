import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🌱", layout="centered")

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

# 2. Configuração de Inteligência (Dicionário Único)
# O que você alterar aqui, muda no site inteiro automaticamente!
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Nutrição Animal", "Melhoramento Genético"],
    "Médico Veterinário": ["Clínica de Grandes", "Reprodução", "Sanidade Animal", "Cirurgia", "Inspeção de Alimentos"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Hortifrúti", "Solo e Adubação", "Irrigação", "Defensivos"],
    "Engenheiro Florestal": ["Reflorestamento", "Manejo Sustentável", "Recuperação de Áreas", "Inventário Florestal"]
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
st.markdown("<div class='main-title'>🌱 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 Bem-vindo ao AgroMatch</h2><p>A maior vitrine de profissionais técnicos para o agronegócio. Escolha uma opção no menu lateral para começar.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro de Profissional")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        prof_escolhida = st.selectbox("Sua Profissão", list(MAPA_AGRO.keys()))
        
        c1, c2 = st.columns(2)
        with c1:
            label_reg = "CRMV" if "Veterinário" in prof_escolhida or "Zootecnista" in prof_escolhida else "CREA"
            registro = st.text_input(f"Registro Profissional ({label_reg})")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            # Aqui o profissional vê EXATAMENTE as especialidades da profissão dele
            especialidades = st.multiselect("Suas Especialidades", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial (R$)", min_value=0)
            
        bio = st.text_area("Resumo de Experiências")
        
        if st.form_submit_button("Finalizar Cadastro"):
            if nome and contato and especialidades:
                novo_df = pd.DataFrame([{
                    "Nome": nome, "Profissão": prof_escolhida, "Registro": registro,
                    "Especialidades": ", ".join(especialidades), "Contato": contato,
                    "Pretensão": pretensao, "Bio": bio
                }])
                conn.update(data=pd.concat([carregar_dados(), novo_df], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil cadastrado com sucesso!")
            else:
                st.warning("Preencha Nome, Contato e selecione as Especialidades.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Acesso Restrito")
        senha = st.text_input("Senha do Produtor", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Acessar Banco"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha inválida")
        with c2:
            # NÃO ESQUEÇA DE TROCAR O NÚMERO ABAIXO PARA O SEU REAL
            seu_whatsapp = "5581999998888" 
            link_suporte = f"https://wa.me/{seu_whatsapp}?text=Olá,%20gostaria%20da%20senha%20do%20AgroMatch"
            st.link_button("🔑 Solicitar Senha", link_suporte)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Filtros de Busca")
        
        prof_busca = st.selectbox("Quem você procura?", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        
        # Filtro de especialidade dinâmico baseado na profissão
        esp_busca = "Todas"
        if prof_busca != "Ver Todos":
            esp_busca = st.selectbox(f"Especialidade em {prof_busca}:", ["Todas"] + MAPA_AGRO[prof_busca])
        
        dados = carregar_dados()
        if not dados.empty:
            df_filtrado = dados
            if prof_busca != "Ver Todos":
                df_filtrado = df_filtrado[df_filtrado['Profissão'] == prof_busca]
                if esp_busca != "Todas":
                    df_filtrado = df_filtrado[df_filtrado['Especialidades'].str.contains(esp_busca, na=False)]
            
            st.info(f"Encontramos {len(df_filtrado)} profissionais para você.")
            
            for _, r in df_filtrado.iterrows():
                with st.expander(f"{r['Nome']} ({r['Profissão']})"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"💳 **{label_reg}:** {r['Registro']}")
                    st.write(f"💰 **Pretensão:** R$ {r['Pretensão']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    zap_final = "https://wa.me/55" + str(r['Contato']).replace(".0","").strip()
                    st.link_button(f"💬 Conversar com {r['Nome']}", zap_final)
        st.markdown("</div>", unsafe_allow_html=True)
