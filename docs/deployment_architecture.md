# 🏗️ Arquitetura de Deploy — Churn Prediction API

## Objetivo

Este documento descreve a arquitetura escolhida para disponibilizar o modelo de previsão de churn em ambiente de inferência.

## Tipo de Deploy Escolhido

A solução foi estruturada como uma **API REST para inferência em tempo real**, utilizando FastAPI.

## Justificativa

A inferência em tempo real foi escolhida porque permite consultar o risco de churn de um cliente individual sob demanda, facilitando integração futura com:

- sistemas de CRM;
- plataformas de atendimento;
- campanhas de retenção;
- dashboards internos.

Esse formato é adequado quando a empresa deseja avaliar clientes individualmente no momento da interação ou antes de uma ação comercial.

## Alternativa: Inferência Batch

Uma arquitetura batch também seria possível para campanhas periódicas, por exemplo:

Base de clientes → pipeline batch → score de churn → lista para campanha

Essa abordagem seria útil para ações semanais ou mensais de retenção, mas oferece menor flexibilidade para integração em tempo real.

### Fluxo da API

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
Probabilidade de churn
        ↓
Aplicação de threshold
        ↓
Resposta da API

### Endpoints

GET /health : Verifica se a API está ativa e retorna a versão do modelo carregado.

POST /predict : Recebe os dados de um cliente e retorna:

- probabilidade de churn;
- classe prevista;
- threshold utilizado;
- versão do modelo.

### Versionamento de Modelo

A API suporta múltiplas versões por variável de ambiente:
* MODEL_VERSION=v1
* MODEL_VERSION=v2

Isso permite:

- rollback rápido;
- comparação entre versões;
- promoção controlada de novos modelos.

### Execução Local

No Git Bash/Linux/Mac:

```bash
MODEL_VERSION=v2 uvicorn churn_model.api:app --reload
```

### Possível Deploy em Nuvem

Como extensão opcional, a API poderia ser empacotada em Docker e disponibilizada em serviços como:

- AWS ECS / App Runner;
- Azure App Service;
- Google Cloud Run.

### Considerações Operacionais

Para uso em produção, recomenda-se:

- autenticação/autorização da API;
- monitoramento de latência e taxa de erro;
- logs centralizados;
- versionamento dos artefatos de modelo;
- plano de rollback;
- monitoramento de drift de dados.