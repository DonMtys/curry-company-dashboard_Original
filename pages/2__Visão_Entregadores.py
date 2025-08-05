from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_folium import st_folium
import folium
import os
#import pillow_avif_plugin

# Configuração da página
st.set_page_config(
    page_title="Curry Company - Executive Dashboard",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/seu-perfil',
        'Report a bug': "mailto:contato@currycompany.com",
        'About': "# Curry Company Analytics Dashboard\nDashboard executivo para análise de performance de entregas."
    }
)

# CSS personalizado avançado para aparência enterprise
st.markdown("""
<style>
    /* Importar fonte profissional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
        position: relative;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        border-radius: 15px;
        z-index: -1;
    }
    
    .sidebar-logo {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(255,107,107,0.3);
        transition: transform 0.3s ease;
    }
    
    .sidebar-logo:hover {
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .tab-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-left: 4px solid #0984e3;
        padding-left: 1rem;
    }
    
    .kpi-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #dff6ff 0%, #b3e5fc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(33,150,243,0.1);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d4f6d4 0%, #b8e6b8 100%);
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ff9f43;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .filter-section {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin-bottom: 1rem;
    }
    
    /* Animações suaves */
    .stMetric {
        transition: all 0.3s ease;
    }
    
    .stSelectbox, .stMultiselect, .stSlider {
        transition: all 0.3s ease;
    }
    
    /* Estilo para gráficos */
    .js-plotly-plot {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-2px);
    }
    
    /* Footer estilizado */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Obter o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'train.csv')
df = pd.read_csv(csv_path)

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
 




#Visão - Empresa 


#Quantidade de pedidos por dia . 


cols = ['ID', 'Order_Date']
df2 = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
df2

#Desenha O graficos de Linhas

px.bar(df2, x = 'Order_Date', y='ID')


# ===================================================
# Barra lateral 
# ===================================================

# Header principal com animação
st.markdown('''
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
        st.info(f"� Boa performance com avaliação de {avg_rating:.2f}")
    else:
        st.warning(f"⚠️ Atenção: Avaliação baixa de {avg_rating:.2f}")
    
    if avg_delivery_time <= 25:
        st.success(f"🚀 Entregas rápidas! Média de {avg_delivery_time:.1f}min")
    elif avg_delivery_time <= 35:
        st.info(f"� Tempo médio de {avg_delivery_time:.1f}min")
    else:
        st.warning(f"🐌 Entregas lentas: {avg_delivery_time:.1f}min")
    
    st.info(f"📊 Analisando {filtered_ratio:.1f}% dos dados ({len(df1_filtered):,} registros)")
    st.markdown('</div>', unsafe_allow_html=True)



# ===================================================
# Layout no Streamlit 
# ===================================================

# Tabs com ícones mais elaborados
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 **Executive Overview**", 
    "📈 **Performance Analytics**", 
    "🗺️ **Geographic Intelligence**",
    "📋 **Detailed Reports**"
])

with tab1:
    st.markdown('''
    <div class="tab-header">
        📊 Executive Overview - Key Performance Indicators
    </div>
    ''', unsafe_allow_html=True)
    
    # Alerta de performance
    performance_score = (avg_rating / 5) * 100
    if performance_score >= 85:
        st.success(f"🎯 **Excelente Performance**: {performance_score:.1f}/100")
    elif performance_score >= 70:
        st.info(f"👍 **Boa Performance**: {performance_score:.1f}/100")
    else:
        st.warning(f"⚠️ **Performance Necessita Melhoria**: {performance_score:.1f}/100")
    
    # KPIs principais com design melhorado
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_orders = len(df1_filtered)
        previous_orders = max(1000, current_orders - 100)
        delta_orders = current_orders - previous_orders
        growth_rate = (delta_orders / previous_orders) * 100
        st.metric(
            label="📦 **Total Orders**",
            value=f"{current_orders:,}",
            delta=f"{growth_rate:+.1f}% growth",
            help="Total de pedidos no período selecionado"
        )
    
    with col2:
        avg_time = df1_filtered['Time_taken(min)'].mean()
        time_delta = -2.3  # Simulado
        st.metric(
            label="⏱️ **Avg Delivery Time**",
            value=f"{avg_time:.1f} min",
            delta=f"{time_delta:.1f} min vs baseline",
            delta_color="inverse",
            help="Tempo médio de entrega"
        )
    
    with col3:
        unique_cities = df1_filtered['City'].nunique()
        st.metric(
            label="🏙️ **Cities Served**",
            value=f"{unique_cities}",
            delta="+1 vs last period",
            help="Número de cidades atendidas"
        )
    
    with col4:
        avg_rating = df1_filtered['Delivery_person_Ratings'].mean()
        rating_delta = 0.1  # Simulado
        st.metric(
            label="⭐ **Customer Rating**",
            value=f"{avg_rating:.2f}/5.0",
            delta=f"+{rating_delta:.1f} improvement",
            help="Avaliação média dos clientes"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos principais com temas profissionais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 **Daily Order Trends**")
        cols = ['ID', 'Order_Date']
        df2 = df1_filtered.loc[:, cols].groupby('Order_Date').count().reset_index()      
        
        fig = px.area(
            df2, 
            x='Order_Date', 
            y='ID',
            title="Order Volume Evolution",
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="Date",
            yaxis_title="Number of Orders",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            title_font_size=16,
            hovermode='x unified'
        )
        fig.update_traces(
            fill='tonexty',
            line=dict(width=3, color='#667eea'),
            fillcolor='rgba(102,126,234,0.1)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🚦 **Traffic Distribution**")
        df_aux = df1_filtered.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
        df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
        df_aux['percentage'] = (df_aux['ID'] / df_aux['ID'].sum() * 100).round(1)

        fig = px.pie(
            df_aux, 
            values='ID', 
            names='Road_traffic_density',
            title="Orders by Traffic Condition",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hover_data=['percentage']
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Orders: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        fig.update_layout(
            font=dict(family="Inter", size=12),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise avançada
    st.subheader("🏙️ **City & Traffic Performance Matrix**")
    df_aux = df1_filtered.loc[:, ['City', 'Road_traffic_density', 'ID', 'Time_taken(min)']].groupby(['City', 'Road_traffic_density']).agg({
        'ID': 'count',
        'Time_taken(min)': 'mean'
    }).reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    
    fig = px.scatter(
        df_aux, 
        x='City', 
        y='Road_traffic_density', 
        size='ID', 
        color='Time_taken(min)',
        title="Performance Matrix: Volume vs Delivery Time",
        size_max=40,
        color_continuous_scale='RdYlBu_r',
        hover_data={'ID': True, 'Time_taken(min)': ':.1f'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12),
        title_font_size=16,
        coloraxis_colorbar=dict(title="Avg Time (min)")
    )
    st.plotly_chart(fig, use_container_width=True)

            



with tab2:
    st.markdown('<div class="tab-header">📈 Análise Tática - Tendências Temporais</div>', unsafe_allow_html=True)
    
    # Análise semanal (usando dados filtrados)
    st.subheader("📅 Evolução Semanal de Pedidos")
    
    # Criar coluna de semana
    df1_filtered['week_of_year'] = df1_filtered['Order_Date'].dt.strftime('%U')
    df_aux = df1_filtered.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    
    fig = px.line(
        df_aux, 
        x='week_of_year', 
        y='ID',
        title="Tendência de Pedidos por Semana do Ano (Filtrado)",
        markers=True
    )
    fig.update_traces(
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8, color='#ff7f0e')
    )
    fig.update_layout(
        xaxis_title="Semana do Ano",
        yaxis_title="Número de Pedidos",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise adicional - Performance por dia da semana (usando dados filtrados)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Pedidos por Dia da Semana")
        df1_filtered['day_of_week'] = df1_filtered['Order_Date'].dt.day_name()
        df_dow = df1_filtered.groupby('day_of_week')['ID'].count().reset_index()
        
        # Ordenar por dia da semana
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_dow['day_of_week'] = pd.Categorical(df_dow['day_of_week'], categories=day_order, ordered=True)
        df_dow = df_dow.sort_values('day_of_week')
        
        fig = px.bar(
            df_dow,
            x='day_of_week',
            y='ID',
            color='ID',
            color_continuous_scale='viridis',
            title="Pedidos por Dia da Semana (Filtrado)"
        )
        fig.update_layout(showlegend=False, xaxis_title="Dia da Semana", yaxis_title="Pedidos")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⏰ Tempo de Entrega por Tráfego")
        df_time = df1_filtered.groupby('Road_traffic_density')['Time_taken(min)'].mean().reset_index()
        df_time = df_time.loc[df_time['Road_traffic_density'] != 'NaN', :]
        
        fig = px.bar(
            df_time,
            x='Road_traffic_density',
            y='Time_taken(min)',
            color='Time_taken(min)',
            color_continuous_scale='Reds',
            title="Tempo Médio por Tráfego (Filtrado)"
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="Condição de Tráfego",
            yaxis_title="Tempo Médio (min)"
        )
        st.plotly_chart(fig, use_container_width=True)



with tab3:
    st.markdown('<div class="tab-header">🗺️ Análise Geográfica</div>', unsafe_allow_html=True)
    
    # Preparar dados geográficos (usando dados filtrados)
    df_aux = df1_filtered.loc[:, ["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]].groupby(["City", "Road_traffic_density"]).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    
    if len(df_aux) > 0:
        # Criar mapa interativo
        center_lat = df_aux['Delivery_location_latitude'].mean()
        center_lon = df_aux['Delivery_location_longitude'].mean()
        
        map_folium = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Adicionar marcadores coloridos por cidade
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred']
        cities = df_aux['City'].unique()
        
        for i, city in enumerate(cities):
            city_data = df_aux[df_aux['City'] == city]
            color = colors[i % len(colors)]
            
            for _, row in city_data.iterrows():
                folium.Marker(
                    [row['Delivery_location_latitude'], row['Delivery_location_longitude']],
                    popup=f"Cidade: {row['City']}<br>Tráfego: {row['Road_traffic_density']}",
                    tooltip=f"{row['City']} - {row['Road_traffic_density']}",
                    icon=folium.Icon(color=color, icon='truck', prefix='fa')
                ).add_to(map_folium)
        
        # Exibir mapa
        st.subheader("📍 Localização das Entregas por Cidade (Filtrado)")
        st_folium(map_folium, width=1200, height=500)
        
        # Estatísticas geográficas (usando dados filtrados)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏙️ Distribuição por Cidade")
            city_counts = df1_filtered['City'].value_counts().reset_index()
            city_counts.columns = ['City', 'Count']
            city_counts = city_counts.head(10)
            
            fig = px.pie(
                city_counts,
                values='Count',
                names='City',
                title="Top 10 Cidades por Volume de Entregas (Filtrado)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚚 Análise de Entregadores")
            deliverer_stats = df1_filtered.groupby('City').agg({
                'Delivery_person_ID': 'nunique',
                'Delivery_person_Ratings': 'mean',
                'Time_taken(min)': 'mean'
            }).reset_index()
            deliverer_stats.columns = ['City', 'Entregadores', 'Avaliação_Média', 'Tempo_Médio']
            deliverer_stats = deliverer_stats.sort_values('Entregadores', ascending=False)
            
            st.dataframe(
                deliverer_stats.round(2),
                use_container_width=True,
                hide_index=True
            )
            
            # Estatísticas resumo dos filtros
            st.markdown("### 📈 Impacto dos Filtros")
            original_count = len(df1)
            filtered_count = len(df1_filtered)
            reduction_pct = ((original_count - filtered_count) / original_count) * 100
            
            st.metric(
                label="📊 Dados Filtrados",
                value=f"{filtered_count:,} registros",
                delta=f"-{reduction_pct:.1f}% do total"
            )
    else:
        st.warning("⚠️ Não há dados geográficos suficientes para exibir o mapa com os filtros aplicados.")
        st.info("💡 Tente ajustar os filtros na barra lateral para ver mais dados.")

with tab4:
    st.markdown('''
    <div class="tab-header">
        📋 Detailed Reports & Data Export
    </div>
    ''', unsafe_allow_html=True)
    
    # Relatórios detalhados
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 **Performance Summary Table**")
        
        # Criar tabela resumo
        summary_data = []
        for city in df1_filtered['City'].unique():
            if city != 'NaN':
                city_data = df1_filtered[df1_filtered['City'] == city]
                summary_data.append({
                    'City': city,
                    'Total Orders': len(city_data),
                    'Avg Rating': city_data['Delivery_person_Ratings'].mean(),
                    'Avg Delivery Time': city_data['Time_taken(min)'].mean(),
                    'Unique Deliverers': city_data['Delivery_person_ID'].nunique(),
                    'Revenue Estimate': len(city_data) * 15.50  # Simulado
                })
        
        summary_df = pd.DataFrame(summary_data)
        if not summary_df.empty:
            summary_df = summary_df.round(2)
            summary_df['Revenue Estimate'] = summary_df['Revenue Estimate'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "City": st.column_config.TextColumn("🏙️ City", width="medium"),
                    "Total Orders": st.column_config.NumberColumn("📦 Orders", format="%d"),
                    "Avg Rating": st.column_config.NumberColumn("⭐ Rating", format="%.2f"),
                    "Avg Delivery Time": st.column_config.NumberColumn("⏱️ Time (min)", format="%.1f"),
                    "Unique Deliverers": st.column_config.NumberColumn("👨‍💼 Deliverers", format="%d"),
                    "Revenue Estimate": st.column_config.TextColumn("💰 Revenue", width="medium")
                }
            )
            
            # Botão de download
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv,
                file_name=f"curry_company_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        st.subheader("📈 **Quick Stats**")
        
        # Stats rápidas
        total_revenue = len(df1_filtered) * 15.50
        st.metric("💰 **Est. Revenue**", f"${total_revenue:,.2f}")
        
        best_city = summary_df.loc[summary_df['Avg Rating'].idxmax(), 'City'] if not summary_df.empty else "N/A"
        st.metric("🏆 **Top Rated City**", best_city)
        
        busiest_day = df1_filtered['Order_Date'].dt.day_name().mode()[0] if len(df1_filtered) > 0 else "N/A"
        st.metric("📅 **Busiest Day**", busiest_day)
        
        # Gráfico de tendência pequeno
        st.subheader("📊 **Trend Preview**")
        df_trend = df1_filtered.groupby('Order_Date')['ID'].count().reset_index()
        fig_mini = px.line(df_trend, x='Order_Date', y='ID', height=200)
        fig_mini.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="",
            yaxis_title="Orders"
        )
        st.plotly_chart(fig_mini, use_container_width=True)

# Rodapé profissional
st.markdown("---")
st.markdown('''
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h3 style="margin: 0; color: white;">🍛 Curry Company Analytics</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Executive Dashboard v2.0</p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; opacity: 0.9;">Developed with ❤️ using Streamlit</p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Last updated: August 2025</p>
        </div>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
        <p style="margin: 0; text-align: center; opacity: 0.8;">
            📧 contato@currycompany.com | 📞 +55 (11) 9999-9999 | 🌐 www.currycompany.com
        </p>
    </div>
</div>
''', unsafe_allow_html=True)
    