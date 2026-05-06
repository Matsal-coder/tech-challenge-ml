# 📊 Tech Challenge — Previsão de Churn com Pipeline End-to-End

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um sistema completo de Machine Learning para previsão de churn (cancelamento de clientes) em uma operadora de telecomunicações.

A solução foi construída de ponta a ponta, incluindo:

* Análise exploratória dos dados (EDA)
* Modelagem com algoritmos tradicionais e redes neurais
* Comparação de modelos com métricas técnicas e de negócio
* Feature engineering orientado a comportamento do cliente
* Deploy de um modelo via API REST
* Estruturação do projeto seguindo boas práticas de engenharia de ML

---

## 🧠 Problema de Negócio

A empresa enfrenta alta taxa de churn e deseja identificar clientes com maior probabilidade de cancelamento, permitindo ações proativas de retenção.

Além da previsão, o projeto considera:

* custo de campanhas de retenção (falsos positivos)
* perda de receita (falsos negativos)

---

## 📁 Estrutura do Projeto

```
.
├── data/
├── models/
├── notebooks/
├── src/
│   └── churn_model/
│       ├── api.py
│       ├── config.py
│       ├── data_schema.py
│       ├── logging_config.py
│       ├── model.py
│       ├── predict.py
│       └── schemas.py
├── tests/
├── examples/
├── pyproject.toml
├── Makefile
└── README.md
```

---

## 🔬 Etapas do Projeto

### 📌 Etapa 1 — EDA e Baselines

* Análise exploratória dos dados
* Tratamento de dados
* Definição de métricas
* Modelos baseline:

  * Dummy Classifier
  * Regressão Logística
  * Random Forest

---

### 📌 Etapa 2 — Modelagem com Redes Neurais

* Implementação de MLP com PyTorch
* Treinamento com early stopping
* Comparação com modelos baseline
* Análise de trade-offs (precision vs recall)

---

### 📌 Etapa 2.5 — Métricas de Negócio

* Definição de custo:

  * Falso positivo → custo de campanha → R$100
  * Falso negativo → perda de receita → ticket médio × meses de retenção
* Otimização de threshold
* Cálculo de valor líquido

---

### 📌 Etapa 3 — Engenharia e API

* Refatoração para `src/`
* Pipeline reutilizável com preprocessador salvo
* API REST com FastAPI:

  * `GET /health`
  * `POST /predict`
* Validação com:

  * Pydantic (input/output)
  * Pandera (schema de dados)
* Logging estruturado
* Middleware de latência
* Testes automatizados:

  * Smoke
  * Schema
  * API
  * Casos de erro

* Testes cobrem:

- validação de input
- funcionamento da API
- casos de erro
---

### 📌 Etapa 4 — Evolução do Modelo (Feature Engineering)

Após a implementação inicial da rede neural, foi identificado que o modelo apresentava bom recall, porém com custo elevado devido ao número de falsos positivos.

Para melhorar a eficiência da estratégia de retenção, foi conduzido um novo experimento com **feature engineering orientado a comportamento do cliente**.

---

## 🔬 Feature Engineering

Foram criadas variáveis derivadas com base em hipóteses de negócio:

* `avg_charge_per_tenure`: relação entre valor pago e tempo de contrato  
* `is_month_to_month`: contratos mensais (maior risco de churn)  
* `has_fiber`: clientes com internet fibra  
* `has_tech_support` e `has_online_security`: proxies de engajamento  
* `is_new_customer` e `is_long_term_customer`: maturidade do cliente  
* `num_services`: número de serviços contratados  
* `charge_per_service`: custo médio por serviço  

Essas variáveis ajudam o modelo a capturar padrões que não são explicitamente representados nos dados originais.

---

## 🤖 Modelos Utilizados

| Modelo              | ROC-AUC | Observações                   |
| ------------------- | ------- | ----------------------------- |
| Regressão Logística | ~0.84   | Melhor performance geral      |
| MLP (PyTorch)       | ~0.83   | Melhor recall (captura churn) |
| Random Forest       | ~0.82   | Modelo intermediário          |
| Dummy               | 0.50    | Baseline                      |

| Modelo              | ROC-AUC | Recall | Precision | F1 | Valor Líquido | Custo Total |
|--------------------|--------|--------|-----------|-----|---------------|------------|
| Regressão Logística | ~0.84 | - | - | - | - | - |
| Random Forest       | ~0.82 | - | - | - | - | - |
| MLP (baseline)      | 0.833 | 0.782 | 0.505 | 0.613 | 27.408 | 35.123 |
| MLP (class weights) | 0.834 | 0.904 | 0.455 | 0.605 | 26.200 | 36.329 |
| **MLP (feature eng.)** | **0.850** | 0.689 | **0.581** | **0.631** | **29.202** | **33.329** |

---

## 🏆 Modelo Selecionado

Embora o modelo anterior apresentasse maior recall, o modelo com feature engineering demonstrou melhor desempenho global, principalmente em métricas de negócio.

Principais melhorias do MLP v2:

* Melhor ROC-AUC (melhor capacidade de ranking)
* Maior precisão (redução de falsos positivos)
* Menor custo operacional
* Maior valor líquido

Assim, o **MLP v2 foi escolhido como melhor candidato para produção**.

---

## 🧠 Insights Principais

* Feature engineering teve impacto direto na performance do modelo  
* O melhor modelo técnico não é necessariamente o melhor modelo de negócio  
* Redução de falsos positivos é fundamental para eficiência operacional  
* Métricas de negócio devem guiar a decisão final  

---

## ⚙️ Deploy e Versionamento

A API suporta múltiplas versões de modelo via variável de ambiente:

- MODEL_VERSION=v1
- MODEL_VERSION=v2

Isso permite:

* comparação entre modelos em produção  
* rollback seguro  
* evolução contínua do modelo  

---

## 🏗️ Arquitetura da Solução

A solução foi estruturada como uma aplicação de inferência em tempo real via API REST.

Fluxo de inferência:

```text
Cliente / Sistema externo
        ↓
FastAPI (/predict)
        ↓
Validação Pydantic
        ↓
Validação Pandera
        ↓
Feature Engineering
        ↓
Preprocessador sklearn
        ↓
Modelo MLP PyTorch
        ↓
Probabilidade de churn + decisão

A escolha por inferência em tempo real foi feita porque o caso de uso envolve identificar o risco de churn de um cliente individual no momento da consulta, permitindo integração futura com sistemas de CRM, atendimento ou campanhas de retenção.

Também seria possível usar inferência batch para campanhas periódicas, mas a API em tempo real oferece maior flexibilidade para integração operacional.

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Matsal-coder/tech-challenge-ml.git
cd tech-challenge-ml
```

---

### 2. Criar ambiente virtual

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```

---

### 3. Instalar dependências

```bash
pip install -e .
```

---

### 4. Rodar testes

```bash
pytest -v
```

---

### 5. Rodar API

```bash
uvicorn churn_model.api:app --reload
```

---

### 6. Acessar documentação

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 Exemplo de Requisição

```json
POST /predict

{
  "features": {
    "Gender": "Male",
    "Senior Citizen": "No",
    "Partner": "Yes",
    "Dependents": "No",
    "Tenure Months": 12,
    "Phone Service": "Yes",
    "Multiple Lines": "No",
    "Internet Service": "Fiber optic",
    "Online Security": "No",
    "Online Backup": "Yes",
    "Device Protection": "No",
    "Tech Support": "No",
    "Streaming TV": "Yes",
    "Streaming Movies": "Yes",
    "Contract": "Month-to-month",
    "Paperless Billing": "Yes",
    "Payment Method": "Electronic check",
    "Monthly Charges": 89.5,
    "Total Charges": 1074.0
  }
}
```

---

## 📤 Resposta

```json
{
  "churn_probability": 0.73,
  "prediction": 1,
  "threshold": 0.5
}
```

---

## 📊 Monitoramento (visão futura)

* Métricas técnicas:

  * ROC-AUC
  * Recall
  * F1-score
* Métricas de negócio:

  * Custo total
  * Valor líquido
* Drift de dados
* Latência da API

---

## ⚠️ Limitações

* Dados históricos podem não refletir comportamento futuro
* Não considera fatores externos (concorrência, mercado)
* Threshold depende de premissas de custo

---

## 🧾 Tecnologias

* Python
* Scikit-learn
* PyTorch
* MLflow
* FastAPI
* Pandera
* Pytest
* Ruff

---

## 📚 Documentação Complementar

Documentos adicionais do projeto:

| Documento | Descrição |
|-----------|------------|
| `MODEL_CARD.md` | Documentação técnica do modelo selecionado |
| `docs/deployment_architecture.md` | Arquitetura da solução e estratégia de deploy |
| `docs/monitoring_plan.md` | Estratégia de monitoramento técnico e operacional |

---

## 📌 Autor

Mateus Saldanha

---

