import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
import joblib

# Carrega os dados
df = pd.read_csv("dados_filtrados.csv")

# Separar as colunas de entrada de dados e de saída de dados
X = df[['TP_COR_RACA', 'TP_ESCOLA', 'SG_UF_PROVA', 'Q002', 'Q006']] 
y = df[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']]

# Transformar valores categóricos em binários
X_transformed = pd.get_dummies(X)

# Normalizando as colunas para que tenham o mesmo peso independente da variação de valores
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X_transformed)

# Separando a base em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

# Aplicando treinamento considerando os 5 vizinhos mais próximos
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)

# === Salva modelo, scaler e colunas ===
joblib.dump(knn, "modelo_knn.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(X_transformed.columns.tolist(), "colunas_modelo.pkl")

print("Modelo, scaler e colunas salvos com sucesso!")
