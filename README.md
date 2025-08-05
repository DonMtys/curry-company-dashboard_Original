# 🍛 Curry Company Analytics Dashboard

## 📊 Executive Analytics Dashboard para Análise de Entregas

Dashboard interativo desenvolvido em Streamlit para análise completa de performance de entregas da Curry Company.

### 🚀 **Deploy na Nuvem - Streamlit Cloud**

Este projeto está configurado para deploy automático no **Streamlit Cloud**.

#### � **Como Fazer Deploy:**

1. **Acesse:** https://share.streamlit.io/
2. **Faça login** com sua conta GitHub
3. **Clique em "New app"**
4. **Configure:**
   - Repository: `DonMtys/curry-company-dashboard_Original`
   - Branch: `master`
   - Main file path: `Home.py`
5. **Clique em "Deploy!"**

### 📋 **Funcionalidades**

#### 🏠 **Home Portal**
- Visão geral da empresa
- Métricas principais em tempo real
- Navegação intuitiva para dashboards especializados
- Design responsivo e profissional

#### 📊 **Visão Empresa**
- KPIs executivos e crescimento
- Análise de tendências temporais
- Performance geral da empresa
- Comparativos mensais
- Insights estratégicos

#### 🚚 **Visão Entregadores**
- Performance individual dos entregadores
- Análise de avaliações e produtividade
- Tempos de entrega e eficiência
- Mapa de localizações
- Indicadores de performance

#### 🍽️ **Visão Restaurantes**
- Análise por cidade/região
- Impacto do tráfego nas entregas
- Qualidade das entregas
- Tendências por área geográfica
- Otimização de rotas

### 🛠️ **Tecnologias Utilizadas**

- **Python 3.8+**
- **Streamlit** - Framework web para dashboards
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **Folium** - Mapas interativos geográficos
- **Haversine** - Cálculos de distância geográfica

### 📦 **Estrutura do Projeto**

```
curry-company-dashboard/
├── Home.py                         # Página principal (ponto de entrada)
├── pages/
│   ├── Visão_empresa_simples.py   # Dashboard executivo
│   ├── Visão_Entregadores.py      # Análise de entregadores
│   └── Visão_Restaurantes.py      # Análise geográfica
├── train.csv                       # Dados das entregas
├── requirements.txt                # Dependências Python
├── .streamlit/
│   └── config.toml                # Configurações do Streamlit
└── README.md                       # Documentação
```

### � **Instalação Local**

```bash
# Clone o repositório
git clone https://github.com/DonMtys/curry-company-dashboard_Original.git
cd curry-company-dashboard_Original

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run Home_novo.py
```

### 🌐 **Deploy na Nuvem**

Este projeto está configurado para deploy automático no:
- **Streamlit Cloud** (Principal)
- **Heroku**
- **Railway**

### 📁 **Estrutura do Projeto**

```
curry-company-dashboard/
├── Home_novo.py                 # Portal principal
├── pages/
│   ├── Visão_Empresa.py        # Dashboard executivo
│   ├── Visão_Entregadores.py   # Analytics de entregadores
│   └── Visão_Restaurantes.py   # Analytics de restaurantes
├── train.csv                   # Dataset principal
├── requirements.txt            # Dependências Python
├── .streamlit/
│   └── config.toml            # Configurações do Streamlit
└── README.md                  # Este arquivo
```

### 📈 **Métricas Principais**

- **Volume de Pedidos**: Análise temporal e geográfica
- **Tempo de Entrega**: Performance e otimização
- **Avaliações**: Satisfação do cliente
- **Coverage Geográfica**: Expansão territorial

### 🎯 **KPIs Monitorados**

1. **Total de Pedidos**: Volume diário/semanal
2. **Tempo Médio de Entrega**: Performance logística
3. **Avaliação dos Clientes**: Qualidade do serviço
4. **Cidades Atendidas**: Expansão geográfica
5. **Performance dos Entregadores**: Produtividade individual

### 🔧 **Configuração**

O dashboard permite filtragem por:
- **Período**: Análise temporal customizada
- **Condições de Trânsito**: Impact no tempo de entrega
- **Regiões**: Performance geográfica
- **Tipo de Pedido**: Análise segmentada

### 📊 **Visualizações Disponíveis**

- **Gráficos de Tendência**: Evolução temporal
- **Mapas Interativos**: Distribuição geográfica
- **Gráficos de Pizza**: Distribuição categórica
- **Scatter Plots**: Correlações
- **Tabelas Dinâmicas**: Dados detalhados

### 👥 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### 📞 **Contato**

- **📧 Email**: contato@currycompany.com
- **📱 WhatsApp**: +55 (11) 9999-9999
- **🌐 Website**: www.currycompany.com

---

**Desenvolvido com ❤️ para otimizar operações de delivery**
