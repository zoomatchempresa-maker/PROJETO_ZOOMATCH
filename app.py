import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuração básica
st.set_page_config(page_title="AgroMatch", page_icon="🐄")

# 2. Conexão (O Streamlit usa as chaves que você colou no Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl=0)
        return df
    except:
        # Se a planilha estiver vazia, cria a estrutura com ACENTOS
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- FORMULÁRIO DE CADASTRO ---
st.title("📝 Cadastro AgroMatch")

with st.form("meu_formulario"):
    nome = st.text_input("Nome Completo")
    profissao = st.selectbox("Profissão", ["Zootecnista", "Médico Veterinário", "Engenheiro Agrônomo"])
    estado = st.text_input("Estado (UF)")
    contato = st.text_input("WhatsApp (ex: 5581999998888)")
    especialidades = st.text_input("Suas Especialidades")
    pretensao = st.number_input("Pretensão Salarial", min_value=0)
    bio = st.text_area("Bio/Resumo")
    
    if st.form_submit_button("🚀 PUBLICAR"):
        if nome and contato:
            try:
                # Criar nova linha
                novo_perfil = pd.DataFrame([{
                    "Nome": nome, 
                    "Profissão": profissao, 
                    "Estado": estado, 
                    "Registro": "N/A", 
                    "Especialidades": especialidades, 
                    "Contato": contato, 
                    "Pretensão": pretensao, 
                    "Bio": bio
                }])
                
                # Ler dados atuais e juntar
                df_atual = carregar_dados()
                df_final = pd.concat([df_atual, novo_perfil], ignore_index=True)
                
                # ATUALIZAR PLANILHA
                conn.update(data=df_final)
                
                st.cache_data.clear()
                st.success("✅ Cadastrado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"O Google negou a gravação. Verifique o Passo 2 abaixo!")
        else:
            st.warning("Preencha o nome e o WhatsApp.")
