import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# --- 🎨 ESTILO VISUAL ORIGINAL ---
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
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de Dados
MAPA_AGRO = {
    "Zootecnista": ["Bovinos", "Aves", "Suínos", "Peixes", "Equinos", "Ovinos/Caprinos", "Nutrição Animal", "Genética", "Pastagens"],
    "Médico Veterinário": ["Reprodução", "Sanidade", "Clínica de Grandes", "Clínica de Pequenos", "Cirurgia", "Inspeção"],
    "Engenheiro Agrônomo": ["Grandes Culturas", "Fruticultura", "Solos", "Fitossanidade", "Irrigação"],
    "Engenheiro Ambiental": ["Licenciamento", "CAR", "Outorga", "Sustentabilidade"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal"]
}
ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
SENHA_MESTRA = "Z00-M4tch-2026#Px"

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# 3. Interface
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Conectando Especialistas ao Produtor Rural</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "🏠 Início":
    st.markdown("<div class='content-card' style='text-align:center;'><h2>🏆 O Agro em um só clique</h2><p>Use o menu lateral para navegar!</p></div>", unsafe_allow_html=True)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado (UF)", ESTADOS)
        registro = st.text_input("Registro Profissional (CRMV/CREA)")
        especialidades = st.multiselect("Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
        contato = st.text_input("WhatsApp (Ex: 5581999998888)")
        pretensao = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
        bio = st.text_area("Descreva sua experiência")
        
        if st.form_submit_button("Finalizar e Publicar"):
            if nome and contato and especialidades:
                try:
                    # Criar DataFrame com os novos dados
                    novo = pd.DataFrame([{
                        "Nome": nome, "Profissão": prof_escolhida, "Estado": estado,
                        "Registro": registro, "Especialidades": ", ".join(especialidades),
                        "Contato": contato, "Pretensão": pretensao, "Bio": bio
                    }])
                    
                    # Tentar ler e concatenar
                    df_atual = carregar_dados()
                    df_final = pd.concat([df_atual, novo], ignore_index=True)
                    
                    # Atualizar
                    conn.update(data=df_final)
                    st.cache_data.clear()
                    st.success(f"✅ Perfil de {nome} publicado!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar. Verifique se a planilha está como EDITOR.")
            else:
                st.warning("Preencha Nome, WhatsApp e Especialidades.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    if "auth" not in st.session_state:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔓 Área do Produtor")
        senha = st.text_input("Senha de Acesso", type="password")
        if st.button("Liberar Banco"):
            if senha == SENHA_MESTRA:
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Senha incorreta")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.header("🔍 Buscar Especialistas")
        p_busca = st.selectbox("Profissão:", ["Ver Todos"] + list(MAPA_AGRO.keys()))
        uf_busca = st.selectbox("Estado (UF):", ["Brasil Inteiro"] + ESTADOS)
        
        dados = carregar_dados()
        if not dados.empty:
            df_f = dados
            if p_busca != "Ver Todos": df_f = df_f[df_f['Profissão'] == p_busca]
            if uf_busca != "Brasil Inteiro": df_f = df_f[df_f['Estado'] == uf_busca]
            
            for _, r in df_f.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"🌟 **Foco:** {r['Especialidades']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    st.link_button(f"💬 WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
        st.markdown("</div>", unsafe_allow_html=True)
