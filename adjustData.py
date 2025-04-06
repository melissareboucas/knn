import pandas as pd

# Caminho do CSV original
caminho_arquivo = 'MICRODADOS_ENEM_2023.csv'

# Lista das colunas que você quer manter (remover município pois atrapalha o treinamento e não tem tanta relevância)
colunas_desejadas = [
    'TP_COR_RACA',
    'TP_ESCOLA',
    'SG_UF_PROVA',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT',
    'NU_NOTA_REDACAO',
    'Q002',
    'Q006'
]

# Lê apenas as colunas desejadas, com encoding e separador corretos
print("Lendo e filtrando colunas do arquivo original...")
df = pd.read_csv(
    caminho_arquivo,
    sep=';',
    encoding='latin1',
    usecols=colunas_desejadas
)

# Remove todas as linhas com pelo menos 1 valor ausente
print("Removendo linhas com valores ausentes...")
df_limpo = df.dropna()

# Salva o resultado final
df_limpo.to_csv('dados_filtrados.csv', index=False)
