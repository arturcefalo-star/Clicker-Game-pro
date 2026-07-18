
import streamlit as st
import time
import random
import json
import os
from streamlit_autorefresh import st_autorefresh

# =====================================================================
# CONFIGURAÇÕES E CONSTANTES
# =====================================================================
NOME_PET_7 = "Barbbie"; BONUS_PET_7 = 1000000
NOME_PET_8 = "Homem A."; BONUS_PET_8 = 2500000
NOME_PET_9 = "Tame do cossita"; BONUS_PET_9 = 5000000
CUSTO_OVO_MUNDO_2_BARATO = 50000000
NOME_PET_M2_R1 = "Pocoyo"; BONUS_PET_M2_R1 = 10000000
NOME_PET_M2_R2 = "Bob Construtor"; BONUS_PET_M2_R2 = 25000000
NOME_PET_M2_R3 = "Pintinho A."; BONUS_PET_M2_R3 = 50000000
CUSTO_OVO_MUNDO_2_CARO = 500000000

SENHA_ADMIN = "XXxx67xxXX"
SENHA_ADMIN2 = "19371937"
ACCOUNTS_FILE = "usuarios.json"
LEADERBOARD_FILE = "leaderboard.json"
AVISOS_FILE = "avisos.json"

# --- FUNÇÕES DE PERSISTÊNCIA ---
def carregar_todos_usuarios():
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def salvar_todos_usuarios(usuarios):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

def salvar_progresso_atual():
    if st.session_state.logado:
        usuarios = carregar_todos_usuarios()
        u = st.session_state.nome_usuario.lower()
        if u in usuarios:
            usuarios[u]["dados"] = {
                "pontos": st.session_state.pontos,
                "poder_base": st.session_state.poder_base,
                "pontos_por_segundo": st.session_state.pontos_por_segundo,
                "pet_slot_1": st.session_state.pet_slot_1,
                "pet_slot_2": st.session_state.pet_slot_2,
                "pet_slot_m2_1": st.session_state.pet_slot_m2_1,
                "pet_slot_m2_2": st.session_state.pet_slot_m2_2,
                "mundo_2_desbloqueado": st.session_state.mundo_2_desbloqueado,
                "mundo_atual": st.session_state.mundo_atual
            }
            salvar_todos_usuarios(usuarios)

# --- INICIALIZAÇÃO ---
if "logado" not in st.session_state: st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.title("Login / Registro")
    u_input = st.text_input("Usuário").lower()
    p_input = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuarios = carregar_todos_usuarios()
        if u_input in usuarios and usuarios[u_input]["senha"] == p_input:
            d = usuarios[u_input]["dados"]
            st.session_state.update({"logado": True, "nome_usuario": u_input, **d})
            st.rerun()
    st.stop()

# --- LÓGICA DO JOGO ---
if "poder_clique" not in st.session_state: st.session_state.poder_clique = 1

with st.sidebar:
    st.write(f"Logado: {st.session_state.nome_usuario}")
    if st.checkbox("Painel Admin"):
        pwd = st.text_input("Senha Admin", type="password")
        if pwd == SENHA_ADMIN:
            st.subheader("Inspecionar Jogadores")
            # CORREÇÃO: Carrega todos os usuários do JSON fresco
            all_users = carregar_todos_usuarios()
            lista_nomes = [all_users[k]["nome_exibicao"] for k in all_users]
            
            alvo = st.selectbox("Escolha um jogador:", options=lista_nomes, key="admin_select_user")
            
            # Buscar chave do usuário selecionado
            for k, v in all_users.items():
                if v["nome_exibicao"] == alvo:
                    st.write(f"Pontos do jogador: {v['dados']['pontos']}")
                    if st.button(f"Resetar {alvo}"):
                        all_users[k]["dados"]["pontos"] = 0
                        salvar_todos_usuarios(all_users)
                        st.rerun()

st.title("Clicker Game")
st.metric("Seus Pontos", f"{st.session_state.pontos:,}")

if st.button("Clique Aqui"):
    st.session_state.pontos += st.session_state.poder_clique
    salvar_progresso_atual()
    st.rerun()

if st.button("Sair"):
    st.session_state.logado = False
    st.rerun()
