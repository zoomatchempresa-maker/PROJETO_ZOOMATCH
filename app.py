import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# --- 🎨 ESTILIZAÇÃO VISUAL PREMIUM ---
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
    .google-btn {
        display: inline-flex; align-items: center; justify-content: center;
        background-color: white; color: #444; border: 1px solid #ddd;
        padding: 12px; border-radius: 10px; font-weight: bold;
        text-decoration: none; transition: 0.3s; width: 100%; margin-bottom: 20px;
    }
    .google-btn:hover { background-color: #f8f9fa; border-color: #2d6a4f; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados e Conexão
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Nutrição Animal", "Melhoramento Genético", "Pastagens"],
    "Médico Veterinário": ["Reprodução e IATF", "Sanidade Animal", "Clínica de Grandes", "Clínica de Pequenos", "Cirurgia", "Inspeção"],
    "Engenheiro Agrônomo": ["Grandes Culturas", "Fruticultura", "Olericultura", "Manejo de Solos", "Fitossanidade", "Irrigação"],
    "Engenheiro Ambiental": ["Licenciamento", "CAR", "Outorga", "Recuperação de Áreas", "Gestão de Resíduos"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventário", "Sistemas Agroflorestais"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
SENHA_MESTRA = "Z00-M4tch-2026#Px"

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        if df is not None:
            df.columns = df.columns.str.strip()
            df['Contato'] = df['Contato'].astype(str).str.replace('.0', '', regex=False).str.strip()
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# 3. Títulos
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 Bem-vindo à Evolução do Campo</h2><p>O AgroMatch une tecnologia e conhecimento técnico para impulsionar sua produtividade.</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro de Especialista")
    
    # BOTÃO GOOGLE VISUAL
    st.markdown(f"""
        <a href="#" class="google-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" style="width:20px; margin-right:12px;">
            Entrar com Google para preenchimento rápido
        </a>
    """, unsafe_allow_html=True)
    
    prof_escolhida = st.selectbox("Sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_final_agro"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado (UF)", ESTADOS)
        c1, c2 = st.columns(2)
        with c1:
            label_reg = "CRMV" if prof_escolhida in ["Zootecnista", "Médico Veterinário"] else "CREA"
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (DDI+DDD+Número, ex: 5581999998888)")
        with c2:
            especialidades = st.multiselect("Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
        
        bio = st.text_area("Resumo das suas principais experiências")
        
        if st.form_submit_button("🚀 PUBLICAR MEU PERFIL"):
            if nome and contato and especialidades:
                novo = pd.DataFrame([{"Nome": nome, "Profissão": prof_escolhida, "Estado": estado, "Registro": registro, "Especialidades": ", ".join(especialidades), "Contato": contato, "Pretensão": pretensao, "Bio": bio}])
                conn.update(data=pd.concat([carregar_dados(), novo], ignore_index=True))
                st.cache_data.clear()
                st.success(f"✨ Parabéns, {nome}! Seu perfil está disponível para produtores de todo o Brasil.")
            else:
                st.warning("⚠️ Atenção: Nome, WhatsApp e Especialidades são obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Acesso ao Banco de Dados")
        senha = st.text_input("Senha do Produtor", type="password")
        if st.button("Liberar Acesso"):
            if senha == SENHA_MESTRA:
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Senha incorreta. Solicite ao administrador.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Filtros de Busca")
        p_busca = st.selectbox("Profissão:", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        uf_busca = st.selectbox("Localização:", ["Brasil Inteiro"] + ESTADOS)
        
        dados = carregar_dados()
        if not dados.empty:
            df_f = dados
            if p_busca != "Ver Todos": df_f = df_f[df_f['Profissão'] == p_busca]
            if uf_busca != "Brasil Inteiro": df_f = df_f[df_f['Estado'] == uf_busca]
            
            st.info(f"📊 Encontramos {len(df_f)} profissionais qualificados.")
            
            for _, r in df_f.iterrows():
                with st.expander(f"👤 {r['Nome']} - {r['Profissão']} ({r['Estado']})"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"💰 **Pretensão:** R$ {r['Pretensão']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    # Botão que puxa o número direto do banco de dados
                    st.link_button(f"💬 Conversar com {r['Nome']}", f"https://wa.me/{str(r['Contato']).strip()}")
        st.markdown("</div>", unsafe_allow_html=True)
