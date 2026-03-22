import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import re # Importado para a limpeza do WhatsApp

# 1. Configuracao da Pagina
st.set_page_config(page_title="AgroElit | Conectando o Campo", page_icon="🌾", layout="centered")

# --- DESIGN PROFISSIONAL (CSS) ---
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

# --- CONFIGURACOES DE ACESSO ---
CHAVE_MESTRE = "Z00-M4tch-2026#Px"
SEU_WHATSAPP = "5581999046156" # <--- MUDE PARA O SEU NUMERO REAL AQUI

# --- BANCO DE ESPECIALIDADES ---
MAPA_AGRO = {
    "Zootecnista": ["Bovinos de Corte", "Bovinos de Leite", "Avicultura", "Suinocultura", "Piscicultura", "Equinocultura", "Ovinos e Caprinos", "Pets (Cães e Gatos)", "Nutrição Animal", "Genética", "Manejo de Pastagens"],
    "Médico Veterinário": ["Clínica de Pets", "Clínica de Grandes Animais", "Cirurgia", "Reprodução/IATF", "Sanidade/Vacinas", "Inspeção de Alimentos", "Anestesiologia", "Patologia"],
    "Engenheiro Agrônomo": ["Grãos (Soja/Milho)", "Fruticultura", "Olericultura", "Manejo de Solos", "Fitossanidade", "Irrigação", "Mecanização", "Agricultura de Precisão"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventário", "Sistemas Agroflorestais", "Recuperação de Áreas", "Tecnologia da Madeira"]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

# --- INTERFACE ---
st.markdown("<div class='main-title'>🌾 AgroElit</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Quem é você?", ["🏠 Início", "📝 Sou Especialista (Cadastro)", "🚜 Sou Produtor (Contratar)"])

if menu == "🏠 Início":
    st.markdown("""
    <div class='content-card' style='text-align:center;'>
        <h2 style='color: #1b4332;'>Bem-vindo ao AgroElit</h2>
        <p style='font-size: 18px;'>Conectando a inteligência técnica ao coração do agronegócio.</p>
        <hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>
        <p style='text-align: justify;'>
            O <b>AgroElit</b> é uma vitrine exclusiva para especialistas do campo. 
            Nossa plataforma permite que Médicos Veterinários, Zootecnistas e Agrônomos 
            publiquem seus perfis, facilitando o acesso de produtores rurais que buscam 
            mão de obra qualificada e especializada.
        </p>
        <br>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px;'>
            <div style='flex: 1; min-width: 150px; background: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <b>📝 Cadastro</b><br><small>Crie seu perfil profissional em minutos.</small>
            </div>
            <div style='flex: 1; min-width: 150px; background: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <b>🔑 Segurança</b><br><small>Acesso restrito para produtores curados.</small>
            </div>
            <div style='flex: 1; min-width: 150px; background: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <b>🤝 Negócio</b><br><small>Contato direto sem intermediários.</small>
            </div>
        </div>
        <br>
        <p style='color: #2d6a4f; font-weight: bold;'>👉 Utilize o menu lateral para começar!</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "📝 Sou Especialista (Cadastro)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🎯 Crie sua Vitrine Profissional")
    prof = st.selectbox("Sua Formação:", list(MAPA_AGRO.keys()))
    
    with st.form("form_registro"):
        nome = st.text_input("Nome Completo")
        uf = st.selectbox("Estado de Atuação", ESTADOS)
        reg = st.text_input("Registro (CRMV/CREA)")
        esp = st.multiselect("Suas Especialidades", MAPA_AGRO[prof])
        tel = st.text_input("WhatsApp (Ex: 81999998888)")
        sal = st.number_input("Pretensão Salarial/Diária (R$)", min_value=0)
        bio = st.text_area("Resumo da sua Experiência")
        
        if st.form_submit_button("🚀 PUBLICAR MEU PERFIL"):
            if nome and tel and esp:
                try:
                    df_antigo = carregar_dados()
                    novo = pd.DataFrame([{"Nome": nome, "Profissão": prof, "Estado": uf, "Registro": reg, "Especialidades": ", ".join(esp), "Contato": tel, "Pretensão": sal, "Bio": bio}])
                    df_final = pd.concat([df_antigo, novo], ignore_index=True)
                    conn.update(data=df_final)
                    st.cache_data.clear()
                    st.success("✅ Perfil publicado com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
            else:
                st.warning("⚠️ Preencha os campos obrigatórios.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Sou Produtor (Contratar)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🔑 Acesso Restrito")
    senha_inserida = st.text_input("Insira a Chave de Acesso:", type="password")
    
    if senha_inserida == CHAVE_MESTRE:
        st.success("Acesso Liberado!")
        df = carregar_dados()
        if not df.empty:
            f_p = st.selectbox("Filtrar por Profissão:", ["Todos"] + list(MAPA_AGRO.keys()))
            df_ex = df if f_p == "Todos" else df[df["Profissão"] == f_p]
            
            for _, r in df_ex.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    
                    # --- LIMPEZA DE CONTATO CORRIGIDA ---
                    num_bruto = str(r['Contato'])
                    # Remove o .0 se houver
                    if '.' in num_bruto: num_bruto = num_bruto.split('.')[0]
                    # Remove tudo que não for número
                    c_limpo = re.sub(r'\D', '', num_bruto) 
                    
                    if c_limpo:
                        if not c_limpo.startswith("55"): c_limpo = "55" + c_limpo
                        st.link_button("💬 Chamar no WhatsApp", f"https://wa.me/{c_limpo}")
                    else:
                        st.warning("Número de contato inválido.")
        else:
            st.info("Nenhum profissional cadastrado.")
            
    elif senha_inserida != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave via WhatsApp", f"https://wa.me/{SEU_WHATSAPP}")
    else:
        st.info("Digite a chave para continuar.")
        st.link_button("📲 Solicitar Chave de Acesso", f"https://wa.me/{SEU_WHATSAPP}")
    st.markdown("</div>", unsafe_allow_html=True)
