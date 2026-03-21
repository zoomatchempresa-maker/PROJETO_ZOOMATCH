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
        background-color: rgba(0, 0, 0, 0.55); z-index: -1;
    }
    .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); }
    .sub-title { text-align: center; color: #fdfdfd; font-size: 20px; text-shadow: 2px 2px 5px rgba(0,0,0,0.7); margin-bottom: 40px; }
    .content-card { 
        background-color: rgba(255, 255, 255, 0.98); 
        padding: 30px; border-radius: 20px; color: #1b4332; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #f8f9fa !important; border: 2px solid #d1d8d5 !important; border-radius: 10px !important; color: #1b4332 !important;
    }
    div.stButton > button { 
        background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%) !important;
        color: white !important; border-radius: 10px !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados de Apoio
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Pets", "Nutrição Animal", "Melhoramento Genético", "Pastagens"],
    "Médico Veterinário": ["Reprodução e IATF", "Sanidade Animal", "Clínica de Grandes", "Clínica de Pequenos (Pets)", "Cirurgia", "Inspeção de Origem Animal"],
    "Engenheiro Agrônomo": ["Grandes Culturas (Soja/Milho)", "Fruticultura", "Olericultura", "Manejo de Solos", "Fitossanidade", "Tecnologia de Aplicação", "Irrigação"],
    "Engenheiro Ambiental": ["Licenciamento Ambiental", "CAR", "Outorga de Água", "Recuperação de Áreas Degradadas", "Gestão de Resíduos", "Sustentabilidade/ESG"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventário Florestal", "Sistemas Agroflorestais", "Produção de Mudas"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
SENHA_MESTRA = "Z00-M4tch-2026#Px"

# 3. Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None:
            df.columns = df.columns.str.strip()
            # Garante que a coluna Contato seja lida como texto para não virar número quebrado
            df['Contato'] = df['Contato'].astype(str).str.replace('.0', '', regex=False).str.strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# 4. Títulos
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 O Agro conectado</h2><p>Encontre o profissional ideal para sua fazenda.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_agro"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado (UF)", ESTADOS)
        c1, c2 = st.columns(2)
        with c1:
            label_reg = "CRMV" if prof_escolhida in ["Zootecnista", "Médico Veterinário"] else "CREA"
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        with c2:
            especialidades = st.multiselect("Especialidades", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial (R$)", min_value=0)
        bio = st.text_area("Sua Bio")
        
        if st.form_submit_button("Finalizar Cadastro"):
            if nome and contato and especialidades:
                novo = pd.DataFrame([{"Nome": nome, "Profissão": prof_escolhida, "Estado": estado, "Registro": registro, "Especialidades": ", ".join(especialidades), "Contato": contato, "Pretensão": pretensao, "Bio": bio}])
                conn.update(data=pd.concat([carregar_dados(), novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Cadastrado!")
            else: st.warning("Preencha os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Área do Produtor")
        senha = st.text_input("Senha", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Acessar"):
                if senha == SENHA_MESTRA:
                    st.session_state["auth"] = True
                    st.rerun()
                else: st.error("Senha incorreta")
        with c2:
            seu_whatsapp = "5581999998888" # <--- MUDE PARA O SEU NÚMERO
            st.link_button("🔑 Solicitar Senha", f"https://wa.me/{seu_whatsapp}?text=Senha%20AgroMatch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Buscar Profissionais")
        
        p_busca = st.selectbox("Profissão:", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        uf_busca = st.selectbox("Estado (UF):", ["Brasil Inteiro"] + ESTADOS)
        
        # Filtro de Especialidade Dinâmico
        esp_filtro = "Todas"
        if p_busca != "Ver Todos":
            esp_filtro = st.selectbox(f"Especialidade em {p_busca}:", ["Todas"] + MAPA_AGRO[p_busca])
        
        dados = carregar_dados()
        if not dados.empty:
            # --- FILTRAGEM REAL ---
            df_filtrado = dados.copy()
            
            if p_busca != "Ver Todos":
                df_filtrado = df_filtrado[df_filtrado['Profissão'] == p_busca]
            
            if uf_busca != "Brasil Inteiro":
                df_filtrado = df_filtrado[df_filtrado['Estado'] == uf_busca]
                
            if esp_filtro != "Todas":
                df_filtrado = df_filtrado[df_filtrado['Especialidades'].str.contains(esp_filtro, na=False)]
            
            st.info(f"📊 Encontramos {len(df_filtrado)} profissionais.")
            
            for _, r in df_filtrado.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"💼 **Profissão:** {r['Profissão']}")
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"💰 **Pretensão:** R$ {r['Pretensão']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    
                    # Link direto para o WhatsApp do profissional cadastrado
                    numero_limpo = str(r['Contato']).strip()
                    # Se o número não começar com 55, o código adiciona automaticamente
                    if not numero_limpo.startswith('55'):
                        numero_limpo = '55' + numero_limpo
                        
                    st.link_button(f"💬 Conversar com {r['Nome']}", f"https://wa.me/{numero_limpo}")
        st.markdown("</div>", unsafe_allow_html=True)
