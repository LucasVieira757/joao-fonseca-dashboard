#  João Fonseca Performance Center

Plataforma de análise esportiva desenvolvida em Python para acompanhar a evolução da carreira do tenista João Fonseca através de dados históricos de partidas ATP.

O projeto aplica conceitos de Engenharia de Dados, ETL, Análise Exploratória de Dados (EDA), Storytelling e Data Visualization para transformar dados esportivos em insights acionáveis.

---

##  Dashboard

> Adicione aqui uma imagem do dashboard após a publicação.

```markdown
![Dashboard](imagens/dashboard.png)
```

---

##  Aplicação Online

> Adicione aqui o link da aplicação após a publicação.

```text
https://SEU-LINK.streamlit.app
```

---

##  Objetivo

Responder perguntas relevantes sobre a evolução competitiva de João Fonseca:

* Como seu desempenho evoluiu ao longo dos anos?
* Qual é seu melhor piso?
* Qual é sua taxa de vitória por categoria de torneio?
* Como performa contra adversários Top 50 e Top 100?
* Quais são suas melhores vitórias da carreira?
* Onde estão suas principais oportunidades de evolução?

---

##  Principais Funcionalidades

### Coleta de Dados

* Extração de partidas ATP
* Consolidação de temporadas
* Construção de base histórica

### Tratamento de Dados

* Identificação automática de adversários
* Classificação por ranking
* Categorização de torneios
* Padronização dos resultados

### Dashboard Analítico

* Evolução da carreira
* Desempenho por piso
* Análise de adversários
* Performance por torneio
* Scout competitivo

### Insights Automáticos

* Melhor piso
* Pior piso
* Melhor vitória da carreira
* Taxa de vitória contra Top 50 e Top 100
* Identificação de padrões de desempenho

---

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas
* Streamlit
* Plotly
* OpenPyXL

---

##  Estrutura do Projeto

```text
joao-fonseca-performance-center
│
├── app.py
│
├── coleta_historica.py
├── tratamento_historico.py
├── analise_historica.py
│
├── main.py
├── analise_joao.py
├── dashboard_data.py
│
├── joao_fonseca_partidas.xlsx
├── joao_fonseca_partidas_tratado.xlsx
├── joao_fonseca_partidas_analisada.xlsx
│
├── joao_fonseca_historico_bruto.xlsx
├── joao_fonseca_historico_tratado.xlsx
├── joao_fonseca_relatorio_historico.xlsx
│
├── requirements.txt
└── README.md
```

### Fluxo de Construção

O projeto foi desenvolvido de forma incremental:

1. Coleta dos dados ATP
2. Tratamento e padronização
3. Construção da base histórica
4. Análises exploratórias
5. Geração de relatórios
6. Desenvolvimento do dashboard interativo em Streamlit

Os arquivos intermediários foram mantidos no repositório para documentar a evolução do projeto e servir como material de estudo e consulta.

```
```

```

---

##  Como Executar

Instale as dependências:

```bash
py -m pip install -r requirements.txt
```

Execute o dashboard:

```bash
py -m streamlit run app.py
```

---

##  Principais Descobertas

Com base nos dados históricos analisados:

* Melhor desempenho em quadras Hard.
* Aproveitamento geral superior a 60%.
* Redução de desempenho contra adversários de elite.
* Maior consistência em pisos rápidos.
* Gramado identificado como principal oportunidade de evolução.

---

##  Conceitos Aplicados

* ETL (Extract, Transform, Load)
* Engenharia de Dados
* Análise Exploratória de Dados (EDA)
* Storytelling com Dados
* Data Visualization
* Desenvolvimento de Dashboards
* Análise Esportiva

---

##  Próximas Evoluções

* Inclusão de torneios Challenger e ITF.
* Integração com rankings ATP atualizados.
* Modelos preditivos de desempenho.
* Machine Learning aplicado ao scouting esportivo.
* Análise detalhada por adversário.

---

##  Autor

Lucas Vieira

Projeto desenvolvido para estudo, portfólio e evolução técnica em Python, Análise de Dados e Visualização de Dados.
