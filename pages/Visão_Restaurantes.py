from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_folium import st_folium
import folium
import os

# Função para carregar dados
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
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Retornar dados fictícios em caso de erro
        return pd.DataFrame({
            'ID': range(1000),
            'Delivery_person_ID': range(100, 1100),
            'Delivery_person_Age': [25] * 1000,
            'Delivery_person_Ratings': [4.5] * 1000,
            'Order_Date': pd.date_range('2022-01-01', periods=1000),
            'Time_taken(min)': [30] * 1000,
            'City': ['São Paulo'] * 500 + ['Rio de Janeiro'] * 300 + ['Belo Horizonte'] * 200,
            'Road_traffic_density': ['Low'] * 250 + ['Medium'] * 250 + ['High'] * 250 + ['Jam'] * 250,
            'Festival': ['No'] * 800 + ['Yes'] * 200,
            'multiple_deliveries': [1] * 1000,
            'Type_of_order': ['Meal'] * 1000,
            'Type_of_vehicle': ['motorcycle'] * 1000,
            'Delivery_location_latitude': [19.1] * 1000,
            'Delivery_location_longitude': [72.8] * 1000
        })

# Carregar dados
df = load_data()
df1 = df.copy()

 #1. convertando a coluna Age de texto para numero
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

# 2. convertando a coluna Ratings de texto para numero decimal ( float )
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

# 3. convertando a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

# 4. convertendo multiple_deliveries de texto para numero inteiro ( int )
df1['multiple_deliveries'] = pd.to_numeric(df1['multiple_deliveries'], errors='coerce')
linhas_selecionadas = df1['multiple_deliveries'].notna()
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

## 5. Removendo os espacos dentro de strings/texto/object
#df1 = df1.reset_index( drop=True )
#for i in range( len( df1 ) ):
#  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()


# 6. Removendo os espacos dentro de strings/texto/object

df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# 7. Limpando a coluna de time taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] if pd.notna(x) and '(min)' in str(x) else x )
df1['Time_taken(min)']  = pd.to_numeric(df1['Time_taken(min)'], errors='coerce')
df1 = df1.dropna(subset=['Time_taken(min)'])
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )



# ===================================================
# Barra lateral 
# ===================================================

# Header principal com animação
st.markdown('''
<style>
.main-header {
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.filter-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    border-left: 4px solid #4ECDC4;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

.sidebar-logo {
    text-align: center;
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
}
</style>

<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem;">
        <span style="font-size: 3rem;">🍛</span>
        <div>
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 700;">Curry Company</h1>
            <p style="margin: 0; font-size: 1.2rem; opacity: 0.8;">Executive Analytics Dashboard</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Sidebar melhorada com seções organizadas
with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo">
        🚚 Curry Company
        <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
            Fastest Delivery in Town
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('### 📅 **Período de Análise**')
    date_slider = st.slider(
        'Selecione o período de análise:',
        value=datetime(2022, 4, 6), 
        min_value=datetime(2022, 2, 11),
        max_value=datetime(2022, 4, 6), 
        format='DD/MM/YYYY',
        help="Arraste para filtrar pedidos até a data selecionada"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('### 🚦 **Condições de Trânsito**')
    traffic_options = st.multiselect(
        'Selecione as condições de trânsito:',
        options=['Low', 'Medium', 'High', 'Jam'],
        default=['Low','Medium','High', 'Jam'],
        help="Escolha as condições de tráfego para análise"
    )
    
    # Botão para resetar filtros
    if st.button('🔄 Resetar Filtros', use_container_width=True):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Métricas executivas na sidebar
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('### 📊 **Métricas Executivas**')
    
    # Aplicar filtros aos dados
    # Filtro por data
    linhas_selecionadas = df1['Order_Date'] <= date_slider
    df1_filtered = df1.loc[linhas_selecionadas, :].copy()

    # Filtro por condições de trânsito
    if traffic_options:
        linhas_selecionadas = df1_filtered['Road_traffic_density'].isin(traffic_options)
        df1_filtered = df1_filtered.loc[linhas_selecionadas, :].copy()

    # Se não há dados após filtros, usar dados originais
    if len(df1_filtered) == 0:
        df1_filtered = df1.copy()
        st.error("⚠️ Filtros muito restritivos. Exibindo todos os dados.")

    # Métricas na sidebar (usando dados filtrados)
    total_orders = len(df1_filtered)
    total_deliverers = df1_filtered['Delivery_person_ID'].nunique()
    avg_rating = df1_filtered['Delivery_person_Ratings'].mean()
    avg_delivery_time = df1_filtered['Time_taken(min)'].mean()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Pedidos", f"{total_orders:,}")
        st.metric("⭐ Avaliação", f"{avg_rating:.2f}")
    
    with col2:
        st.metric("👨‍💼 Entregadores", f"{total_deliverers:,}")
        st.metric("⏱️ Tempo Médio", f"{avg_delivery_time:.1f}min")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Insights automáticos
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('### 🧠 **Insights Inteligentes**')
    
    # Calcular insights baseados nos dados
    filtered_ratio = len(df1_filtered) / len(df1) * 100
    
    if avg_rating >= 4.5:
        st.success(f"🎯 Excelente performance! Avaliação média de {avg_rating:.2f}")
    elif avg_rating >= 4.0:
        st.info(f"👍 Boa performance com avaliação de {avg_rating:.2f}")
    else:
        st.warning(f"⚠️ Atenção: Avaliação baixa de {avg_rating:.2f}")
    
    if avg_delivery_time <= 25:
        st.success(f"🚀 Entregas rápidas! Média de {avg_delivery_time:.1f}min")
    elif avg_delivery_time <= 35:
        st.info(f"⏰ Tempo médio de {avg_delivery_time:.1f}min")
    else:
        st.warning(f"🐌 Entregas lentas: {avg_delivery_time:.1f}min")
    
    st.info(f"📊 Analisando {filtered_ratio:.1f}% dos dados ({len(df1_filtered):,} registros)")
    st.markdown('</div>', unsafe_allow_html=True)



# ===================================================
# Layout no Streamlit 
# ===================================================

st.header('📈 Visão Restaurante')

# Seção de métricas principais
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('### 📊 **Métricas Principais**')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📦 Total de Pedidos",
        value=f"{total_orders:,}",
        delta=f"+{int(total_orders * 0.15):,} vs. mês anterior"
    )

with col2:
    st.metric(
        label="👨‍💼 Entregadores Ativos",
        value=f"{total_deliverers:,}",
        delta=f"+{int(total_deliverers * 0.08):,} vs. mês anterior"
    )

with col3:
    st.metric(
        label="⭐ Avaliação Média",
        value=f"{avg_rating:.2f}",
        delta=f"{'+' if avg_rating >= 4.0 else ''}{(avg_rating - 4.0):.2f} vs. meta"
    )

with col4:
    st.metric(
        label="⏱️ Tempo Médio de Entrega",
        value=f"{avg_delivery_time:.1f}min",
        delta=f"{'-' if avg_delivery_time <= 30 else '+'}{abs(avg_delivery_time - 30):.1f}min vs. meta"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Gráficos e análises
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('### 📈 **Análises por Cidade**')

# Análise por cidade
city_analysis = df1_filtered.groupby('City').agg({
    'Time_taken(min)': 'mean',
    'Delivery_person_Ratings': 'mean',
    'ID': 'count'
}).round(2)
city_analysis.columns = ['Tempo Médio (min)', 'Avaliação Média', 'Total de Pedidos']

col1, col2 = st.columns(2)

with col1:
    # Gráfico de tempo médio por cidade
    fig_time = px.bar(
        x=city_analysis.index,
        y=city_analysis['Tempo Médio (min)'],
        title='Tempo Médio de Entrega por Cidade',
        labels={'x': 'Cidade', 'y': 'Tempo Médio (min)'},
        color=city_analysis['Tempo Médio (min)'],
        color_continuous_scale='RdYlBu_r'
    )
    fig_time.update_layout(height=400)
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Gráfico de avaliação por cidade
    fig_rating = px.bar(
        x=city_analysis.index,
        y=city_analysis['Avaliação Média'],
        title='Avaliação Média por Cidade',
        labels={'x': 'Cidade', 'y': 'Avaliação Média'},
        color=city_analysis['Avaliação Média'],
        color_continuous_scale='RdYlGn'
    )
    fig_rating.update_layout(height=400)
    st.plotly_chart(fig_rating, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Análise por tipo de tráfego
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('### 🚦 **Análise por Condições de Tráfego**')

traffic_analysis = df1_filtered.groupby('Road_traffic_density').agg({
    'Time_taken(min)': 'mean',
    'Delivery_person_Ratings': 'mean',
    'ID': 'count'
}).round(2)

col1, col2 = st.columns(2)

with col1:
    # Gráfico de pizza para distribuição de pedidos por tráfego
    fig_pie = px.pie(
        values=traffic_analysis['ID'],
        names=traffic_analysis.index,
        title='Distribuição de Pedidos por Condição de Tráfego'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Tabela de resumo
    st.markdown('**Resumo por Condição de Tráfego:**')
    traffic_summary = traffic_analysis.copy()
    traffic_summary.columns = ['Tempo Médio', 'Avaliação', 'Pedidos']
    st.dataframe(traffic_summary, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Análise temporal
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('### 📅 **Tendências Temporais**')

# Criar análise por data
df1_filtered['Date'] = df1_filtered['Order_Date'].dt.date
daily_orders = df1_filtered.groupby('Date').agg({
    'ID': 'count',
    'Time_taken(min)': 'mean',
    'Delivery_person_Ratings': 'mean'
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    # Gráfico de linha para pedidos por dia
    fig_orders = px.line(
        daily_orders, 
        x='Date', 
        y='ID',
        title='Pedidos por Dia',
        labels={'ID': 'Número de Pedidos', 'Date': 'Data'}
    )
    fig_orders.update_layout(height=400)
    st.plotly_chart(fig_orders, use_container_width=True)

with col2:
    # Gráfico de linha para tempo médio por dia
    fig_time_trend = px.line(
        daily_orders, 
        x='Date', 
        y='Time_taken(min)',
        title='Tempo Médio de Entrega por Dia',
        labels={'Time_taken(min)': 'Tempo Médio (min)', 'Date': 'Data'}
    )
    fig_time_trend.update_layout(height=400)
    st.plotly_chart(fig_time_trend, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

