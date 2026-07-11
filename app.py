import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ocupar a tela toda
st.set_page_config(
    page_title="SIGE Lite - Mercadinho", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CONFIGURAÇÃO DE ESTILO FIXO, LEITURA DOS NOMES E ZOOM MOBILE ---
st.markdown("""
    <style>
    /* AJUSTE FORÇADO DE ZOOM APENAS PARA CELULARES */
    @media (max-width: 768px) {
        [data-testid="stAppViewContainer"] {
            transform: scale(0.9) !important;
            transform-origin: top left !important;
            width: 111% !important; /* Compensa o encolhimento para não sobrar espaço branco */
        }
    }
    
    /* Oculta o botão Deploy antigo, o atualizado e o menu do Streamlit */
    .stDeployButton, iframe[title="deploy"], [data-testid="stDeployButton"], button[title="Deploy this app"], #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Bloqueia a janela flutuante de anúncio que abre no meio da tela */
    [role="dialog"], .stModal, div[data-baseweb="modal"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Força fundo branco e textos escuros em tudo */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background-color: #F8F9FA !important; 
        color: #333333 !important;
    }
    
    /* Garante visibilidade preta/escura para textos comuns e títulos no fundo claro */
    h1, h2, h3, h4, h5, h6, p, label, span, small {
        color: #333333 !important;
    }
    
    /* Topbar Roxa do topo permanece idêntica à imagem */
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
    
    /* CORREÇÃO DO TEXTO APAGADO: Alvo direto na estrutura interna do botão do Streamlit */
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"],
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] p,
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] span,
    .stButton button, .stButton button p {
        background-color: #4A148C !important;
        color: #FFFFFF !important; /* Cor Branca Absoluta e Forçada */
        -webkit-text-fill-color: #FFFFFF !important; /* Força em iPhones e Safari */
        border: 1px solid #7B1FA2 !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        opacity: 1 !important;
    }
    
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"]:hover {
        background-color: #7B1FA2 !important;
        color: #FFFFFF !important;
    }
    
    /* Cartões do Dashboard totalmente brancos e limpos */
    .dashboard-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-top: 4px solid #6A1B9A;
        border-left: 1px solid #EAEAEA;
        border-right: 1px solid #EAEAEA;
        border-bottom: 1px solid #EAEAEA;
    }
    
    /* Alertas de Estoque */
    .stock-alert {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #EEEEEE;
        color: #333333 !important;
    }
    .stock-critical {
        color: #D32F2F !important;
        font-weight: bold;
    }
    
    /* Caixas de texto, seletores e inputs */
    input, select, div[data-baseweb="select"], div[data-baseweb="input"], .stSelectbox {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #CCCCCC !important;
    }
    
    /* Tabelas de dados */
    .stDataFrame div {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIMULAÇÃO DE BANCO DE DADOS EM MEMÓRIA ---
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

# --- HEADER SUPERIOR ESTILO SIGELITE ---
st.markdown("""
    <div class="topbar">
        <h2 style='margin:0;'>🛍️ MERCADINHO PRO</h2>
        <span style='font-size:14px;'>🟢 MODO CLARO OBRIGATÓRIO • ATUALIZADO</span>
    </div>
""", unsafe_allow_html=True)

# Botões superiores alinhados
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

# --- BARRA LATERAL ORIGINAL ---
st.sidebar.title("🏪 Menu Mercadinho")
st.sidebar.write("---")
indice_padrao = opcoes_menu.index(st.session_state.menu_atual) if 'menu_atual' in st.session_state else 0
menu = st.sidebar.radio("Ir para:", opcoes_menu, index=indice_padrao)
st.session_state.menu_atual = menu
# ==========================================================
# 1. TELA: DASHBOARD INICIAL
# ==========================================================
if menu == "Dashboard Inicial":
    st.markdown('<h2 style="color: #333333;">Fluxo de Fiados & Devedores</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card"><h3 style="color:#333;">Top Maiores Devedores (R$)</h3></div>', unsafe_allow_html=True)
        if not st.session_state.devedores.empty:
            df_sorted = st.session_state.devedores.sort_values(by="Divida", ascending=True)
            fig = px.bar(df_sorted, x="Divida", y="Nome", orientation='h', color_discrete_sequence=['#6A1B9A'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                height=300,
                font=dict(color="#333333")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Nenhuma dívida registrada.")
        
    with col2:
        st.markdown('<div class="dashboard-card"><h3 style="color:#333;">⚠️ Alertas do Estoque</h3></div>', unsafe_allow_html=True)
        for _, prod in st.session_state.produtos.iterrows():
            status_class = "stock-critical" if prod['Estoque'] <= prod['Minimo'] else ""
            st.markdown(f"""
                <div class="stock-alert">
                    <span>{prod['Produto']}</span>
                    <span class="{status_class}">{prod['Estoque']} / {prod['Minimo']}</span>
                </div>
            """, unsafe_allow_html=True)

    # Cards de Resumo inferiores originais em modo claro nativo
    st.write("---")
    c1, c2, c3 = st.columns(3)
    total_fiado = st.session_state.devedores["Divida"].sum()
    clientes_atraso = len(st.session_state.devedores[st.session_state.devedores["Divida"] > st.session_state.devedores["Limite"]])
    
    with c1: st.metric(label="Soma Total de Fiados", value=f"R$ {total_fiado:,.2f}", delta="A receber", delta_color="inverse")
    with c2: st.metric(label="Clientes Acima do Limite", value=clientes_atraso, delta="Crítico", delta_color="inverse")
    with c3: st.metric(label="Caixa Estimado do Dia", value="R$ 1.250,00", delta="+15% ontem")

# ==========================================================
# 2. TELA: GESTÃO DE FIADOS
# ==========================================================
elif menu == "Gestão de Fiados":
    st.markdown('<div class="dashboard-card"><h2 style="color:#333;">Local dos Fiados (Controle de Clientes)</h2></div>', unsafe_allow_html=True)
    
    aba_cad, aba_rem = st.tabs(["➕ Cadastrar Cliente / Lançar", "❌ Remover Pessoa dos Fiados"])
    
    with aba_cad:
        with st.expander("➕ Cadastrar Novo Cliente"):
            nome = st.text_input("Nome do Cliente")
            tel = st.text_input("Telefone (WhatsApp)")
            limite = st.number_input("Limite de Crédito (R$)", min_value=0.0, value=200.0)
            if st.button("Salvar Cliente"):
                st.session_state.devedores = pd.concat([st.session_state.devedores, pd.DataFrame([{"Nome": nome, "Telefone": tel, "Limite": limite, "Divida": 0.0}])], ignore_index=True)
                st.success("Cliente cadastrado com sucesso!")
                st.rerun()

        st.write("### 💸 Lançar Compra ou Pagamento no Fiado")
        if not st.session_state.devedores.empty:
            cliente_sel = st.selectbox("Selecione o Cliente:", st.session_state.devedores["Nome"].tolist())
            val_operacao = st.number_input("Valor da Operação (R$)", min_value=0.01, step=1.0)
            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("🔴 Adicionar à Dívida (+ Fiado)"):
                    st.session_state.devedores.loc[st.session_state.devedores["Nome"] == cliente_sel, "Divida"] += val_operacao
                    st.rerun()
            with cb2:
                if st.button("🟢 Abater Dívida (Cliente Pagou)"):
                    st.session_state.devedores.loc[st.session_state.devedores["Nome"] == cliente_sel, "Divida"] -= val_operacao
                    st.rerun()
        else:
            st.write("Nenhum cliente cadastrado.")

    with aba_rem:
        st.write("### 🗑️ Excluir Conta de Cliente permanentemente")
        if not st.session_state.devedores.empty:
            cliente_remover = st.selectbox("Selecione a pessoa para remover:", st.session_state.devedores["Nome"].tolist(), key="rem_cliente")
            if st.button("🗑️ CONFIRMAR REMOÇÃO"):
                st.session_state.devedores = st.session_state.devedores[st.session_state.devedores["Nome"] != cliente_remover].reset_index(drop=True)
                st.success(f"{cliente_remover} removido(a)!")
                st.rerun()
        else:
            st.write("Não há clientes para remover.")
            
    st.write("---")
    st.write("### Lista Geral de Contas")
    st.dataframe(st.session_state.devedores, use_container_width=True)

# ==========================================================
# 3. TELA: TABELAS DE PREÇO
# ==========================================================
elif menu == "Tabelas de Preço":
    st.markdown('<div class="dashboard-card"><h2 style="color:#333;">Tabelas de Preços e Estoque</h2></div>', unsafe_allow_html=True)
    
    aba_p1, aba_p2 = st.tabs(["📋 Lista de Produtos", "🗑️ Remover Produto"])
    
    with aba_p1:
        with st.expander("📦 Adicionar Novo Produto ao Estoque"):
            cod = st.text_input("Código do Produto")
            nome_prod = st.text_input("Nome do Produto")
            p_varejo = st.number_input("Preço Varejo (R$)", min_value=0.0)
            p_atacado = st.number_input("Preço Atacado (R$)", min_value=0.0)
            est_inicial = st.number_input("Estoque Atual", min_value=0)
            est_min = st.number_input("Estoque Mínimo (Alerta)", min_value=0)
            
            if st.button("Cadastrar Produto"):
                novo_prod = {"Código": cod, "Produto": nome_prod, "Preço": p_varejo, "Atacado": p_atacado, "Estoque": est_inicial, "Minimo": est_min}
                st.session_state.produtos = pd.concat([st.session_state.produtos, pd.DataFrame([novo_prod])], ignore_index=True)
                st.success("Produto adicionado com sucesso!")
                st.rerun()
                
        st.write("### Lista de Preços Atual")
        st.dataframe(st.session_state.produtos, use_container_width=True)

    with aba_p2:
        st.write("### 🗑️ Excluir Produto do Catálogo")
        if not st.session_state.produtos.empty:
            prod_remover = st.selectbox("Selecione o produto para remover:", st.session_state.produtos["Produto"].tolist())
            if st.button("🗑️ CONFIRMAR EXCLUSÃO DE PRODUTO"):
                st.session_state.produtos = st.session_state.produtos[st.session_state.produtos["Produto"] != prod_remover].reset_index(drop=True)
                st.success(f"Produto '{prod_remover}' excluído!")
                st.rerun()
        else:
            st.write("Não há produtos cadastrados.")
