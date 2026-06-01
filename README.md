# 🎾 João Fonseca Performance Center

Plataforma de análise esportiva desenvolvida em Python para monitorar a evolução da carreira do tenista João Fonseca através de dados históricos de partidas.

O projeto utiliza técnicas de Engenharia de Dados, Análise Exploratória, Visualização de Dados e Storytelling para transformar dados brutos em insights acionáveis sobre desempenho, evolução competitiva e perfil esportivo.

---

##  Objetivo

Criar uma plataforma analítica capaz de responder perguntas como:

* Como João Fonseca evoluiu ao longo dos anos?
* Em quais pisos apresenta melhor desempenho?
* Como performa contra adversários de diferentes níveis?
* Qual foi sua melhor vitória da carreira?
* Quais são seus principais pontos fortes e oportunidades de melhoria?

O foco não é apenas exibir dados, mas gerar conclusões que apoiem a tomada de decisão.

---

##  Funcionalidades

### Coleta de Dados

* Extração automática de partidas ATP
* Consolidação de múltiplas temporadas
* Construção de base histórica

### Tratamento de Dados

* Padronização de resultados
* Identificação automática de adversários
* Classificação de ranking
* Categorização de torneios

### Dashboard Interativo

* Evolução da carreira
* Desempenho por piso
* Análise de adversários
* Performance por torneio
* Scout competitivo

### Insights Automáticos

* Melhor piso
* Pior piso
* Melhor vitória da carreira
* Aproveitamento contra Top 50 e Top 100
* Identificação de tendências de desempenho

---

##  Tecnologias Utilizadas

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
├── joao_fonseca_historico_bruto.xlsx
├── joao_fonseca_historico_tratado.xlsx
├── joao_fonseca_relatorio_historico.xlsx
│
├── requirements.txt
└── README.md
```

---

##  Como Executar

### Instalar dependências

```bash
py -m pip install -r requirements.txt
```

### Executar dashboard

```bash
py -m streamlit run app.py
```

---

##  Principais Descobertas

Com base nos dados históricos analisados:

* Melhor desempenho em quadras Hard
* Aproveitamento geral superior a 60%
* Maior dificuldade contra adversários de elite
* Performance mais consistente em pisos rápidos
* Gramado identificado como principal oportunidade de evolução

---

## Aprendizados do Projeto

Este projeto permitiu aplicar conceitos de:

* ETL (Extract, Transform, Load)
* Engenharia de Dados
* Manipulação de dados com Pandas
* Visualização de Dados
* Storytelling com Dados
* Desenvolvimento de Dashboards
* Análise Esportiva

---

##  Próximos Passos

* Inclusão de dados Challenger e ITF
* Integração com rankings ATP atualizados
* Modelos preditivos de vitória
* Análise de desempenho por adversário
* Machine Learning aplicado ao scouting esportivo

---

##  Autor

Lucas Vieira

Projeto desenvolvido para fins de estudo, portfólio e evolução técnica em Análise de Dados, Python e Data Visualization.
