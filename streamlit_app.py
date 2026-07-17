# --- 4. BARRA LATERAL: PAINEL DO ADMINISTRADOR ---
with st.sidebar:
    st.header("⚙️ Painel de Adimin")
    if st.checkbox("Ativar Modo Administrador"):
        senha_input = st.text_input("Digite a senha de Admin:", type="password")
        
        if len(senha_input) > 0 and senha_input == SENHA_ADMIN:
            st.success("Acesso liberado, Mestre!")
            st.subheader("Gerenciar Placar Global")
            
            placar_completo = []
            if os.path.exists(LEADERBOARD_FILE):
                try:
                    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                        placar_completo = json.load(f)
                except Exception:
                    pass

            if placar_completo:
                for i, jogador in enumerate(placar_completo):
                    # Ajustado o espaçamento para acomodar 3 botões alinhados
                    col_adm1, col_adm2, col_adm3, col_adm4 = st.columns([2, 1, 1, 1])
                    col_adm1.write(f"**{jogador['Jogador']}**: {jogador['Pontos']} pts")
                    
                    # Botão para deletar jogador
                    if col_adm2.button("Ban", key=f"del_{i}", help="Deletar este jogador"):
                        placar_completo.pop(i)
                        salvar_leaderboard_completo(placar_completo)
                        st.rerun()
                    
                    # Botão para somar pontos (+5000)
                    if col_adm3.button("Add", key=f"add_{i}", help="Adicionar +5000 pontos"):
                        jogador['Pontos'] += 5000
                        salvar_leaderboard_completo(placar_completo)
                        st.rerun()

                    # 🌟 NOVO: Botão para remover pontos (-5000)
                    if col_adm4.button("Rem", key=f"rem_{i}", help="Remover -5000 pontos"):
                        jogador['Pontos'] = max(0, jogador['Pontos'] - 5000) # Garante que não fique negativo
                        salvar_leaderboard_completo(placar_completo)
                        st.rerun()
            else:
                st.info("Nenhum jogador registrado no placar ainda.")
        elif senha_input != "":
            st.error("Senha incorreta!")
