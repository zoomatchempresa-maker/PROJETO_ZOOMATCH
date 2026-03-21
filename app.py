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
    background-size: coveimport streamlit as st
from streamlit_gsheets import GSimimport streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuracao da Pagina
st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

# --- DESIGN PROFISSIONAL (CSS) ---
# Usei aspas simples nos valores numericos para evitar o erro de 'decimal literal'
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
    background-size: cover; background-position: center; background-attachment: fixed;
}
.stApp::before {
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0,0,0,0.6); z-index: -1;
}
.main-title { 
    color: white; text-align: center; font-size: 50px; font-weight: 900; 
    text-shadow: 2px 2px 8px #000; padding: 20px 0; 
}
.content-card { 
    background-color: rgba(255, 255, 255, 0.96); padding: 30px; 
    border-radius: 20px; color: #1b4332; 
    box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; 
}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACOES ---
CHAVE_MESTRE = "Agro2024"
SEU_WHATSAPP = "5581999998888" # Coloque seu numero real aqui

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
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("Quem é você?", ["🏠 Início", "📝 Sou Especialista (Cadastro)", "🚜 Sou Produtor (Contratar)"])

if menu == "📝 Sou Especialista (Cadastro)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🎯 Crie sua Vitrine Profissional")
    prof = st.selectbox("Sua Formação:", list(MAPA_AGRO.keys()))
    with st.form("form_registro"):
        nome = st.text_input("Nome Completo")
        uf = st.selectbox("Estado de Atuação", ESTADOS)
        reg = st.text_input("Registro (CRMV/CREA)")
        esp = st.multiselect("Suas Especialidades", MAPA_AGRO[prof])
        tel = st.text_input("WhatsApp")
        sal = st.number_input("Pretensão Salarial/Diária (R$)", min_value=0)
        bio = st.text_area("Resumo da sua Experiência")
        if st.form_submit_button("🚀 PUBLICAR MEU PERFIL"):
            if nome and tel and esp:
                df_antigo = carregar_dados()
                novo = pd.DataFrame([{"Nome": nome, "Profissão": prof, "Estado": uf, "Registro": reg, "Especialidades": ", ".join(esp), "Contato": tel, "Pretensão": sal, "Bio": bio}])
                conn.update(data=pd.concat([df_antigo, novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil publicado!")
                st.balloons()
            else:
                st.warning("⚠️ Preencha Nome, Especialidades e WhatsApp.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Sou Produtor (Contratar)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🔑 Acesso Restrito")
    senha = st.text_input("Chave de Acesso:", type="password")
    if senha == CHAVE_MESTRE:
        df = carregar_dados()
        if not df.empty:
            f_p = st.selectbox("Filtrar por Profissão:", ["Todos"] + list(MAPA_AGRO.keys()))
            df_ex = df if f_p == "Todos" else df[df["Profissão"] == f_p]
            for _, r in df_ex.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    st.link_button("💬 Chamar no WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
    elif senha != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave", f"https://wa.me/{SEU_WHATSAPP}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- CARD "QUEM SOMOS" NA TELA DE INICIO ---
    st.markdown(f"""
    <div class='content-card' style='text-align:center;'>
        <h2 style='color: #1b4332; margin-bottom: 20px;'>Bem-vindo ao AgroMatch</h2>
        <p style='font-size: 18px; line-height: 1.6;'>
            O <b>AgroMatch</b> nasceu para conectar a inteligência técnica ao coração do agronegócio. 
            Nossa missão é facilitar o encontro entre produtores rurais que buscam excelência 
            e os profissionais mais qualificados do mercado.
        </p>
        <hr style='border: 0; border-top: 1px solid #eee; margin: 25px 0;'>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;'>
            <div style='flex: 1; min-width: 150px;'>
                <h4 style='color: #2d6a4f;'>📝 Cadastro</h4>
                <p style='font-size: 14px;'>Especialistas mostram seu talento para o mercado.</p>
            </div>
            <div style='flex: 1; min-width: 150px;'>
                <h4 style='color: #2d6a4f;'>🔑 Segurança</h4>
                <p style='font-size: 14px;'>Acesso curado e restrito para produtores parceiros.</p>
            </div>
            <div style='flex: 1; min-width: 150px;'>
                <h4 style='color: #2d6a4f;'>🤝 Conexão</h4>
                <p style='font-size: 14px;'>Negociações diretas e rápidas via WhatsApp.</p>
            </div>
        </div>
        <p style='margin-top: 30px; font-weight: bold; color: #2d6a4f;'>
            👉 Utilize o menu lateral para navegar!
        </p>
    </div>
    """, unsafe_allow_html=True)port streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="AgroMatch", page_icon="🐄", layout="centered")

# CSS Limpo e sem caracteres invisiveis
st.markdown("""
<style>
.stApp { 
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop"); 
    background-size: cover; 
    background-attachment: fixed; 
}
.stApp::before { 
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
    background-color: rgba(0,0,0,0.6); z-index: -1; 
}
.main-title { 
    color: white; text-align: center; font-size: 40px; font-weight: bold; 
    text-shadow: 2px 2px 5px rgba(0,0,0,0.8); padding: 20px; 
}
.content-card { 
    background-color: rgba(255,255,255,0.95); padding: 25px; 
    border-radius: 15px; color: #1b4332; margin-bottom: 20px; 
}
</style>
""", unsafe_allow_html=True)

CHAVE_MESTRE = "Agro2024"
SEU_WHATSAPP = "5581999998888" # Ajuste aqui

MAPA_AGRO = {
    "Zootecnista": ["Bovinos de Corte", "Bovinos de Leite", "Avicultura", "Suinocultura", "Nutrição", "Pastagens"],
    "Médico Veterinário": ["Clínica", "Grandes Animais", "Cirurgia", "Reprodução/IATF", "Sanidade"],
    "Engenheiro Agrônomo": ["Grãos", "Fruticultura", "Solos", "Fitossanidade", "Irrigação"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Recuperação", "Tecnologia da Madeira"]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("Menu", ["🏠 Início", "📝 Cadastro", "🚜 Produtor"])

if menu == "📝 Cadastro":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    prof = st.selectbox("Formação:", list(MAPA_AGRO.keys()))
    with st.form("f1"):
        n = st.text_input("Nome")
        uf = st.selectbox("Estado", ESTADOS)
        r = st.text_input("Registro")
        e = st.multiselect("Especialidades", MAPA_AGRO[prof])
        w = st.text_input("WhatsApp")
        s = st.number_input("Pretensão (R$)", min_value=0)
        b = st.text_area("Bio")
        if st.form_submit_button("🚀 PUBLICAR"):
            if n and w and e:
                df = carregar()
                novo = pd.DataFrame([{"Nome":n,"Profissão":prof,"Estado":uf,"Registro":r,"Especialidades":", ".join(e),"Contato":w,"Pretensão":s,"Bio":b}])
                conn.update(data=pd.concat([df, novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil publicado!")
                st.balloons()
            else:
                st.warning("Preencha Nome, Whats e Especialidades.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Produtor":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    pw = st.text_input("Chave de Acesso:", type="password")
    if pw == CHAVE_MESTRE:
        df = carregar()
        if not df.empty:
            f = st.selectbox("Filtrar:", ["Todos"] + list(MAPA_AGRO.keys()))
            df_f = df if f == "Todos" else df[df["Profissão"] == f]
            for _, r in df_f.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"🌟 {r['Especialidades']}")
                    st.write(f"📝 {r['Bio']}")
                    st.link_button("💬 WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
        else:
            st.info("Nenhum cadastro encontrado.")
    elif pw != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave", f"https://wa.me/{SEU_WHATSAPP}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class='content-card' style='text-align:center;'>
        <h1>Bem-vindo ao AgroMatch</h1>
        <p>Conectando produtores a especialistas.</p>
        <hr>
        <p><b>📝 Cadastro:</b> Profissionais criam seu perfil.</p>
        <p><b>🔑 Curadoria:</b> Acesso seguro para produtores.</p>
        <p><b>🤝 Negócio:</b> Contato direto via WhatsApp.</p>
        <br>
        <p>👉 <b>Use o menu ao lado para começar!</b></p>
    </div>
    """, unsafe_allow_html=True)heetsConnection
import pandas as pd

st.set_page_config(page_title="AgroMatch | Conectando o Campo", page_icon="🐄", layout="centered")

st.markdown("""
<style>
.stApp { background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop"); background-size: cover; background-attachment: fixed; }
.stApp::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.6); z-index: -1; }
.main-title { color: white; text-align: center; font-size: 52px; font-weight: 900; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); padding: 20px 0; }
.content-card { background-color: rgba(255, 255, 255, 0.96); padding: 30px; border-radius: 20px; color: #1b4332; box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

CHAVE_MESTRE = "Agro2024"
SEU_WHATSAPP = "5581999998888" # Ajuste seu número aqui

MAPA_AGRO = {
    "Zootecnista": ["Bovinos de Corte", "Bovinos de Leite", "Avicultura", "Suinocultura", "Piscicultura", "Equinocultura", "Ovinos", "Pets", "Nutrição", "Genética", "Pastagens"],
    "Médico Veterinário": ["Clínica de Pets", "Grandes Animais", "Cirurgia", "Reprodução/IATF", "Sanidade", "Inspeção", "Anestesiologia", "Patologia"],
    "Engenheiro Agrônomo": ["Grãos", "Fruticultura", "Olericultura", "Solos", "Fitossanidade", "Irrigação", "Mecanização", "Agricultura de Precisão"],
    "Engenheiro Florestal": ["Silvicultura", "Manejo Florestal", "Inventário", "Agroflorestas", "Recuperação de Áreas", "Tecnologia da Madeira"]
}

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar():
    try: return conn.read(ttl=0)
    except: return pd.DataFrame(columns=["Nome", "Profissão", "Estado", "Registro", "Especialidades", "Contato", "Pretensão", "Bio"])

st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)
menu = st.sidebar.selectbox("Quem é você?", ["🏠 Início", "📝 Sou Especialista", "🚜 Sou Produtor"])

if menu == "📝 Sou Especialista":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("🎯 Cadastro Profissional")
    prof = st.selectbox("Formação:", list(MAPA_AGRO.keys()))
    with st.form("f1"):
        n = st.text_input("Nome")
        uf = st.selectbox("Estado", ESTADOS)
        r = st.text_input("Registro")
        e = st.multiselect("Especialidades", MAPA_AGRO[prof])
        w = st.text_input("WhatsApp")
        s = st.number_input("Pretensão (R$)", min_value=0)
        b = st.text_area("Bio")
        if st.form_submit_button("🚀 PUBLICAR"):
            if n and w and e:
                df = carregar()
                novo = pd.DataFrame([{"Nome":n,"Profissão":prof,"Estado":uf,"Registro":r,"Especialidades":", ".join(e),"Contato":w,"Pretensão":s,"Bio":b}])
                conn.update(data=pd.concat([df, novo], ignore_index=True))
                st.cache_data.clear()
                st.success("✅ Perfil publicado!")
                st.balloons()
            else: st.warning("Preencha os campos!")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🚜 Sou Produtor":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    pw = st.text_input("Chave de Acesso:", type="password")
    if pw == CHAVE_MESTRE:
        df = carregar()
        if not df.empty:
            f = st.selectbox("Filtrar:", ["Todos"] + list(MAPA_AGRO.keys()))
            df_f = df if f == "Todos" else df[df["Profissão"] == f]
            for _, r in df_f.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']})"):
                    st.write(f"🌟 {r['Especialidades']}")
                    st.write(f"📝 {r['Bio']}")
                    st.link_button("💬 WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
    elif pw != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave", f"https://wa.me/{SEU_WHATSAPP}")
    else: st.info("Insira a chave.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"""<div class='content-card' style='text-align:center;'><h1>Bem-vindo ao AgroMatch</h1><p>Conectando quem produz com quem entende.</p><hr>
    <div style='display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px;'>
    <div style='flex: 1; padding: 10px; border-r; background-position: center; background-attachment: fixed;
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

# --- ⚙️ CONFIGURAÇÕES DE ACESSO ---
CHAVE_MESTRE = "Agro2024"  
SEU_WHATSAPP = "5581999998888" # Lembre-se de colocar seu número real aqui

# --- ⚙️ BANCO DE ESPECIALIDADES ---
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
st.markdown("<div class='main-title'>🐄 AgroMatch</div>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Quem é você?", ["🏠 Início", "📝 Sou Especialista (Cadastro)", "🚜 Sou Produtor (Contratar)"])

if menu == "📝 Sou Especialista (Cadastro)":
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
    senha_inserida = st.text_input("Insira a Chave de Acesso para visualizar os profissionais:", type="password")
    
    if senha_inserida == CHAVE_MESTRE:
        st.success("Acesso Liberado!")
        df = carregar_dados()
        if not df.empty:
            f_p = st.selectbox("Filtrar por Profissão:", ["Todos"] + list(MAPA_AGRO.keys()))
            df_ex = df if f_p == "Todos" else df[df["Profissão"] == f_p]
            for _, r in df_ex.iterrows():
                with st.expander(f"👤 {r['Nome']} ({r['Estado']}) - {r['Profissão']}"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    st.link_button(f"💬 Chamar no WhatsApp", f"https://wa.me/{str(r['Contato']).strip()}")
        else:
            st.info("Nenhum profissional cadastrado ainda.")
    elif senha_inserida != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave via WhatsApp", f"https://wa.me/{SEU_WHATSAPP}?text=Olá,%20gostaria%20da%2
