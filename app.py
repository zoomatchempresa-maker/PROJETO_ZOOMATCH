import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuracao da Pagina
st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

# --- DESIGN PROFISSIONAL (CSS) ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
    background-size: cover; 
    background-position: center; 
    background-attachment: fixed;
}
.stApp::before {
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.6); z-index: -1;
}
.main-title { 
    color: white; text-align: center; font-size: 52px; font-weight: 900; 
    text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0; 
}
.content-card { 
    background-color: rgba(255, 255, 255, 0.96); padding: 30px; 
    border-radius: 20px; color: #1b4332; 
    box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; 
}
</style>
""", unsafe_allow_html=True)

# --- BANCO DE ESPECIALIDADES ---
MAPA_AGRO = {
    "Zootecnista": ["Bovinocultura de Corte", "Bovinocultura de Leite", "Avicultura", "Suinocultura", "Piscicultura", "Equinocultura", "Ovinos e Caprinos", "Pets (Nutricao)", "Nutricao Animal", "Genetica", "Pastagens"],
    "Médico Veterinário": ["Clinica de Pets", "Clinica de Grandes", "Cirurgia", "Reproducao/IATF", "Sanidade", "Inspecao de POA", "Anestesiologia", "Imagem", "Patologia"],
    "Engenheiro Agrônomo": ["Graos", "Fruticultura", "Olericultura", "Solos", "Fitossanidade", "Irrigacao", "Mecanizacao", "Pos-colheita"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventario", "Sistemas Agroflorestais", "Recuperacao de Areas", "Tecnologia Florestal"]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- INTERFACE ---
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Navegação", ["Início", "Cadastro", "Buscar"])

if menu == "Cadastro":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    prof = st.selectbox("Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_vfinal"):
        nome = st.text_input("Nome Completo")
        uf = st.selectbox("Estado", ESTADOS)
        reg = st.text_input("Registro (CRMV/CREA)")
        esp = st.multiselect("Especialidades", MAPA_AGRO[prof])
        tel = st.text_input("WhatsApp (Ex: 81999998888)")
        sal = st.number_input("Pretensão (R$)", min_value=0)
        bio = st.text_area("Bio/Resumo")
        
        if st.form_submit_button("🚀 PUBLICAR"):
            if nome and tel and esp:
                try:
                    df_antigo = carregar_dados()
                    novo = pd.DataFrame([{"Nome": nome, "Profissão": prof, "Estado": uf, "Registro": reg, "Especialidades": ", ".join(esp), "Contato": tel, "Pretensão": sal, "Bio": bio}])
                    df_final = pd.concat([df_antigo, novo], ignore_index=True)
                    conn.update(data=df_final)
                    st.cache_data.clear()
                    st.success("✅ Perfil publicado!")
                    st.balloons()
                except:
                    st.error("Erro ao salvar. Verifique se o e-mail do robô é EDITOR na planilha.")
            else:
                st.warning("Preencha Nome, Especialidades e WhatsApp.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Buscar":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🔍 Buscar Especialistas")
    df = carregar_dados()
    if not df.empty:
        f_p = st.selectbox("Filtrar Profissão", ["Todos"] + list(MAPA_AGRO.keys()))
        df_ex = df if f_p == "Todos" else df[df["Profissão"] == f_p]
        for _, r in df_ex.iterrows():
            with st.expander(f"{r['Nome']} ({r['Estado']})"):
                st.write(f"🌟 {r['Especialidades']}")
                st.link_button("WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='content-card' style='text-align:center;'><h2>Bem-vindo!</h2><p>Conectando o Agro brasileiro.</p></div>", unsafe_allow_html=True)
