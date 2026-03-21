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

# 2. Mapa de Especialidades TÉCNICAS (Corrigido por Área)
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Pets", "Nutrição Animal", "Melhoramento Genético", "Gestão de Pastagens"],
    "Médico Veterinário": ["Reprodução e IATF", "Sanidade Animal", "Clínica de Grandes", "Clínica de Pequenos (Pets)", "Cirurgia", "Inspeção de Produtos de Origem Animal"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Fruticultura", "Olericultura", "Manejo de Solos e Adubação", "Fitossanidade (Pragas/Doenças)", "Tecnologia de Aplicação", "Irrigação e Drenagem"],
    "Engenheiro Ambiental": ["Licenciamento Ambiental", "CAR (Cadastro Ambiental Rural)", "Outorga de Água", "Recuperação de Áreas Degradadas", "Gestão de Resíduos Agrícolas", "Sustentabilidade/ESG no Campo"],
    "Engenheiro Florestal": ["Silvicultura (Eucalipto/Pinus)", "Manejo Florestal Sustentável", "Inventário Florestal", "Sistemas Agroflorestais", "Produção de Mudas", "Exploração Florestal"]
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

# 4. Interface
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Hub de Especialistas para o Agronegócio</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 O Agro em um só lugar</h2><p>Conectando Agrônomos, Veterinários, Zootecnistas e Engenheiros aos produtores que buscam excelência técnica.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Seu Perfil Técnico")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
        
        c1, c2 = st.columns(2)
        with c1:
            # Lógica de Registro Profissional
            if prof_escolhida in ["Zootecnista", "Médico Veterinário"]:
                label_reg = "CRMV"
            else:
                label_reg = "CREA"
            
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            # LISTA DINÂMICA: Muda conforme a profissão escolhida!
            especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
            
        bio = st.text_area("Descreva suas principais experiências e cursos")
        
        if st.form_submit_button("Finalizar e Publicar"):
            if nome and contato and especialidades:
                novo_df = pd.DataFrame([{
                    "Nome": nome, "Profissão": prof_escolhida, "Registro": registro,
                    "Especialidades": ", ".join(especialidades), "Contato": contato,
                    "Pretensão": pretensao, "Bio": bio
                }])
                conn.update(data=pd.concat([carregar_dados(), novo_df], ignore_index=True))
                st.cache_data.clear()
                st.success(f"✅ Perfil de {prof_escolhida} cadastrado com sucesso!")
            else:
                st.warning("Por favor, preencha Nome, WhatsApp e Especialidades.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Acesso do Produtor")
        senha = st.text_input("Digite a Senha de Acesso", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Liberar Banco"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha incorreta")
        with c2:
            # Lembre-se de colocar SEU NÚMERO abaixo
            seu_whatsapp = "5581999998888" 
            st.link_button("🔑 Solicitar Senha", f"https://wa.me/{seu_whatsapp}?text=Gostaria%20da%20senha%20do%20AgroMatch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Buscar Profissionais")
        
        p_busca = st.selectbox("Qual profissional você procura?", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        
        esp_filtro = "Todas"
        if p_busca != "Ver Todos":
            # Filtro dinâmico na busca também!
            esp_filtro = st.selectbox(f"Especialidade em {p_busca}:", ["Todas"] + MAPA_AGRO[p_busca])
        
        dados = carregar_dados()
        if not dados.empty:
            df_final = dados
            if p_busca != "Ver Todos":
                df_final = df_final[df_final['Profissão'] == p_busca]
                if esp_filtro != "Todas":
                    df_final = df_final[df_final['Especialidades'].str.contains(esp_filtro, na=False)]
            
            st.info(f"Encontramos {len(df_final)} profissionais.")
            
            for _, r in df_final.iterrows():
                with st.expander(f"👤 {r['Nome']} - {r['Profissão']}"):
                    st.write(f"🌟 **Foco Técnico:** {r['Especialidades']}")
                    st.write(f"💳 **Registro:** {r['Registro']}")
                    st.write(f"💰 **Pretensão:** R$ {r['Pretensão']}")
                    st.write(f"📝 **Resumo:** {r['Bio']}")
                    zap = "https://wa.me/55" + str(r['Contato']).replace(".0","").strip()
                    st.link_button(f"💬 Contatar {r['Nome']}", zap)
        st.markdown("</div>", unsafe_allow_html=True)
