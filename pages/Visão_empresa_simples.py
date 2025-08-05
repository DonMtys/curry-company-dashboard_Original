import plotly.express as px
import pandas as pd
import streamlit as st
from datetime import datetime
import os

# CSS personalizado
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(255,107,107,0.3);
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Função para carregar e limpar dados
@st.cache_data
def load_data():
    try:
        # Tentar carregar do diretório atual (Streamlit Cloud)
        if os.path.exists('train.csv'):
            df = pd.read_csv('train.csv')
        # Tentar carregar do diretório pai (estrutura local)
        elif os.path.exists('../train.csv'):
            df = pd.read_csv('../train.csv')
        # Último recurso - buscar na raiz do projeto
        else:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(script_dir, 'train.csv')
            df = pd.read_csv(csv_path)
        
        # Limpeza básica
        df = df[df['Delivery_person_Age'] != 'NaN ']
        df = df[df['Road_traffic_density'] != 'NaN ']
        df = df[df['City'] != 'NaN ']
        df = df[df['Festival'] != 'NaN ']
        
        # Converter tipos
        df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
        df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y', errors='coerce')
        
        # Limpar time_taken
        df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
        df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').astype(float)
        
        # Remover linhas com valores nulos
        df = df.dropna()
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Carregar dados
df = load_data()

# Header
st.markdown('''
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🏢 Curry Company - Visão Empresa</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Dashboard Executivo e Estratégico</p>
</div>
''', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏠 **Navegação**")
    if st.button("🏠 Voltar ao Home", use_container_width=True):
        st.markdown("**🔗 Acesse:** http://localhost:8501")
    
    st.markdown("---")
    st.markdown("### 📊 **Filtros**")
    
    # Filtro de data
    if not df.empty:
        data_min = df['Order_Date'].min().date()
        data_max = df['Order_Date'].max().date()
        
        data_slider = st.slider(
            "Selecione o período:",
            min_value=data_min,
            max_value=data_max,
            value=(data_min, data_max),
            format="DD/MM/YYYY"
        )
        
        # Aplicar filtro
        df_filtrado = df[
            (df['Order_Date'].dt.date >= data_slider[0]) & 
            (df['Order_Date'].dt.date <= data_slider[1])
        ]
    else:
        df_filtrado = df

if not df_filtrado.empty:
    # Métricas principais
    st.markdown("## 📈 **KPIs Principais**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pedidos = len(df_filtrado)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FF6B6B; margin: 0;">📦</h3>
            <h2 style="margin: 0.5rem 0;">{total_pedidos:,}</h2>
            <p style="margin: 0; color: #666;">Total de Pedidos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        entregadores_unicos = df_filtrado['Delivery_person_ID'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #4ECDC4; margin: 0;">👨‍💼</h3>
            <h2 style="margin: 0.5rem 0;">{entregadores_unicos:,}</h2>
            <p style="margin: 0; color: #666;">Entregadores Ativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rating_medio = df_filtrado['Delivery_person_Ratings'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #45B7D1; margin: 0;">⭐</h3>
            <h2 style="margin: 0.5rem 0;">{rating_medio:.2f}</h2>
            <p style="margin: 0; color: #666;">Avaliação Média</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        tempo_medio = df_filtrado['Time_taken(min)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FFA07A; margin: 0;">⏱️</h3>
            <h2 style="margin: 0.5rem 0;">{tempo_medio:.1f}min</h2>
            <p style="margin: 0; color: #666;">Tempo Médio de Entrega</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    st.markdown("## 📊 **Análises Estratégicas**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pedidos por dia
        pedidos_dia = df_filtrado.groupby('Order_Date').size().reset_index(name='Pedidos')
        fig_linha = px.line(
            pedidos_dia, 
            x='Order_Date', 
            y='Pedidos',
            title='📈 Evolução de Pedidos por Dia',
            color_discrete_sequence=['#FF6B6B']
        )
        fig_linha.update_layout(height=400)
        st.plotly_chart(fig_linha, use_container_width=True)
    
    with col2:
        # Distribuição por cidade
        pedidos_cidade = df_filtrado['City'].value_counts()
        fig_pizza = px.pie(
            values=pedidos_cidade.values,
            names=pedidos_cidade.index,
            title='🏙️ Distribuição de Pedidos por Cidade',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza.update_layout(height=400)
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    # Análise de tráfego
    st.markdown("### 🚦 **Análise de Tráfego**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trafego_pedidos = df_filtrado['Road_traffic_density'].value_counts()
        fig_bar = px.bar(
            x=trafego_pedidos.index,
            y=trafego_pedidos.values,
            title='Pedidos por Densidade de Tráfego',
            color=trafego_pedidos.values,
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Tempo médio por tráfego
        tempo_trafego = df_filtrado.groupby('Road_traffic_density')['Time_taken(min)'].mean().sort_values()
        fig_bar2 = px.bar(
            x=tempo_trafego.index,
            y=tempo_trafego.values,
            title='Tempo Médio de Entrega por Tráfego',
            color=tempo_trafego.values,
            color_continuous_scale='Blues'
        )
        fig_bar2.update_layout(height=400)
        st.plotly_chart(fig_bar2, use_container_width=True)
    
    # Tabela resumo
    st.markdown("### 📋 **Resumo Executivo**")
    
    resumo = df_filtrado.groupby('City').agg({
        'ID': 'count',
        'Delivery_person_Ratings': 'mean',
        'Time_taken(min)': 'mean'
    }).round(2)
    resumo.columns = ['Total Pedidos', 'Rating Médio', 'Tempo Médio (min)']
    resumo = resumo.reset_index()
    
    st.dataframe(resumo, use_container_width=True)

else:
    st.warning("⚠️ Nenhum dado disponível para exibir.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>🏢 <strong>Curry Company - Visão Empresa</strong> | Dashboard Executivo</p>
    <p>📊 Dados atualizados em tempo real</p>
</div>
""", unsafe_allow_html=True)
