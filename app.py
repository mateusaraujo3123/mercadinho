import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração estável da página para ocupar a tela toda
st.set_page_config(
    page_title="SIGE Lite - Mercadinho", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CONFIGURAÇÃO INVIOLÁVEL DE MODO CLARO, BOTÕES LINDOS E ZOOM COMPENSADO ---
st.markdown("""
    <style>
    /* Oculta o botão Deploy e o menu padrão do Streamlit */
    .stDeployButton, iframe[title="deploy"], [data-testid="stDeployButton"], button[title="Deploy this app"], #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Remove janelas flutuantes de anúncio */
    [role="dialog"], .stModal, div[data-baseweb="modal"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* OBRIGATORIEDADE DO MODO CLARO: Fundo claro e textos escuros */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        background-color: #F8F9FA !important; 
        color: #222222 !important;
    }
    
    /* Garante visibilidade para textos comuns e títulos */
    h1, h2, h3, h4, h5, h6, p, label, span, small {
        color: #222222 !important;
    }
    
    /* Topbar Roxa do topo */
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
    
    /* NOVO ESTILO DOS BOTÕES ROXOS GRANDES COM LETRA BRANCA (SEM CAIXAS DUPLAS) */
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"],
    .stButton button {
        background-color: #6A1B9A !important; /* Roxo sólido e bonito */
        color: #FFFFFF !important; /* Letras brancas puras */
        border: none !important; /* Elimina qualquer borda externa */
        outline: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.15) !important;
        padding: 16px 20px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        transition: background-color 0.2s;
    }
    
    /* Remove as caixas, bordas e linhas cinzas internas que enfeiavam os botões */
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] div,
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] p,
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] span,
    .stButton button div, .stButton button p, .stButton button span {
        border: none !important;
        background: transparent !important;
        color: #FFFFFF !important; /* Força o texto interno a ficar branco */
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Efeito ao passar o mouse ou tocar no botão */
    div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"]:hover,
    .stButton button:hover {
        background-color: #4A148C !important;
        color: #FFFFFF !important;
    }
    
    /* COMPENSAÇÃO DE ZOOM AUTOMÁTICA EM CELULARES */
    @media (max-width: 768px) {
        [data-testid="stAppViewContainer"] {
            transform: scale(0.85) !important; /* Reduz o zoom de tudo para caber na tela */
            transform-origin: top left !important;
            width: 117% !important; /* Preenche a largura corretamente */
        }
    }
    
    /* Cartões brancos do Dashboard */
    .dashboard-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #EAEAEA !important;
    }
    
    /* Alertas de Estoque */
    .stock-alert {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #EEEEEE;
        color: #222222 !important;
    }
    .stock-critical {
        color: #D32F2F !important;
        font-weight: bold;
    }
    
    /* Caixas de entrada de texto e inputs */
    input, select, div[data-baseweb="select"], div[data-baseweb="input"], .stSelectbox {
        background-color: #FFFFFF !important;
        color: #222222 !important;
        border: 1px solid #CCCCCC !important;
    }
    
    /* Tabelas de dados */
    .stDataFrame div, [data-testid="stTable"] div {
        background-color: #FFFFFF !important;
        color: #222222 !important;
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

# --- HEADER SUPERIOR ESTILO SIGELITE ---
st.markdown("""
    <div class="topbar">
        <h2 style='margin:0;'>🛍️ MERCADINHO PRO</h2>
        <span style='font-size:14px;'>🟢 MODO CLARO TOTAL • ATUALIZADO</span>
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
indice_padrao = opcoes_menu.index(st.session_state.menu_atual) if st.session_state.menu_atual in opcoes_menu else 0
menu = st.sidebar.radio("Ir para:", opcoes_menu, index=indice_padrao)
st.session_state.menu_atual = menu
# ==========================================================
# 1. TELA: DASHBOARD INICIAL
# ==========================================================
if menu == "Dashboard Inicial":
    st.markdown('<h2 style="color: #222222 !important; font-weight: bold;">Fluxo de Fiados & Devedores</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card"><h3 style="color:#222222 !important; font-weight: bold;">Top Maiores Devedores (R$)</h3></div>', unsafe_allow_html=True)
        if not st.session_state.devedores.empty:
            df_sorted = st.session_state.devedores.sort_values(by="Divida", ascending=True)
            fig = px.bar(df_sorted, x="Divida", y="Nome", orientation='h', color_discrete_sequence=['#6A1B9A'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                height=300,
                font=dict(color="#222222", size=14, family="Arial"),
                xaxis=dict(tickfont=dict(color='#222222', size=12), title_font=dict(color='#222222')),
                yaxis=dict(tickfont=dict(color='#222222', size=12), title_font=dict(color='#222222'))
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Nenhuma dívida registrada.")
        
    with col2:
        st.markdown('<div class="dashboard-card"><h3 style="color:#222222 !important; font-weight: bold;">⚠️ Alertas do Estoque</h3></div>', unsafe_allow_html=True)
        for _, prod in st.session_state.produtos.iterrows():
            status_class = "stock-critical" if prod['Estoque'] <= prod['Minimo'] else ""
            st.markdown(f"""
                <div class="stock-alert">
                    <span style="color:#222222 !important; font-weight: bold;">{prod['Produto']}</span>
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
    st.markdown('<div class="dashboard-card"><h2 style="color:#222222 !important;">Local dos Fiados (Controle de Clientes)</h2></div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="dashboard-card"><h2 style="color:#222222 !important;">Tabelas de Preços e Estoque</h2></div>', unsafe_allow_html=True)
    
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
