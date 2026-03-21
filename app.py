# ... (início igual)

elif menu == "📝 Cadastro Profissional":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.header("📋 Cadastro Profissional")
    
    # IMPORTANTE: Usei o st.selectbox FORA do formulário para ele atualizar na hora!
    prof_escolhida = st.selectbox("Selecione sua Profissão", list(MAPA_AGRO.keys()))
    
    with st.form("form_cadastro_final"):
        nome = st.text_input("Nome Completo")
        
        c1, c2 = st.columns(2)
        with c1:
            if prof_escolhida in ["Zootecnista", "Médico Veterinário"]:
                label_reg = "CRMV"
            else:
                label_reg = "CREA"
            registro = st.text_input(f"Seu {label_reg}")
            contato = st.text_input("WhatsApp (Ex: 81999998888)")
        
        with c2:
            # Esse é o segredo: a lista depende do prof_escolhida lá de cima
            especialidades = st.multiselect("Suas Especialidades Técnicas", MAPA_AGRO[prof_escolhida])
            pretensao = st.number_input("Pretensão Salarial Média (R$)", min_value=0)
            
        bio = st.text_area("Resumo de Qualificações")
        
        if st.form_submit_button("Finalizar e Publicar"):
            # ... (resto do código de salvar)
