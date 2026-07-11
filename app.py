import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Configuração estável da página para ocupar a tela toda
st.set_page_config(
    page_title="SIGE Lite - Mercadinho", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO NATIVA LIMPA ---
st.markdown("""
    <style>
    .stDeployButton, #MainMenu { display: none !important; }
    .topbar {
        background-color: #6A1B9A; padding: 15px; border-radius: 8px;
        color: white !important; margin-bottom: 20px; display: flex;
        justify-content: space-between; align-items: center;
    }
    .dashboard-card {
        background-color: #FFFFFF !important; padding: 20px;
        border-radius: 8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05); 
        margin-bottom: 20px; border: 1px solid #EAEAEA;
    }
    .stock-alert { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #EEEEEE; }
    .stock-critical { color: #D32F2F; font-weight: bold; }
    
    div.stButton > button, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] {
        background-color: #6A1B9A !important; color: #FFFFFF !important;
        border: none !important; padding: 16px 20px !important;
        font-weight: bold !important; font-size: 16px !important;
        border-radius: 8px !important; box-shadow: 0px 4px 6px rgba(0,0,0,0.15) !important;
    }
    div.stButton > button:hover, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"]:hover { 
        background-color: #4A148C !important; 
    }
    div.stButton > button div, div.stButton > button p, div.stButton > button span,
    button[data-testid="baseButton-secondary"] div, button[data-testid="baseButton-secondary"] p, button[data-testid="baseButton-secondary"] span {
        color: #FFFFFF !important; border: none !important; background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO DUPLA (PANDAS LÊ SEGURO / GSPREAD GRAVA SEM ERRO) ---
try:
    # 1. Leitura ultra veloz via link público (Evita o RefreshError de leitura)
    url_base = st.secrets["connections"]["gsheets"]["spreadsheet"]
    url_id = url_base.split("/edit")
    url_clientes = f"{url_id[0]}/gviz/tq?tqx=out:csv&sheet=Clientes"
    url_produtos = f"{url_id[0]}/gviz/tq?tqx=out:csv&sheet=Produtos"
    
    df_devedores = pd.read_csv(url_clientes)
    df_produtos = pd.read_csv(url_produtos)
    
    # 2. Inicializa o motor gspread em segundo plano apenas para salvar quando clicar nos botões
    info_chaves = dict(st.secrets["gserviceaccount"])
    info_chaves["private_key"] = info_chaves["private_key"].replace("\\n", "\n")
    escopos = ["https://googleapis.com", "https://googleapis.com"]
    creds = Credentials.from_service_account_info(info_chaves, scopes=escopos)
    client_gspread = gspread.authorize(creds)
    
    planilha = client_gspread.open_by_key("1Wmf92fjhBcgZwnrgi_Zme1XiZM4acAn27eBsNHrKgFg")
    aba_clientes = planilha.worksheet("Clientes")
    aba_produtos = planilha.worksheet("Produtos")

    # Tratamento numérico padrão
    df_devedores["Limite"] = pd.to_numeric(df_devedores["Limite"], errors='coerce').fillna(0.0)
    df_devedores["Divida"] = pd.to_numeric(df_devedores["Divida"], errors='coerce').fillna(0.0)
    df_produtos["Preço"] = pd.to_numeric(df_produtos["Preço"], errors='coerce').fillna(0.0)
    df_produtos["Atacado"] = pd.to_numeric(df_produtos["Atacado"], errors='coerce').fillna(0.0)
    df_produtos["Estoque"] = pd.to_numeric(df_produtos["Estoque"], errors='coerce').fillna(0).astype(int)
    df_produtos["Minimo"] = pd.to_numeric(df_produtos["Minimo"], errors='coerce').fillna(0).astype(int)

except Exception as e:
    st.error("⚠️ Erro de inicialização com o banco de dados:")
    st.exception(e)
    st.stop()

opcoes_menu = ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"]
if 'menu_atual' not in st.session_state:
    st.session_state.menu_atual = "Dashboard Inicial"

st.markdown('<div class="topbar"><h2 style="margin:0; color:white;">🛍️ MERCADINHO PRO</h2><span>🟢 SISTEMA INTEGRADO ATIVO</span></div>', unsafe_allow_html=True)

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

if menu == "Dashboard Inicial":
    st.write("## Fluxo de Fiados & Devedores")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="dashboard-card"><h3>Top Maiores Devedores (R$)</h3></div>', unsafe_allow_html=True)
        if not df_devedores.empty and df_devedores["Divida"].sum() > 0:
            df_sorted = df_devedores.sort_values(by="Divida", ascending=True)
            fig = px.bar(df_sorted, x="Divida", y="Nome", orientation='h', color_discrete_sequence=['#6A1B9A'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Nenhuma dívida ativa registrada na planilha.")
    with col2:
        st.markdown('<div class="dashboard-card"><h3>⚠️ Alertas do Estoque</h3></div>', unsafe_allow_html=True)
        if not df_produtos.empty:
            for _, prod in df_produtos.iterrows():
                status_class = "stock-critical" if prod['Estoque'] <= prod['Minimo'] else ""
                st.markdown(f'<div class="stock-alert"><span>{prod["Produto"]}</span><span class="{status_class}">{prod["Estoque"]} / {prod["Minimo"]}</span></div>', unsafe_allow_html=True)
        else:
            st.write("Nenhum produto cadastrado na planilha.")

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Soma Total de Fiados", value=f"R$ {df_devedores['Divida'].sum():,.2f}")
    with c2: st.metric(label="Clientes Acima do Limite", value=len(df_devedores[df_devedores["Divida"] > df_devedores["Limite"]]))
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
                # gspread adiciona a linha diretamente no fim da tabela
                aba_clientes.append_row([nome, str(tel), float(limite), 0.0])
                st.success("Cadastrado com sucesso na Planilha!")
                st.rerun()
                
        st.write("### 💸 Lançar Compra ou Pagamento")
        if not df_devedores.empty and len(df_devedores["Nome"].tolist()) > 0:
            cliente_sel = st.selectbox("Selecione o Cliente:", df_devedores["Nome"].tolist())
            val_operacao = st.number_input("Valor (R$)", min_value=0.01, step=1.0)
            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("🔴 Adicionar à Dívida (+ Fiado)", use_container_width=True):
                    idx = df_devedores[df_devedores["Nome"] == cliente_sel].index[0]
                    valor_atual = float(df_devedores.loc[idx, "Divida"])
                    aba_clientes.update_cell(int(idx) + 2, 4, valor_atual + float(val_operacao))
                    st.rerun()
            with cb2:
                if st.button("🟢 Abater Dívida (Cliente Pagou)", use_container_width=True):
                    idx = df_devedores[df_devedores["Nome"] == cliente_sel].index[0]
                    valor_atual = float(df_devedores.loc[idx, "Divida"])
                    aba_clientes.update_cell(int(idx) + 2, 4, valor_atual - float(val_operacao))
                    st.rerun()
        else:
            st.write("Nenhum cliente cadastrado.")
            
    with aba_rem:
        if not df_devedores.empty and len(df_devedores["Nome"].tolist()) > 0:
            cliente_remover = st.selectbox("Selecione para remover:", df_devedores["Nome"].tolist(), key="rem")
            if st.button("🗑️ CONFIRMAR REMOÇÃO", use_container_width=True):
                idx = df_devedores[df_devedores["Nome"] == cliente_remover].index[0]
                aba_clientes.delete_rows(int(idx) + 2)
                st.rerun()
                
    st.write("---")
    st.write("### Lista Geral de Contas")
    st.dataframe(df_devedores, use_container_width=True)

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
                aba_produtos.append_row([str(cod), nome_prod, float(p_varejo), float(p_atacado), int(est_inicial), int(est_min)])
                st.rerun()
                
        st.dataframe(df_produtos, use_container_width=True)
        
    with aba_p2:
        if not df_produtos.empty and len(df_produtos["Produto"].tolist()) > 0:
            prod_remover = st.selectbox("Selecione produto para remover:", df_produtos["Produto"].tolist())
            if st.button("🗑️ CONFIRMAR EXCLUSÃO"):
                idx = df_produtos[df_produtos["Produto"] == prod_remover].index[0]
                aba_produtos.delete_rows(int(idx) + 2)
                st.rerun()
