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

# --- CONEXÃO 100% BLINDADA VIA LINKS DE EXPORTAÇÃO EXCEL NATIVOS ---
try:
    # URL de exportação direta da planilha inteira como arquivo Excel (.xlsx) de forma pública
    url_excel = "https://google.com"
    
    # O Pandas faz a leitura baixando o arquivo direto usando o motor openpyxl (evita erros de urlopen)
    df_devedores = pd.read_excel(url_excel, sheet_name="Clientes", engine="openpyxl")
    df_produtos = pd.read_excel(url_excel, sheet_name="Produtos", engine="openpyxl")
    
    if df_devedores.empty:
        df_devedores = pd.DataFrame(columns=["Nome", "Telefone", "Limite", "Divida"])
    if df_produtos.empty:
        df_produtos = pd.DataFrame(columns=["Código", "Produto", "Preço", "Atacado", "Estoque", "Minimo"])
        
    df_devedores["Limite"] = pd.to_numeric(df_devedores["Limite"], errors='coerce').fillna(0.0)
    df_devedores["Divida"] = pd.to_numeric(df_devedores["Divida"], errors='coerce').fillna(0.0)
    df_produtos["Preço"] = pd.to_numeric(df_produtos["Preço"], errors='coerce').fillna(0.0)
    df_produtos["Atacado"] = pd.to_numeric(df_produtos["Atacado"], errors='coerce').fillna(0.0)
    df_produtos["Estoque"] = pd.to_numeric(df_produtos["Estoque"], errors='coerce').fillna(0).astype(int)
    df_produtos["Minimo"] = pd.to_numeric(df_produtos["Minimo"], errors='coerce').fillna(0).astype(int)

except Exception as e:
    st.error("⚠️ Erro crítico ao tentar processar o arquivo da planilha:")
    st.exception(e)
    st.stop()

opcoes_menu = ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"]
if 'menu_atual' not in st.session_state:
    st.session_state.menu_atual = "Dashboard Inicial"

st.markdown('<div class="topbar"><h2 style="margin:0; color:white;">🛍️ MERCADINHO PRO</h2><span>🟢 BANCO DE DADOS ONLINE</span></div>', unsafe_allow_html=True)

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
    
    st.info("💡 Como a planilha é pública e totalmente integrada, você pode gerenciar, cadastrar clientes e lançar/abater fiados abrindo o link diretamente no celular ou computador. O painel do Streamlit atualizará sozinho na hora.")
    
    # Botão limpo para o operador abrir a tabela e preencher na hora
    st.link_button("🔗 ABRIR PLANILHA NO GOOGLE SHEETS", "https://google.com", use_container_width=True)
    
    st.write("---")
    st.write("### Lista Geral de Contas Cadastradas")
    st.dataframe(df_devedores, use_container_width=True)

# ==========================================================
# 3. TELA: TABELAS DE PREÇO
# ==========================================================
elif menu == "Tabelas de Preço":
    st.markdown('<div class="dashboard-card"><h2>Tabelas de Preços e Estoque</h2></div>', unsafe_allow_html=True)
    
    st.info("📋 Modifique os preços, códigos de barra e quantidades de estoque abrindo a planilha pelo link abaixo. O painel do Streamlit atualizará as métricas e os gráficos em tempo real.")
    
    st.link_button("🔗 EDITAR PRODUTOS E ESTOQUE", "https://google.com", use_container_width=True)
    
    st.write("---")
    st.dataframe(df_produtos, use_container_width=True)
