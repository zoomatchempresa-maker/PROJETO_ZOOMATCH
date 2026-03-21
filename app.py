import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

# --- 🎨 ESTILIZAÇÃO VISUAL AVANÇADA ---
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
    .main-title { color: white; text-align: center; font-size: 55px; font-weight: 900; text-shadow: 3px 3px 10px rgba(0,0,0,0.8); padding-top: 20px; }
    .sub-title { text-align: center; color: #fdfdfd; font-size: 22px; text-shadow: 2px 2px 5px rgba(0,0,0,0.7); margin-bottom: 40px; }
    .content-card { 
        background-color: rgba(255, 255, 255, 0.98); 
        padding: 35px; border-radius: 25px; color: #1b4332; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background-color: #2d6a4f; color: white; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1b4332; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de Dados
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Nutrição Animal", "Genética", "Pastagens"],
    "Médico Veterinário": ["Reprodução/IATF", "Sanidade", "Clínica de Grandes", "Clínica de Pequenos", "Cirurgia", "Inspeção"],
    "Engenheiro Agrônomo": ["Grandes Culturas", "Fruticultura", "Solos", "Fitossanidade", "Irrigação", "Mecanização"],
    "Engenheiro Ambiental": ["Licenciamento", "CAR/Outorga", "Gestão de Resíduos", "Sustentabilidade"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Sistemas Agroflorestais"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
SENHA_MESTRA = "Z00-M4tch-2026#Px"

# Conexão com Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None:
            df.columns = df.columns.str.strip()
            df['Contato'] = df['Contato'].astype(str).str.replace('.0', '', regex=False).strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- INTERFACE PRINCIPAL ---
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>A maior vitrine de especialistas do agronegócio</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Menu de Navegação", ["🏠 Home", "📝 Cadastro Profissional", "🚜 Painel do Produtor"])

if menu == "🏠 Home":
    st.markdown("<div class='content-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.header("Seja bem-vindo!")
    st.write("Conectamos produtores que precisam de resultados a profissionais que têm o conhecimento técnico.")
    st.write("---")
    st.info("Escolha uma opção no menu lateral para começar.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🎯 Crie seu Perfil Técnico")
    
    prof_escolhida = st.selectbox("Sua formação principal:", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro_premium"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo")
            estado = st.selectbox("Estado de Atuação", ESTADOS)
            contato = st.text_input("WhatsApp (DDI+DDD+Num)", placeholder="Ex: 5581999998888")
        with col2:
            label_reg = "CRMV" if "Veterinário" in prof_escolhida or "Zootecnista" in prof_escolhida else "CREA"
            registro = st.text_input(f"Registro Profissional ({label_reg})")
            pretensao = st.number_input("Pretensão Salarial/Diária (R$)", min_value=0)
        
        especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
        bio = st.text_area("Resumo Profissional (Experiências e Cursos)")
        
        if st.form_submit_button("🚀 PUBLICAR MEU PERFIL"):
            if nome and contato and especialidades:
                try:
                    # Preparar dado
                    novo = pd.DataFrame([{
                        "Nome": nome, "Profissão": prof_escolhida, "Estado": estado,
                        "Registro": registro, "Especialidades": ", ".join(especialidades),
                        "Contato": contato, "Pretensão": pretensao, "Bio": bio
                    }])
                    
                    # Lógica de atualização segura
                    df_antigo = carregar_dados()
                    df_final = pd.concat([df_antigo, novo], ignore_index=True) if not df_antigo.empty else novo
                    
                    conn.update(data=df_final)
                    st.cache_data.clear()
                    st.success("✨ Sucesso! Seu perfil já está visível para produtores.")
                    st.balloons()
                except Exception as e:
                    st.error("❌ Erro de conexão com o banco de dados. Verifique as permissões de Editor.")
            else:
                st.warning("⚠️ Nome, WhatsApp e Especialidades são campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Painel do Produtor":
    if "autenticado" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Acesso Restrito")
        pass_input = st.text_input("Digite a senha do produtor:", type="password")
        if st.button("Liberar Banco de Dados"):
            if pass_input == SENHA_MESTRA:
                st.session_state["autenticado"] = True
                st.rerun()
            else: st.error("Senha incorreta!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Buscar Especialistas")
        
        c1, c2 = st.columns(2)
        with c1: f_prof = st.selectbox("Filtrar Profissão:", ["Todos"] + list(MAPA_AGRO.keys()))
        with c2: f_uf = st.selectbox("Filtrar Estado:", ["Brasil"] + ESTADOS)
        
        df_busca = carregar_dados()
        if not df_busca.empty:
            if f_prof != "Todos": df_busca = df_busca[df_busca['Profissão'] == f_prof]
            if f_uf != "Brasil": df_busca = df_busca[df_busca['Estado'] == f_uf]
            
            st.write(f"📊 **{len(df_busca)}** profissionais encontrados.")
            
            for _, r in df_busca.iterrows():
                with st.expander(f"👤 {r['Nome']} - {r['Estado']}"):
                    st.write(f"🎓 **Formação:** {r['Profissão']}")
                    st.write(f"🌟 **Foco:** {r['Especialidades']}")
                    st.write(f"📖 **Bio:** {r['Bio']}")
                    st.link_button(f"💬 Chamar no WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
        st.markdown("</div>", unsafe_allow_html=True)
