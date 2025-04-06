# 🎓 Previsão de Notas do ENEM com KNN

Este projeto utiliza dados públicos do ENEM para prever as notas de um(a) candidato(a) com base em suas características socioeconômicas, usando o algoritmo K-Nearest Neighbors (KNN).

---

## 🗂 Fonte dos Dados

Os dados utilizados neste projeto foram extraídos da base oficial do INEP:

🔗 [Microdados ENEM - Dados Abertos do Governo Federal](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)

---

## ⚙️ Etapas de Desenvolvimento

### 1. **Coleta e Tratamento dos Dados**

O script `adjustData.py` realiza:

- Leitura e limpeza dos microdados brutos;
- Filtro para manter apenas os participantes válidos e completos;
- Seleção das variáveis mais relevantes (    'TP_COR_RACA',
    'TP_ESCOLA',
    'SG_UF_PROVA',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT',
    'NU_NOTA_REDACAO',
    'Q002',
    'Q006')
- Criação do arquivo `dados_filtrados.csv` contendo os dados prontos para o treinamento.

### 2. **Treinamento do Modelo**

O script `trainModel.py` realiza:

- Leitura do arquivo `dados_filtrados.csv`;
- Aplicação de codificação categórica e normalização dos dados;
- Treinamento do algoritmo KNN com validação;
- Salvamento dos arquivos:

  - `modelo_knn.pkl`: modelo KNN treinado;
  - `scaler.pkl`: transformador de normalização;
  - `colunas_modelo.pkl`: colunas esperadas pelo modelo.

---

## 🤖 Justificativa do Modelo

O algoritmo **K-Nearest Neighbors (KNN)** foi escolhido por sua capacidade de prever resultados com base na similaridade entre amostras. A ideia central é:

> “Candidatos(as) com características socioeconômicas semelhantes tendem a ter desempenhos semelhantes no ENEM.”

O modelo analisa os **k candidatos mais próximos** (por padrão, `k=5`) e utiliza suas notas como base para prever as do novo aluno.

Além das notas previstas, a aplicação compara os resultados do(a) candidato(a) com seus vizinhos mais próximos, informando se suas notas estão entre as **maiores**, **menores** ou **médias** dentro do grupo.

---

## 🖥 Como Executar

### 1. Instale as dependências

```bash
pip install pandas scikit-learn streamlit joblib numpy
```

### 2. Prepare os dados

Certifique-se de que o arquivo original do INEP (`MICRODADOS_ENEM_****.csv`) esteja na pasta do projeto. - Escolha o ano do ENEM que deseja analisar

Execute:

```bash
python adjustData.py
```

Isso criará o arquivo `dados_filtrados.csv`.

### 3. Treine o modelo

```bash
python trainModel.py
```

Isso criará os arquivos:

- `modelo_knn.pkl`
- `scaler.pkl`
- `colunas_modelo.pkl`

### 4. Inicie a interface

```bash
streamlit run app.py
```

---

## 📈 Interface

A aplicação oferece uma interface intuitiva feita com Streamlit, onde é possível:

- Inserir as características do(a) aluno(a);
- Visualizar as **notas previstas** para cada área do ENEM;
- Ver como essas notas se comparam com os vizinhos identificados.

---

## 🧠 Exemplo de Previsão

> “Sua nota em Matemática foi a **menor** entre os vizinhos.”  
> “Sua nota em Redação foi a **maior** entre os vizinhos.”  

Essas comparações ajudam a entender o desempenho previsto dentro de um contexto social semelhante.

---
