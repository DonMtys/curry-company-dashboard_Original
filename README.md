# 🍛 Curry Company Analytics Dashboard

## 📊 Executive Analytics Dashboard para Análise de Entregas

Dashboard interativo desenvolvido em Streamlit para análise completa de performance de entregas da Curry Company.

### 🚀 **Demonstração Online**
🔗 **[Acesse o Dashboard ao Vivo](https://seu-app.streamlit.app)**

### 📋 **Funcionalidades**

#### 🏠 **Home Portal**
- Visão geral da empresa
- Métricas principais
- Navegação para dashboards especializados

#### 📊 **Visão Empresa**
- KPIs executivos
- Análise de tendências
- Performance por região

#### 🚚 **Visão Entregadores**
- Performance individual
- Métricas de produtividade
- Análise geográfica

#### 🍽️ **Visão Restaurantes**
- Análise de parceiros
- Performance por tipo de comida
- Métricas de qualidade

### 🛠️ **Tecnologias Utilizadas**

- **Python 3.8+**
- **Streamlit** - Framework web
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações interativas
- **Folium** - Mapas interativos
- **Haversine** - Cálculos geográficos

### 📦 **Instalação Local**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/curry-company-dashboard.git
cd curry-company-dashboard

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
