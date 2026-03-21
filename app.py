import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="AgroMatch", page_icon="🐄")

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para ler os dados sem travar
def carregar_dados():
    try:
        return conn.read(ttl=0)
    except Exception:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

st.title("🐄 AgroMatch")

# Formulário simplificado para teste
with st.form("meu_form"):
    nome = st.text_input("Seu Nome")
    contato = st.text_input("WhatsApp")
    if st.form_submit_button("Publicar Perfil"):
        if nome and contato:
            try:
                # 1. Pega o que já tem
                df_atual = carregar_dados()
                
                # 2. Cria a nova linha (cuidado com os nomes das colunas!)
                novo = pd.DataFrame([{"Nome": nome, "Contato": contato}])
                
                # 3. Junta tudo
                df_final = pd.concat([df_atual, novo], ignore_index=True)
                
                # 4. Tenta salvar
                conn.update(data=df_final)
                st.cache_data.clear()
                st.success("✅ FUNCIONOU! Verifique sua planilha.")
                st.balloons()
            except Exception as e:
                st.error(f"O Google ainda recusa o acesso. Erro: {e}")
        else:
            st.warning("Preencha os campos.")
