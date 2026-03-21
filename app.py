import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

# --- 🎨 DESIGN PROFISSIONAL (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-positiimport streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

# --- 🎨 DESIGN PROFISSIONAL (CSS) ---
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
    .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0; }
    .content-card { background-color: rgba(255, 255, 255, 0.96); padding: 30px; border-radius: 20px; color: #1b4332; box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ BANCO DE ESPECIALIDADES ---
MAPA_AGRO = {
    "Zootecnista": [
        "Bovinocultura de Corte", "Bovinocultura de Leite", "Avicultura", "Suinocultura", 
        "Piscicultura/Aquicultura", "Equinocultura", "Ovinos e Caprinos", "Pets (Nutrição)",
        "Nutrição Animal Avançada", "Melhoramento Genético", "Manejo de Pastagens", "Gestão Rural"
    ],
    "Médico Veterinário": [
        "Clínica de Pequenos Animais (Pets)", "Clínica de Grandes Animais", "Cirurgia Veterinária",
        "Reprodução Animal / IATF", "Sanidade e Vacinação", "Inspeção de POA",
        "Anestesiologia", "Diagnóstico por Imagem", "Patologia"
    ],
    "Engenheiro Agrônomo": [
        "Grãos (Soja, Milho, Trigo)", "Fruticultura", "Olericultura", "Manejo de Solos",
        "Fitossanidade", "Irrigação e Drenagem", "Mecanização/Agricultura de Precisão",
        "Pós-colheita", "Extensão Rural"
    ],
    "Engenheiro Florestal": [
        "Silvicultura", "Manejo Florestal Sustentável", "Inventário Florestal",
        "Sistemas Agroflorestais", "Recuperação de Áreas Degradadas", "Tecnologia Florestal"
    ]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- INTERFACE ---
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro de Especialista")
    
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro_vfinal"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado de Atuação", ESTADOS)
        registro = st.text_input("Registro Profissional (CRMV / CREA)")
        especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
        contato = st.text_input("WhatsApp (Ex: 81999998888)")
        pretensao = st.number_input("Pretensão Salarial/Diária (R$)", min_value=0)
        bio = st.text_area("Bio / Experiência Profissional")
        
        enviar = st.form_submit_button("🚀 PUBLICAR MEU PERFIL")
        
        if enviar:
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
                    st.success("✅ Perfil publicado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar. Verifique se o robô é EDITOR na planilha.")
            else:
                st.warning("⚠️ Preencha Nome, Especialidades e Contato.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Buscar Especialistas":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🔍 Buscar Profissionais")
    dados = carregar_dados()
    if dados is not None and not dados.empty:
        f_prof = st.selectbox("Filtrar Profissão", ["Todos"] + list(MAPA_AGRO.keys()))
        
        if f_prof == "Todos":
            df_exibir = dados
        else:
            df_exibir = dados[dados["Profissão"] == f_prof]
        
        for _, r in df_exibir.iterrows():
            with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                st.write(f"💼 **{r['Profissão']}**")
                st.write(f"🌟 **Foco:** {r['Especialidades']}")
                st.write(f"📝 **Bio:** {r['Bio']}")
                st.link_button(f"💬 Conversar", f"https://wa.me/{str(r['Contato']).strip()}")
    else:
        st.info("Nenhum profissional cadastrado ainda.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='content-card' style='text-align:center;'><h2>Bem-vindo ao AgroMatch</h2><p>Conectando quem produz com quem entende.</p></div>", unsafe_allow_html=True)on: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.6); z-index: -1;
    }
    .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0; }
    .content-card { background-color: rgba(255, 255, 255, 0.96); padding: 30px; border-radius: 20px; color: #1b4332; box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ BANCO DE ESPECIALIDADES COMPLETO ---
MAPA_AGRO = {
    "Zootecnista": [
        "Bovinocultura de Corte", "Bovinocultura de Leite", "Avicultura", "Suinocultura", 
        "Piscicultura/Aquicultura", "Equinocultura", "Ovinos e Caprinos", "Pets (Nutrição)",
        "Nutrição Animal Avançada", "Melhoramento Genético", "Manejo de Pastagens", "Gestão Rural"
    ],
    "Médico Veterinário": [
        "Clínica de Pequenos Animais (Pets)", "Clínica de Grandes Animais", "Cirurgia Veterinária",
        "Reprodução Animal / IATF", "Sanidade e Vacinação", "Inspeção de POA",
        "Anestesiologia", "Diagnóstico por Imagem", "Patologia"
    ],
    "Engenheiro Agrônomo": [
        "Grãos (Soja, Milho, Trigo)", "Fruticultura", "Olericultura", "Manejo de Solos",
        "Fitossanidade", "Irrigação e Drenagem", "Mecanização/Agricultura de Precisão",
        "Pós-colheita", "Extensão Rural"
    ],
    "Engenheiro Florestal": [
        "Silvicultura", "Manejo Florestal Sustentável", "Inventário Florestal",
        "Sistemas Agroflorestais", "Recuperação de Áreas Degradadas", "Tecnologia Florestal"
    ]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- INTERFACE ---
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("📍 Navegação", ["🏠 Início", "📝 Cadastro Profissional", "🚜 Buscar Especialistas"])

if menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro de Especialista")
    
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro_vfinal"):
        nome = st.text_input("Nome Completo")
        estado = st.selectbox("Estado de Atuação", ESTADOS)
        registro = st.text_input("Registro Profissional (CRMV / CREA)")
        especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
        contato = st.text_input("WhatsApp (Ex: 81999998888)")
        pretensao = st.number_input("Pretensão Salarial/Diária (R$)", min_value=0)
        bio = st.text_area("Bio / Experiência Profissional")
        
        # Botão de envio obrigatório dentro do form
        enviar = st.form_submit_button("🚀 PUBLICAR MEU PERFIL")
        
        if enviar:
            if nome and contato
