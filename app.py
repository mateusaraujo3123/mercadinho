import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ocupar a tela toda e sem barra lateral por padrão
st.set_page_config(
    page_title="MERCADINHO PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÃO FORÇADA DE MODO CINZA CHUMBO E BOTÕES ROXOS GRANDES ---
st.markdown("""
    <style>
    /* Esconde completamente a barra lateral e os menus nativos da plataforma */
    [data-testid="stSidebar"], #MainMenu, header, footer, .stDeployButton {
        display: none !important;
    }
    
    /* BLOQUEIO TOTAL: Fundo Cinza Chumbo e texto branco */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #24252A !important; 
        color: #FFFFFF !important;
    }
    
    /* Força texto branco para todos os elementos na tela */
    h1, h2, h3, h4, h5, h6, p, label, span, small, div {
        color: #FFFFFF !important;
    }
    
    /* Topbar Roxa Principal */
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
    
    /* Cartões do Dashboard em tom sobre tom para contraste com o chumbo */
    .dashboard-card {
        background-color: #2F313A; 
        padding: 20px; 
        border-radius: 8px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4); 
        margin-bottom: 20px; 
        border-top: 4px solid #6A1B9A;
    }
    
    .stock-alert { 
        display: flex; 
        justify-content: space-between; 
        padding: 8px 0; 
        border-bottom: 1px solid #3A3D4A; 
    }
    
    .stock-critical { 
        color: #FF6B6B !important; 
        font-weight: bold; 
    }
    
    /* Caixas de entrada, inputs e tabelas adaptados ao chumbo */
    .stDataFrame, div[data-baseweb="select"], input, div[data-baseweb="input"], textarea {
        background-color: #2F313A !important;
        color: white !important;
        border-color: #3A3D4A !important;
    }
    
    /* MODIFICAÇÃO: Estilo para transformar as abas nativas nos BOTÕES ROXOS GRANDES desejados */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        border-bottom: none !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        background-color: #4A148C !important;
        color: white !important;
        border: 2px solid #7B1FA2 !important;
        border-radius: 12px;
        padding: 18px 40px !important; /* Aumenta o tamanho interno do botão */
        font-weight: bold;
        font-size: 18px !important; /* Deixa o texto do botão maior */
        min-width: 250px; /* Garante que os botões fiquem largos e imponentes */
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        background-color: #7B1FA2 !important;
        border-color: #9C27B0 !important;
        transform: translateY(-2px); /* Efeito leve de flutuar ao passar o mouse */
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #9C27B0 !important;
        border-color: #E040FB !important;
        box-shadow: 0px 0px 15px rgba(224, 64, 251, 0.6);
    }
    
    /* Botões padrões de ação (Salvar, Adicionar, Deletar) */
    button {
        background-color: #4A148C !important;
        color: white !important;
        border: 1px solid #7B1FA2 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS EM MEMÓRIA ---
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

# --- HEADER SUPERIOR ---
st.markdown("""
    <div class="topbar">
        <h2 style='margin:0; color:white !important;'>🛍️ MERCADINHO PRO</h2>
        <span style='font-size:14px; color:white !important;'>🟢 MODO ESCURO • BOTÕES ROXOS ATIVADOS</span>
    </div>
""", unsafe_allow_html=True)

# MENU CENTRALIZADO (Abas superiores robustas estilizadas como botões grandes)
aba_dashboard, aba_fiado, aba_produtos = st.tabs(["📊 DASHBOARD INITIAL", "👥 FIADO", "📦 PRODUTOS"])
# ==========================================================
# 1. TELA: DASHBOARD INICIAL
# ==========================================================
with aba_dashboard:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card"><h3>Maiores Dívidas</h3></div>', unsafe_allow_html=True)
        if not st.session_state.devedores.empty:
            df_sorted = st.session_state.devedores.sort_values(by="Divida", ascending=True)
            fig = px.bar(df_sorted, x="Divida", y="Nome", orientation='h', color_discrete_sequence=['#9C27B0'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                height=300, 
                font_color="white",
                xaxis=dict(gridcolor='#3A3D4A', title_font=dict(color='white'), tickfont=dict(color='white')), 
                yaxis=dict(gridcolor='#3A3D4A', title_font=dict(color='white'), tickfont=dict(color='white'))
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Nenhuma dívida registrada.")
        
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
# 2. TELA: FIADO
# ==========================================================
with aba_fiado:
    st.markdown('<div class="dashboard-card"><h2>Local dos Fiados (Controle de Clientes)</h2></div>', unsafe_allow_html=True)
    
    sub_aba_cad, sub_aba_rem = st.tabs(["➕ Cadastrar Cliente / Lançar", "❌ Remover Pessoa dos Fiados"])
    
    with sub_aba_cad:
        with st.expander("➕ Cadastrar Novo Cliente"):
            nome = st.text_input("Nome do Cliente")
            tel = st.text_input("Telefone")
            limite = st.number_input("Limite (R$)", min_value=0.0, value=200.0)
            if st.button("Salvar Cliente"):
                st.session_state.devedores = pd.concat([st.session_state.devedores, pd.DataFrame([{"Nome": nome, "Telefone": tel, "Limite": limite, "Divida": 0.0}])], ignore_index=True)
                st.success("Cliente cadastrado!")
                st.rerun()

        st.write("### 💸 Lançar Compra ou Pagamento")
        if not st.session_state.devedores.empty:
            cliente_sel = st.selectbox("Selecione o Cliente:", st.session_state.devedores["Nome"].tolist())
            val_operacao = st.number_input("Valor (R$)", min_value=0.01)
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

    with sub_aba_rem:
        st.write("### 🗑️ Excluir Conta de Cliente permanentemente")
        if not st.session_state.devedores.empty:
            cliente_remover = st.selectbox("Selecione a pessoa para remover:", st.session_state.devedores["Nome"].tolist(), key="rem_cliente")
            if st.button("🗑️ CONFIRMAR REMOÇÃO"):
                st.session_state.devedores = st.session_state.devedores[st.session_state.devedores["Nome"] != cliente_remover].reset_index(drop=True)
                st.success(f"{cliente_remover} foi removido(a) com sucesso!")
                st.rerun()
        else:
            st.write("Não há clientes para remover.")
            
    st.write("---")
    st.write("### Lista Geral de Contas")
    st.dataframe(st.session_state.devedores, use_container_width=True)

# ==========================================================
# 3. TELA: TABELAS DE PREÇO / PRODUTOS
# ==========================================================
with aba_produtos:
    st.markdown('<div class="dashboard-card"><h2>Tabelas de Preços e Estoque</h2></div>', unsafe_allow_html=True)
    
    sub_aba_p1, sub_aba_p2 = st.tabs(["📋 Lista de Produtos", "🗑️ Remover Produto"])
    
    with sub_aba_p1:
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

    with sub_aba_p2:
        st.write("### 🗑️ Excluir Produto do Catálogo")
        if not st.session_state.produtos.empty:
            prod_remover = st.selectbox("Selecione o produto para remover:", st.session_state.produtos["Produto"].tolist())
            if st.button("🗑️ CONFIRMAR EXCLUSÃO DE PRODUTO"):
                st.session_state.produtos = st.session_state.produtos[st.session_state.produtos["Produto"] != prod_remover].reset_index(drop=True)
                st.success(f"Produto '{prod_remover}' excluído!")
                st.rerun()
        else:
            st.write("Não há produtos cadastrados.")

# --- BOTÃO DE EMERGÊNCIA NO FINAL DA PÁGINA ---
st.write("---")
if st.button("🔄 ATUALIZAR INTERFACE", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
