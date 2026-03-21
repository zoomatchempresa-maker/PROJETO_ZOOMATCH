import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# CSS e Design que você gosta
st.markdown("""<style>.stApp { background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop"); background-size: cover; background-position: center; background-attachment: fixed; } .stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.6); z-index: -1; } .main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0; } .content-card { background-color: rgba(255, 255, 255, 0.96); padding: 30px; border-radius: 20px; color: #1b4332; box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; }</style>""", unsafe_allow_html=True)

MAPA_AGRO = {
    "Zootecnista": ["Bovinos de Corte", "Bovinos de Leite", "Avicultura", "Suinocultura", "Piscicultura", "Equinocultura", "Ovinos e Caprinos", "Pets (Caes e Gatos)", "Nutricao Animal", "Genetica", "Manejo de Pastagens"],
    "Médico Veterinário": ["Clinica de Pets", "Clinica de Grandes Animais", "Cirurgia", "Reproducao/IATF", "Sanidade/Vacinas", "Inspecao de Alimentos", "Anestesiologia", "Patologia"],
    "Engenheiro Agrônomo": ["Graos (Soja/Milho)", "Fruticultura", "Olericultura", "Manejo de Solos", "Fitossanidade", "Irrigacao", "Mecanizacao", "Agricultura de Precisao"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventario", "Sistemas Agroflorestais", "Recuperacao de Areas", "Tecnologia da Madeira"]
}

conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("Quem é você?", ["🏠 Início", "📝 Sou Especialista (Cadastro)", "🚜 Sou Produtor (Contratar)"])

if menu == "📝 Sou Especialista (Cadastro)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    prof = st.selectbox("Sua Formação:", list(MAPA_AGRO.keys()))
    with st.form("form_final"):
        nome = st.text_input("Nome Completo")
        tel = st.text_input("WhatsApp")
        esp = st.multiselect("Especialidades", MAPA_AGRO[prof])
        if st.form_submit_button("🚀 PUBLICAR"):
            if nome and tel and esp:
                try:
                    df = conn.read(ttl=0)
                    novo = pd.DataFrame([{"Nome": nome, "Profissão": prof, "Especialidades": ", ".join(esp), "Contato": tel}])
                    df_res = pd.concat([df, novo], ignore_index=True)
                    conn.update(data=df_res)
                    st.success("✅ FUNCIONOU! Verifique sua planilha.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro Real: {e}")
            else:
                st.warning("Preencha os campos.")
    st.markdown("</div>", unsafe_allow_html=True)
elif menu == "🚜 Sou Produtor (Contratar)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    df = conn.read(ttl=0)
    st.write(df)
    st.markdown("</div>", unsafe_allow_html=True)
