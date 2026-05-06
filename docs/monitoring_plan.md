# 📊 Plano de Monitoramento — Churn Prediction API

## Objetivo

Este documento descreve o plano de monitoramento proposto para a API de previsão de churn em ambiente de produção.

O objetivo do monitoramento é garantir:

- qualidade das previsões;
- estabilidade operacional;
- identificação precoce de degradação do modelo;
- suporte a ações corretivas.

---

## 🔬 Métricas Técnicas

As seguintes métricas devem ser acompanhadas continuamente:

| Métrica | Objetivo |
|--------|----------|
| ROC-AUC | Avaliar capacidade discriminatória do modelo |
| Recall (churn) | Garantir captura de clientes propensos a churn |
| Precision | Controlar falsos positivos |
| F1-score | Equilibrar precision e recall |

---

## 💰 Métricas de Negócio

| Métrica | Objetivo |
|--------|----------|
| Valor líquido | Maximizar retorno financeiro |
| Custo total | Controlar custos operacionais |
| Taxa de retenção | Avaliar impacto da estratégia |

---

## ⚙️ Métricas Operacionais

| Métrica | Objetivo |
|--------|----------|
| Latência da API | Garantir tempo de resposta adequado |
| Taxa de erro | Detectar falhas na aplicação |
| Disponibilidade | Garantir uptime da API |

---

## 📉 Monitoramento de Drift

O comportamento dos clientes pode mudar ao longo do tempo, reduzindo a qualidade do modelo.

Por isso, recomenda-se monitorar:

### Drift de Features

Mudanças na distribuição de variáveis como:

- Monthly Charges
- Tenure Months
- Contract
- Internet Service

### Drift de Predição

Mudanças na distribuição das probabilidades previstas pelo modelo.

Exemplo:

```text
Treino:
média churn_probability = 0.32

Produção:
média churn_probability = 0.58
```

Isso pode indicar degradação do modelo.

---

## 🚨 Alertas Recomendados

| Evento | Ação |
|--------|------|
| Queda relevante de ROC-AUC | Revisar modelo |
| Aumento forte de latência | Investigar infraestrutura |
| Crescimento de erros HTTP | Verificar aplicação |
| Drift elevado | Reavaliar treinamento |

---

## 🛠️ Playbook de Resposta

### Cenário 1 — Queda de performance

Possíveis ações:

- revisar dados recentes;
- recalibrar threshold;
- retreinar modelo;
- promover nova versão.

---

### Cenário 2 — Drift de dados

Possíveis ações:

- comparar distribuição treino vs produção;
- revisar feature engineering;
- criar pipeline de retreinamento.

---

### Cenário 3 — Problemas operacionais

Possíveis ações:

- rollback para modelo anterior;
- reinício da aplicação;
- investigação de logs;
- escalonamento da infraestrutura.

---

## 🔄 Estratégia de Versionamento

A API suporta múltiplas versões de modelo:

```bash
MODEL_VERSION=v1
MODEL_VERSION=v2
```

Isso permite:

- rollback rápido;
- testes controlados;
- comparação entre modelos.

---

## 🚀 Evoluções Futuras

Possíveis melhorias futuras:

- monitoramento automatizado;
- dashboards com Grafana/Prometheus;
- alertas automáticos;
- pipeline de retreinamento;
- deploy em nuvem;
- CI/CD para promoção automática de modelos.

---

## 📌 Conclusão

O monitoramento é essencial para garantir que o modelo continue gerando valor ao negócio após o deploy.

Além das métricas técnicas, o acompanhamento de métricas operacionais e financeiras é fundamental para avaliar o impacto real da solução.