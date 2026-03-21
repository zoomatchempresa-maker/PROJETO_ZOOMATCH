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
                with st.expander(f"👤 {r['Nome']} ({r['Estado']}) - {r['Profissão']}"):
                    st.write(f"🌟 **Especialidades:** {r['Especialidades']}")
                    st.write(f"📝 **Bio:** {r['Bio']}")
                    
                    # --- LIMPEZA DO NÚMERO PARA NÃO DAR ERRO 404 ---
                    contato_limpo = str(r['Contato']).replace("(", "").replace(")", "").replace("-", "").replace(" ", "").strip()
                    if not contato_limpo.startswith("55"):
                        contato_limpo = "55" + contato_limpo
                    
                    st.link_button(f"💬 Chamar no WhatsApp", f"https://wa.me/{contato_limpo}")
        else:
            st.info("Nenhum profissional cadastrado ainda.")
            
    elif senha_inserida != "":
        st.error("Chave incorreta!")
        st.link_button("📲 Solicitar Chave via WhatsApp", f"https://wa.me/{SEU_WHATSAPP}")
        
    else:
        st.info("Digite a chave para continuar.")
        st.link_button("📲 Solicitar Chave de Acesso", f"https://wa.me/{SEU_WHATSAPP}")
    
    st.markdown("</div>", unsafe_allow_html=True)
