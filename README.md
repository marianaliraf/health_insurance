# 🏥 Health Insurance Propensity Score Prediction

Este projeto tem como objetivo prever a probabilidade (propensity score) de um cliente adquirir um seguro de saúde, utilizando aprendizado de máquina com base nos dados disponibilizados pelo [Kaggle - Health Insurance Cross Sell Prediction](https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction).


---

## Estrutura do Projeto

### `projeto health insurance/`
Contém as etapas de desenvolvimento e experimentação do modelo:

- `datasets/`: arquivos de entrada, como `train.csv`.
- `notebook/`: desenvolvimento do modelo em Jupyter Notebook.
- `model/`: modelo treinado e serializado (`.pkl`).
- `api/`: versão inicial da API.

### `health_insurance-api/`
Contém a API Flask implantada no Heroku.

- `health_insurance/`: código com a lógica de predição.
- `model/`: modelo `.pkl` carregado pela API.
- `parameter/`: parâmetros de transformação de dados.
- `handler.py`: endpoint principal da API.
- `Procfile`, `requirements.txt`, `runtime.txt`: arquivos de configuração para deploy no Heroku.

---

## API em Produção

A API foi implantada no Heroku e está disponível em:  

### Endpoint `/predict`

**Método:** `POST`  
**Content-Type:** `application/json`  
**Body (exemplo):**
```json
{
  "id": 1,
  "Gender": "Male",
  "Age": 45,
  "Driving_License": 1,
  "Region_Code": 28.0,
  "Previously_Insured": 0,
  "Vehicle_Age": "< 1 Year",
  "Vehicle_Damage": "Yes",
  "Annual_Premium": 30000.0,
  "Policy_Sales_Channel": 152.0,
  "Vintage": 120
}
```

**Retorno:**
```json
[{"score": 0.7635}]
```

---

## Integração com Google Sheets

Criou-se uma integração com o Google Sheets para consumo da API via `Google Apps Script`.

- A planilha possui os dados dos clientes.
- Um botão executa o script `PredictAll()`, que envia as informações à API e escreve os `Propensity_Score` na última coluna.
-  Health_Insurance.gs

---

## Tecnologias Utilizadas

- Python 3.8
- Flask
- Scikit-learn
- Heroku (deploy)
- Google Apps Script (integração com Sheets)

<img width="1003" height="464" alt="image" src="https://github.com/user-attachments/assets/a5a2316e-b47a-404c-869e-f6caafa50ecb" />

---

## Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/health_insurance.git
   cd health_insurance/health_insurance-api
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

3. Rode a API:
   ```bash
   python handler.py
   ```

---

## Autora

Desenvolvido por [@marianaliraf](https://github.com/marianaliraf)

**Este projeto foi desenvolvido exclusivamente para fins educacionais.**
