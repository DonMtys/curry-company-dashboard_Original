import plotly.express as px
import pandas as pd
import streamlit as st
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Curry Company - Analytics Dashboard",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.dashboard-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    border-left: 6px solid;
    transition: all 0.3s ease;
}

.dashboard-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.card-empresa {
    border-left-color: #FF6B6B;
    background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
}

.card-entregadores {
    border-left-color: #4ECDC4;
    background: linear-gradient(135deg, #fff 0%, #f0fffe 100%);
}

.card-restaurantes {
    border-left-color: #45B7D1;
    background: linear-gradient(135deg, #fff 0%, #f0f9ff 100%);
}

.metric-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
}

.feature-list {
    list-style: none;
    padding: 0;
}

.feature-list li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
}

.feature-list li:before {
    content: "✅ ";
    margin-right: 0.5rem;
}

.sidebar-logo {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 2rem;
    font-size: 1.3rem;
    font-weight: bold;
}

.company-info {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# Carregar dados básicos
@st.cache_data
def load_basic_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'train.csv')
        df = pd.read_csv(csv_path)
        
        # Limpeza básica dos dados - similar ao que está nos outros dashboards
        # Filtrar valores válidos
        if 'Delivery_person_Age' in df.columns:
            df = df[df['Delivery_person_Age'] != 'NaN ']
        if 'Road_traffic_density' in df.columns:
            df = df[df['Road_traffic_density'] != 'NaN ']
        if 'City' in df.columns:
            df = df[df['City'] != 'NaN ']
        if 'Festival' in df.columns:
            df = df[df['Festival'] != 'NaN ']
        
        # Converter ratings para numérico, tratando strings concatenadas
        if 'Delivery_person_Ratings' in df.columns:
            # Limpar e converter ratings
            df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(str)
            # Se houver valores concatenados, pegar apenas o primeiro número válido
            df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].str.extract(r'(\d+\.?\d*)').astype(float)
            df = df.dropna(subset=['Delivery_person_Ratings'])
        
        # Limpar Time_taken se existir
        if 'Time_taken(min)' in df.columns:
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
            df['Time_taken(min)'] = df['Time_taken(min)'].str.extract(r'(\d+)').astype(float)
            df = df.dropna(subset=['Time_taken(min)'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Se não conseguir carregar, retorna dados fictícios
        return pd.DataFrame({
            'ID': range(1000),
            'Delivery_person_ID': range(100, 1100),
            'Delivery_person_Ratings': [4.5] * 1000,
            'Time_taken(min)': [30] * 1000,
            'City': ['São Paulo'] * 500 + ['Rio de Janeiro'] * 300 + ['Belo Horizonte'] * 200
        })

# Carregar dados
df = load_basic_data()

# Header principal
st.markdown('''
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: center; gap: 2rem;">
        <span style="font-size: 4rem;">🍛</span>
        <div>
            <h1 style="margin: 0; font-size: 3.5rem; font-weight: 700;">Curry Company</h1>
            <p style="margin: 0; font-size: 1.5rem; opacity: 0.9;">Analytics Dashboard Hub - Fastest Delivery in Town</p>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo">
        🚚 Curry Company
        <div style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
            Dashboard Hub
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### 🧭 **Navegação Rápida**")
    
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <a href="http://localhost:8502" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E8E); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.3s ease;">
                🏢 <strong>Acessar Visão Empresa</strong>
            </div>
        </a>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <a href="http://localhost:8503" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #4ECDC4, #6FE3D6); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.3s ease;">
                👨‍💼 <strong>Acessar Visão Entregadores</strong>
            </div>
        </a>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <a href="http://localhost:8504" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #45B7D1, #6BC5E8); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.3s ease;">
                🍽️ <strong>Acessar Visão Restaurantes</strong>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Calcular métricas gerais
total_orders = len(df)
total_deliverers = df['Delivery_person_ID'].nunique() if 'Delivery_person_ID' in df.columns else 150
avg_rating = df['Delivery_person_Ratings'].mean() if 'Delivery_person_Ratings' in df.columns else 4.5
avg_delivery_time = df['Time_taken(min)'].mean() if 'Time_taken(min)' in df.columns else 30
total_cities = df['City'].nunique() if 'City' in df.columns else 3

# Métricas gerais em destaque
st.markdown("## 📊 **Visão Geral da Empresa**")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'''
    <div class="metric-container">
        <h3 style="margin: 0; color: #FF6B6B;">📦</h3>
        <h2 style="margin: 0;">{total_orders:,}</h2>
        <p style="margin: 0;">Total de Pedidos</p>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-container">
        <h3 style="margin: 0; color: #4ECDC4;">👨‍💼</h3>
        <h2 style="margin: 0;">{total_deliverers:,}</h2>
        <p style="margin: 0;">Entregadores</p>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-container">
        <h3 style="margin: 0; color: #45B7D1;">⭐</h3>
        <h2 style="margin: 0;">{avg_rating:.2f}</h2>
        <p style="margin: 0;">Avaliação Média</p>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-container">
        <h3 style="margin: 0; color: #FFA07A;">⏱️</h3>
        <h2 style="margin: 0;">{avg_delivery_time:.1f}min</h2>
        <p style="margin: 0;">Tempo Médio</p>
    </div>
    ''', unsafe_allow_html=True)

with col5:
    st.markdown(f'''
    <div class="metric-container">
        <h3 style="margin: 0; color: #9370DB;">🏙️</h3>
        <h2 style="margin: 0;">{total_cities}</h2>
        <p style="margin: 0;">Cidades Atendidas</p>
    </div>
    ''', unsafe_allow_html=True)

# Seção dos dashboards
st.markdown("## 🎯 **Nossos Dashboards Especializados**")
st.markdown("Explore nossos 3 dashboards analíticos especializados para diferentes perspectivas do negócio:")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("### 🏢 **Visão Empresa**")
        st.markdown("**Objetivo:** Análise executiva e estratégica do negócio")
        st.markdown("**Público-alvo:** Diretores, Gerentes e Executivos")
        
        st.markdown("#### 📋 **Funcionalidades:**")
        st.markdown("""
        - ✅ KPIs executivos e crescimento
        - ✅ Análise de tendências temporais  
        - ✅ Performance geral da empresa
        - ✅ Comparativos mensais
        - ✅ Insights estratégicos
        """)
        
        st.info("🚀 **Status:** ✅ Funcionando")
        st.success("📱 **Porta:** 8502")
        st.markdown('[🔗 **ACESSAR DASHBOARD EMPRESA**](http://localhost:8502)', unsafe_allow_html=True)
        
        # Botão estilizado
        st.markdown("""
        <a href="http://localhost:8502" target="_blank" style="text-decoration: none;">
            <div style="background: #FF6B6B; color: white; padding: 0.8rem; border-radius: 8px; text-align: center; margin-top: 1rem; cursor: pointer; font-weight: bold;">
                🚀 ENTRAR AGORA
            </div>
        </a>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("### 👨‍💼 **Visão Entregadores**")
        st.markdown("**Objetivo:** Monitoramento da força de trabalho")
        st.markdown("**Público-alvo:** Gerentes de Operações e RH")
        
        st.markdown("#### 📋 **Funcionalidades:**")
        st.markdown("""
        - ✅ Performance individual
        - ✅ Análise de avaliações
        - ✅ Tempos de entrega
        - ✅ Mapa de localizações
        - ✅ Indicadores de produtividade
        """)
        
        st.info("🚀 **Status:** ✅ Funcionando")
        st.success("� **Porta:** 8503")
        st.markdown('[🔗 **ACESSAR DASHBOARD ENTREGADORES**](http://localhost:8503)', unsafe_allow_html=True)
        
        # Botão estilizado
        st.markdown("""
        <a href="http://localhost:8503" target="_blank" style="text-decoration: none;">
            <div style="background: #4ECDC4; color: white; padding: 0.8rem; border-radius: 8px; text-align: center; margin-top: 1rem; cursor: pointer; font-weight: bold;">
                🚀 ENTRAR AGORA
            </div>
        </a>
        """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown("### 🍽️ **Visão Restaurantes**")
        st.markdown("**Objetivo:** Otimização de parcerias e qualidade")
        st.markdown("**Público-alvo:** Gerentes de Qualidade")
        
        st.markdown("#### 📋 **Funcionalidades:**")
        st.markdown("""
        - ✅ Análise por cidade/região
        - ✅ Impacto do tráfego
        - ✅ Qualidade das entregas
        - ✅ Tendências por área
        - ✅ Otimização de rotas
        """)
        
        st.info("🚀 **Status:** ✅ Funcionando")
        st.success("📱 **Porta:** 8504")
        st.markdown('[🔗 **ACESSAR DASHBOARD RESTAURANTES**](http://localhost:8504)', unsafe_allow_html=True)
        
        # Botão estilizado
        st.markdown("""
        <a href="http://localhost:8504" target="_blank" style="text-decoration: none;">
            <div style="background: #45B7D1; color: white; padding: 0.8rem; border-radius: 8px; text-align: center; margin-top: 1rem; cursor: pointer; font-weight: bold;">
                🚀 ENTRAR AGORA
            </div>
        </a>
        """, unsafe_allow_html=True)

# Seção de instruções
st.markdown("## 🚀 **Como Acessar os Dashboards**")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 📋 **Instruções de Uso:**
    
    1. **🏢 Visão Empresa** - ✅ **ATIVO**
       - 🌐 Acesse: [http://localhost:8502](http://localhost:8502)
       - 📊 Dashboard executivo completo
    
    2. **👨‍💼 Visão Entregadores** - ✅ **ATIVO**
       - 🌐 Acesse: [http://localhost:8503](http://localhost:8503)
       - 🎯 Análise focada nos entregadores
    
    3. **🍽️ Visão Restaurantes** - ✅ **ATIVO**
       - 🌐 Acesse: [http://localhost:8504](http://localhost:8504)
       - 🗺️ Análise geográfica e de qualidade
    
    ### 💡 **Como Funciona:**
    - ✅ **Todos os dashboards estão rodando** em portas diferentes
    - 🖱️ **Clique nos links** para navegar diretamente
    - 🔄 **Navegação entre abas** do navegador
    - 📱 **Compatível** com desktop e mobile
    - 🏠 **Sempre volte** para esta página Home (porta 8501)
    """)

    # Seção de links rápidos
    st.markdown("### 🚀 **Acesso Direto aos Dashboards:**")
    
    col_link1, col_link2, col_link3 = st.columns(3)
    
    with col_link1:
        st.markdown("""
        <a href="http://localhost:8502" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E8E); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(255,107,107,0.3);">
                <h3 style="margin: 0;">🏢 EMPRESA</h3>
                <p style="margin: 0.5rem 0 0 0;">Clique para acessar</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col_link2:
        st.markdown("""
        <a href="http://localhost:8503" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #4ECDC4, #6FE3D6); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(78,205,196,0.3);">
                <h3 style="margin: 0;">👨‍💼 ENTREGADORES</h3>
                <p style="margin: 0.5rem 0 0 0;">Clique para acessar</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col_link3:
        st.markdown("""
        <a href="http://localhost:8504" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #45B7D1, #6BC5E8); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(69,183,209,0.3);">
                <h3 style="margin: 0;">🍽️ RESTAURANTES</h3>
                <p style="margin: 0.5rem 0 0 0;">Clique para acessar</p>
            </div>
        </a>
        """, unsafe_allow_html=True)

with col2:
    # Gráfico simples de distribuição
    if 'City' in df.columns:
        city_dist = df['City'].value_counts()
        fig_pie = px.pie(
            values=city_dist.values,
            names=city_dist.index,
            title='📍 Distribuição por Cidade',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("📊 Gráfico será exibido quando os dados estiverem disponíveis")

# Seção sobre a empresa
st.markdown("## 🎯 **Sobre a Curry Company**")

col_about1, col_about2 = st.columns([2, 1])

with col_about1:
    st.markdown("""
    A **Curry Company** é líder em delivery de comida rápida e eficiente. 
    Nosso compromisso é entregar refeições deliciosas no menor tempo possível, 
    mantendo a mais alta qualidade de serviço.
    """)
    
    st.markdown("### 🚀 **Nossa Missão**")
    st.markdown("Conectar pessoas à comida que amam através de tecnologia de ponta e excelência operacional.")
    
    st.markdown("### 🎯 **Nossos Valores**")
    st.markdown("""
    - ⚡ **Rapidez:** Entregas em tempo recorde
    - 🍽️ **Qualidade:** Comida sempre fresca  
    - 💻 **Tecnologia:** Inovação constante
    - 🌱 **Sustentabilidade:** Compromisso ambiental
    """)

with col_about2:
    st.markdown("### 📈 **Nossos Números**")
    
    # Cards individuais para cada métrica
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0.5rem 0; text-align: center;">
        <span style="font-size: 1.8rem; color: #FF6B6B;">🏙️</span>
        <h3 style="margin: 0.3rem 0; color: #FF6B6B; font-size: 1.5rem;">{total_cities}</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Cidades Atendidas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0.5rem 0; text-align: center;">
        <span style="font-size: 1.8rem; color: #4ECDC4;">👨‍💼</span>
        <h3 style="margin: 0.3rem 0; color: #4ECDC4; font-size: 1.5rem;">{total_deliverers:,}</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Entregadores Ativos</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0.5rem 0; text-align: center;">
        <span style="font-size: 1.8rem; color: #45B7D1;">📦</span>
        <h3 style="margin: 0.3rem 0; color: #45B7D1; font-size: 1.5rem;">{total_orders:,}</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Pedidos Processados</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0.5rem 0; text-align: center;">
        <span style="font-size: 1.8rem; color: #FFA07A;">⭐</span>
        <h3 style="margin: 0.3rem 0; color: #FFA07A; font-size: 1.5rem;">{avg_rating:.1f}★</h3>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">Avaliação Média</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p style="font-size: 1.1rem;">© 2025 Curry Company - Analytics Dashboard Hub 🍛</p>
    <p>Fastest Delivery in Town | Desenvolvido com ❤️ usando Streamlit</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        🏢 Visão Empresa | 👨‍💼 Visão Entregadores | 🍽️ Visão Restaurantes
    </p>
</div>
""", unsafe_allow_html=True)
