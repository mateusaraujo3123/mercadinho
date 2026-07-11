import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração estável da página para ocupar a tela toda
st.set_page_config(
    page_title="SIGE Lite - Mercadinho", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO NATIVA LIMPA ---
st.markdown("""
    <style>
    /* Oculta apenas o botão Deploy e o menu original do Streamlit */
    .stDeployButton, #MainMenu { 
        display: none !important; 
    }
    
    /* Configuração para deixar o cabeçalho roxo do topo idêntico ao modelo original */
    .topbar {
        background-color: #6A1B9A; 
        padding: 15px; 
        border-radius: 8px;
        color: white !important; 
        margin-bottom: 20px; 
        display: flex;
        justify-content: space-between; 
        align-items: center;
    }
    .topbar h2, .topbar span {
        color: white !important;
    }
    
    /* Moldura limpa para os cartões brancos do Dashboard */
    .dashboard-card {
        background-color: #FFFFFF !important; 
        padding: 20px;
        border-radius: 8px; 
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05); 
        margin-bottom: 20px;
        border: 1px solid #EAEAEA;
    }
    
    .stock-alert { 
        display: flex; 
        justify-content: space-between; 
        padding: 8px 0; 
        border-bottom: 1px solid #EEEEEE; 
    }
    
    .stock-critical { 
        color: #D32F2F; 
        font-weight: bold; 
    }
    
    /* CONFIGURAÇÃO DOS BOTÕES: Roxos sólidos, letras brancas visíveis e sem caixas duplas */
    div.stButton > button, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] {
        background-color: #6A1B9A !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 16px 20px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.15) !important;
    }
    div.stButton > button:hover, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"]:hover { 
        background-color: #4A148C !important; 
    }
    
    /* Garante texto interno do botão sempre branco */
    div.stButton > button div, div.stButton > button p, div.stButton > button span,
    button[data-testid="baseButton-secondary"] div, button[data-testid="baseButton-secondary"] p, button[data-testid="baseButton-secondary"] span {
        color: #FFFFFF !important;
        border: none !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS EM MEMÓRIA ---
if 'devedores' not in st.session_state:
    st.session_state.devedores = pd.DataFrame([
        {"Nome": "João Silva", "Telefone": "11999999999", "Limite": 500.0, "Divida": 350.0},
        {"Nome": "Maria Oliveira", "Telefone": "11988888888", "Limite": 300.0, "Divida": 280.0},
        {"Nome": "Carlos Souza", "Telefone": "11977777777", "Limite": 1000.0, "Divida": 150.0},
        {"Nome": "Ana Costa", "Telefone": "11966666666", "Limite": 400.0, "Divida": 410.0},
    ])

if 'produtos' not in st.session_state:
    st.session_state.produtos = pd.DataFrame([
        {"Código": "001", "Produto": "Pilha Recarregável", "Preço": 15.00, "Atacado": 12.00, "Estoque": 5, "Minimo": 50},
        {"Código": "002", "Produto": "Carregador de Celular", "Preço": 35.00, "Atacado": 30.00, "Estoque": 17, "Minimo": 65},
        {"Código": "003", "Produto": "Caixa de som Bluetooth", "Preço": 120.00, "Atacado": 100.00, "Estoque": 12, "Minimo": 150},
        {"Código": "004", "Produto": "Mouse para Notebook", "Preço": 45.00, "Atacado": 40.00, "Estoque": 23, "Minimo": 23},
    ])

opcoes_menu = ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"]
if 'menu_atual' not in st.session_state:
    st.session_state.menu_atual = "Dashboard Inicial"

# --- TOPBAR ROXA ---
st.markdown('<div class="topbar"><h2 style="margin:0; color:white;">🛍️ MERCADINHO PRO</h2><span>🟢 SISTEMA ONLINE</span></div>', unsafe_allow_html=True)

# Atalhos Rápidos por colunas nativas estáveis
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    if st.button("👥 PESSOAS", use_container_width=True):
        st.session_state.menu_atual = "Gestão de Fiados"
        st.rerun()
with col_b2:
    if st.button("📦 PRODUTOS", use_container_width=True):
        st.session_state.menu_atual = "Tabelas de Preço"
        st.rerun()
with col_b3:
    if st.button("📈 CONTAS A RECEBER", use_container_width=True):
        st.session_state.menu_atual = "Gestão de Fiados"
        st.rerun()

st.write("---")
st.sidebar.title("🏪 Menu Mercadinho")
menu = st.sidebar.radio("Ir para:", opcoes_menu, index=opcoes_menu.index(st.session_state.menu_atual) if st.session_state.menu_atual in opcoes_menu else 0)
st.session_state.menu_atual = menu
# ==========================================================
# 1. TELA: DASHBOARD INICIAL
# ==========================================================
if menu == "Dashboard Inicial":
    st.write("## Fluxo de Fiados & Devedores")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card"><h3>Top Maiores Devedores (R$)</h3></div>', unsafe_allow_html=True)
        if not st.session_state.devedores.empty:
            df_sorted = st.session_state.devedores.sort_values(by="Divida", ascending=True)
            # CORREÇÃO DEFINITIVA DO GRÁFICO: Gráfico gerado de forma simples, nativa e segura
            fig = px.bar(df_sorted, x="Divida", y="Nome", orientation='h', color_discrete_sequence=['#6A1B9A'])
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="dashboard-card"><h3>⚠️ Alertas do Estoque</h3></div>', unsafe_allow_html=True)
        for _, prod in st.session_state.produtos.iterrows():
            status_class = "stock-critical" if prod['Estoque'] <= prod['Minimo'] else ""
            st.markdown(f'<div class="stock-alert"><span>{prod["Produto"]}</span><span class="{status_class}">{prod["Estoque"]} / {prod["Minimo"]}</span></div>', unsafe_allow_html=True)

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Soma Total de Fiados", value=f"R$ {st.session_state.devedores['Divida'].sum():,.2f}")
    with c2: st.metric(label="Clientes Acima do Limite", value=len(st.session_state.devedores[st.session_state.devedores["Divida"] > st.session_state.devedores["Limite"]]))
    with c3: st.metric(label="Caixa Estimado do Dia", value="R$ 1.250,00")

# ==========================================================
# 2. TELA: GESTÃO DE FIADOS
# ==========================================================
elif menu == "Gestão de Fiados":
    st.markdown('<div class="dashboard-card"><h2>Local dos Fiados (Controle de Clientes)</h2></div>', unsafe_allow_html=True)
    aba_cad, aba_rem = st.tabs(["➕ Cadastrar Cliente / Lançar", "❌ Remover Pessoa dos Fiados"])
    
    with aba_cad:
        with st.expander("➕ Cadastrar Novo Cliente"):
            nome = st.text_input("Nome do Cliente")
            tel = st.text_input("Telefone")
            limite = st.number_input("Limite (R$)", min_value=0.0, value=200.0)
            if st.button("Salvar Cliente"):
                st.session_state.devedores = pd.concat([st.session_state.devedores, pd.DataFrame([{"Nome": nome, "Telefone": tel, "Limite": limite, "Divida": 0.0}])], ignore_index=True)
                st.rerun()
        st.write("### 💸 Lançar Compra ou Pagamento")
        if not st.session_state.devedores.empty:
            cliente_sel = st.selectbox("Selecione o Cliente:", st.session_state.devedores["Nome"].tolist())
            val_operacao = st.number_input("Valor (R$)", min_value=0.01, step=1.0)
            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("🔴 Adicionar à Dívida (+ Fiado)", use_container_width=True):
                    st.session_state.devedores.loc[st.session_state.devedores["Nome"] == cliente_sel, "Divida"] += val_operacao
                    st.rerun()
            with cb2:
                if st.button("🟢 Abater Dívida (Cliente Pagou)", use_container_width=True):
                    st.session_state.devedores.loc[st.session_state.devedores["Nome"] == cliente_sel, "Divida"] -= val_operacao
                    st.rerun()
    with aba_rem:
        if not st.session_state.devedores.empty:
            cliente_remover = st.selectbox("Selecione para remover:", st.session_state.devedores["Nome"].tolist(), key="rem")
            if st.button("🗑️ CONFIRMAR REMOÇÃO", use_container_width=True):
                st.session_state.devedores = st.session_state.devedores[st.session_state.devedores["Nome"] != cliente_remover].reset_index(drop=True)
                st.rerun()
    st.write("---")
    st.write("### Lista Geral de Contas")
    st.dataframe(st.session_state.devedores, use_container_width=True)

# ==========================================================
# 3. TELA: TABELAS DE PREÇO
# ==========================================================
elif menu == "Tabelas de Preço":
    st.markdown('<div class="dashboard-card"><h2>Tabelas de Preços e Estoque</h2></div>', unsafe_allow_html=True)
    aba_p1, aba_p2 = st.tabs(["📋 Lista de Produtos", "🗑️ Remover Produto"])
    with aba_p1:
        with st.expander("📦 Adicionar Novo Produto"):
            cod = st.text_input("Código")
            nome_prod = st.text_input("Produto")
            p_varejo = st.number_input("Preço Varejo", min_value=0.0)
            p_atacado = st.number_input("Preço Atacado", min_value=0.0)
            est_inicial = st.number_input("Estoque Atual", min_value=0)
            est_min = st.number_input("Mínimo", min_value=0)
            if st.button("Cadastrar Produto"):
                st.session_state.produtos = pd.concat([st.session_state.produtos, pd.DataFrame([{"Código": cod, "Produto": nome_prod, "Preço": p_varejo, "Atacado": p_atacado, "Estoque": est_inicial, "Minimo": est_min}])], ignore_index=True)
                st.rerun()
        st.dataframe(st.session_state.produtos, use_container_width=True)
    with aba_p2:
        if not st.session_state.produtos.empty:
            prod_remover = st.selectbox("Selecione produto para remover:", st.session_state.produtos["Produto"].tolist())
            if st.button("🗑️ CONFIRMAR EXCLUSÃO"):
                st.session_state.produtos = st.session_state.produtos[st.session_state.produtos["Produto"] != prod_remover].reset_index(drop=True)
                st.rerun()
