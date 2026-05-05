# 📊 Tech Challenge — Previsão de Churn com Pipeline End-to-End

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um sistema completo de Machine Learning para previsão de churn (cancelamento de clientes) em uma operadora de telecomunicações.

A solução foi construída de ponta a ponta, incluindo:

* Análise exploratória dos dados (EDA)
* Modelagem com algoritmos tradicionais e redes neurais
* Comparação de modelos com métricas técnicas e de negócio
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

  * Falso positivo → custo de campanha
  * Falso negativo → perda de receita
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

---

## 🤖 Modelos Utilizados

| Modelo              | ROC-AUC | Observações                   |
| ------------------- | ------- | ----------------------------- |
| Regressão Logística | ~0.84   | Melhor performance geral      |
| MLP (PyTorch)       | ~0.83   | Melhor recall (captura churn) |
| Random Forest       | ~0.82   | Modelo intermediário          |
| Dummy               | 0.50    | Baseline                      |

### 💡 Insight

O melhor modelo técnico (AUC) não necessariamente é o melhor modelo de negócio.

A MLP apresentou melhor capacidade de identificar churn, sendo mais adequada para estratégias de retenção.

---

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

## 📌 Autor

Mateus Saldanha

---

## 🎥 Entrega

* Repositório GitHub ✔
* API funcional ✔
* Pipeline completo ✔
* (Em andamento) Vídeo STAR

---
