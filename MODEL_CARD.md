# 📄 Model Card — Churn Prediction (MLP v2)

## 📌 Visão Geral

Este modelo foi desenvolvido para prever a probabilidade de churn (cancelamento) de clientes em uma operadora de telecomunicações, com o objetivo de apoiar estratégias de retenção.

O modelo selecionado é uma **rede neural MLP (Multilayer Perceptron)** treinada com feature engineering orientado a comportamento do cliente.

---

## 🎯 Objetivo do Modelo

Identificar clientes com maior risco de churn para permitir ações proativas de retenção, equilibrando:

- Maximização de clientes retidos
- Minimização de custos com campanhas desnecessárias

---

## 🧠 Tipo de Modelo

- Arquitetura: MLP (PyTorch)
- Versão: **v2 (feature engineering)**

Estrutura da rede:
128 → 64 → 32 → 1

- Função de ativação: ReLU  
- Regularização: Dropout (0.3)  
- Loss: BCEWithLogitsLoss (com `pos_weight`)  
- Otimizador: Adam  
- Early Stopping baseado em validação  

---

## 🔬 Dados de Entrada

O modelo recebe dados estruturados de clientes contendo:

- Informações demográficas
- Informações de contrato
- Serviços contratados
- Valores de cobrança

### Exemplo de input

```json
{
  "Tenure Months": 12,
  "Monthly Charges": 89.5,
  "Total Charges": 1074.0,
  "Contract": "Month-to-month"
}
```

---

## ⚙️ Feature Engineering

O modelo utiliza variáveis derivadas com base em hipóteses de negócio:

- avg_charge_per_tenure
- is_month_to_month
- has_fiber
- has_tech_support
- has_online_security
- is_new_customer
- is_long_term_customer
- num_services
- charge_per_service

Essas variáveis ajudam a capturar padrões comportamentais não explícitos nos dados originais.

---


## 📊 Métricas de Performance

| Métrica           | Valor |
| ----------------- | ----- |
| ROC-AUC           | 0.850 |
| Recall (churn)    | 0.689 |
| Precision (churn) | 0.581 |
| F1-score          | 0.631 |

---

## 💰 Métricas de Negócio
| Métrica       | Valor  |
| ------------- | ------ |
| Valor líquido | 29.202 |
| Custo total   | 33.329 |

#### Interpretação
. O modelo reduz custos ao diminuir falsos positivos
. Mantém boa capacidade de identificar churn
. Maximiza o retorno financeiro da estratégia de retenção

---

## ⚖️ Trade-offs

| Aspecto       | Observação                     |
| ------------- | ------------------------------ |
| Recall        | Menor que modelo anterior      |
| Precision     | Maior (menos falsos positivos) |
| Custo         | Reduzido                       |
| Valor líquido | Aumentado                      |

---

## 🏆 Justificativa de Escolha

O modelo foi selecionado por apresentar o melhor equilíbrio entre métricas técnicas e métricas de negócio.

Embora modelos anteriores apresentassem maior recall, o MLP v2 apresentou:

- Melhor ROC-AUC
- Melhor F1-score
- Maior valor líquido
- Menor custo total

---

## ⚠️ Limitações

. Dependência de premissas de custo (custo_fp, custo_fn)
. Sensível a mudanças no comportamento dos clientes (data drift)
. Não incorpora fatores externos (concorrência, mercado)
. Pode sofrer degradação ao longo do tempo

---

## 📊 Monitoramento Recomendado

Métricas técnicas:
- ROC-AUC
- Recall churn
- F1-score
Métricas de negócio:
- Valor líquido
- Custo total
Operacional:
- Latência da API
- Taxa de erro

---

## 🔄 Versionamento

O modelo está integrado a uma API com suporte a múltiplas versões:
. MODEL_VERSION=v1
. MODEL_VERSION=v2

Isso permite:
- Comparação entre modelos
- Rollback seguro
- Evolução contínua

---

## 🚀 Uso em Produção

Fluxo de inferência:
→ Input bruto
→ Feature engineering
→ Preprocessamento
→ Modelo MLP v2
→ Probabilidade de churn
→ Aplicação de threshold
→ Decisão final

---

## 📌 Autor

Mateus Saldanha

---