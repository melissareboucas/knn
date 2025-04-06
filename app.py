import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Carregando os arquivos salvos
knn = joblib.load("modelo_knn.pkl")
scaler = joblib.load("scaler.pkl")
colunas_modelo = joblib.load("colunas_modelo.pkl")

# Mapas para exibição e valores reais
mapa_cor_raca = {
    "Não declarado": 0,
    "Branca": 1,
    "Preta": 2,
    "Parda": 3,
    "Amarela": 4,
    "Indígena": 5,
    "Não dispõe da informação": 6
}

mapa_tp_escola = {
    "Não respondeu": 1,
    "Pública": 2,
    "Privada": 3
}

mapa_q002 = {
    "Nunca estudou": "A",
    "Não completou a 4ª série/5º ano do EF": "B",
    "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do EF": "C",
    "Completou a 8ª série/9º ano do EF, mas não completou o EM": "D",
    "Completou o EM, mas não completou a Faculdade": "E",
    "Completou a Faculdade, mas não completou a Pós-graduação": "F",
    "Completou a Pós-graduação": "G",
    "Não sei": "H"
}

mapa_q006 = {
    "Nenhuma Renda": "A",
    "Até R$ 1.320,00": "B",
    "De R$ 1.320,01 até R$ 1.980,00": "C",
    "De R$ 1.980,01 até R$ 2.640,00": "D",
    "De R$ 2.640,01 até R$ 3.300,00": "E",
    "De R$ 3.300,01 até R$ 3.960,00": "F",
    "De R$ 3.960,01 até R$ 5.280,00": "G",
    "De R$ 5.280,01 até R$ 6.600,00": "H",
    "De R$ 6.600,01 até R$ 7.920,00": "I",
    "De R$ 7.920,01 até R$ 9.240,00": "J",
    "De R$ 9.240,01 até R$ 10.560,00": "K",
    "De R$ 10.560,01 até R$ 11.880,00": "L",
    "De R$ 11.880,01 até R$ 13.200,00": "M",
    "De R$ 13.200,01 até R$ 15.840,00": "N",
    "De R$ 15.840,01 até R$19.800,00": "O",
    "De R$ 19.800,01 até R$ 26.400,00": "P",
    "Acima de R$ 26.400,00": "Q"
}

# Título e descrição
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎯 Previsão de Notas do ENEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Insira os dados de um(a) aluno(a) para prever suas notas nas áreas do conhecimento com base em dados reais do ENEM 2023.</p>", unsafe_allow_html=True)
st.markdown("---")

# Formulário com campos amigáveis
cor_raca_legivel = st.selectbox("Cor/Raça", list(mapa_cor_raca.keys()))
tipo_escola = st.selectbox("Tipo de Escola", list(mapa_tp_escola.keys()))
uf_prova = st.selectbox("UF da Prova", [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
])
q002 = st.selectbox("Escolaridade do Responsável", list(mapa_q002.keys()))
q006 = st.selectbox("Renda Familiar", list(mapa_q006.keys()))

# Botão para previsão
if st.button("📊 Prever Notas"):
    # Traduz o valor escolhido pelo usuário para o código numérico
    cor_raca = mapa_cor_raca[cor_raca_legivel]

    # Criar DataFrame com os dados inseridos
    novo_aluno = pd.DataFrame([{
        'TP_COR_RACA': cor_raca,
        'TP_ESCOLA': mapa_tp_escola[tipo_escola],
        'SG_UF_PROVA': uf_prova,
        'Q002': mapa_q002[q002],
        'Q006': mapa_q006[q006]
    }])

    # Pré-processamento
    novo_aluno_encoded = pd.get_dummies(novo_aluno)
    novo_aluno_encoded = novo_aluno_encoded.reindex(columns=colunas_modelo, fill_value=0)
    novo_aluno_normalized = scaler.transform(novo_aluno_encoded)

    # Previsão
    notas_previstas = knn.predict(novo_aluno_normalized)

    # Obtem os índices dos vizinhos mais próximos
    distances, indices = knn.kneighbors(novo_aluno_normalized)
    # Obtemos os dados de saída usados no treinamento do modelo
    y_train = pd.DataFrame(knn._y, columns=['CN', 'CH', 'LC', 'MT', 'Redacao'])
    notas_vizinhos = y_train.iloc[indices[0]]

    st.markdown("---")
    st.success("✅ Previsão realizada com sucesso!")

    st.subheader("📈 Notas Previstas:")

    col_nomes = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens', 'Matemática', 'Redação']
    for i, area in enumerate(col_nomes):
        nota_prevista = notas_previstas[0][i]
        notas_vizinhos_disciplina = notas_vizinhos.iloc[:, i]

        menor = sum(nota_prevista < notas_vizinhos_disciplina)
        igual = sum(nota_prevista == notas_vizinhos_disciplina)
        maior = sum(nota_prevista > notas_vizinhos_disciplina)

        if maior > menor and maior > igual:
            comparativo = "acima da maioria dos vizinhos"
        elif menor > maior and menor > igual:
            comparativo = "abaixo da maioria dos vizinhos"
        elif igual >= maior and igual >= menor:
            comparativo = "igual à maioria dos vizinhos"
        else:
            comparativo = "sem diferença significativa em relação aos vizinhos"

        emoji = "🧪" if "Natureza" in area else "📜" if "Humanas" in area else "📝" if "Redação" in area else "🔢" if "Matemática" in area else "📚"
        st.markdown(f"{emoji} **{area}**: `{nota_prevista:.1f}` — {comparativo}")
