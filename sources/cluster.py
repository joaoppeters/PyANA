# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Simulação de pontos de operação estocásticos
# np.random.seed(42)
# num_pontos = 1000
# dados = {
#     "Carga_Total": np.random.normal(1000, 200, num_pontos),  # MW
#     "Geracao_Eolica": np.random.normal(300, 100, num_pontos),  # MW
#     "Tensao_Minima": np.random.uniform(0.9, 1.05, num_pontos)  # pu
# }
# df = pd.DataFrame(dados)

# # Definir estratos com base na tensão mínima
# bins = [0.9, 0.95, 1.0, 1.05]  # Faixas de tensão mínima
# labels = ["Baixa", "Média", "Alta"]
# df["Estrato_Tensao"] = pd.cut(df["Tensao_Minima"], bins=bins, labels=labels, right=False)

# # Tamanho da amostra por estrato
# amostra_por_estrato = {
#     "Baixa": 30,
#     "Média": 50,
#     "Alta": 20
# }

# # Função de amostragem estratificada
# def amostragem_estratificada(df, coluna_estrato, amostra_por_estrato):
#     amostras = []
#     for estrato, tamanho in amostra_por_estrato.items():
#         estrato_df = df[df[coluna_estrato] == estrato]
#         amostra = estrato_df.sample(n=tamanho, random_state=42)  # Amostragem aleatória
#         amostras.append(amostra)
#     return pd.concat(amostras)

# # Realizar a amostragem
# amostra = amostragem_estratificada(df, "Estrato_Tensao", amostra_por_estrato)

# # Visualização Gráfica
# plt.figure(figsize=(12, 6))

# # Gráfico de dispersão dos dados originais
# plt.subplot(1, 2, 1)
# sns.scatterplot(
#     data=df, x="Carga_Total", y="Geracao_Eolica", hue="Estrato_Tensao", palette="viridis"
# )
# plt.title("Dados Originais")
# plt.xlabel("Carga Total (MW)")
# plt.ylabel("Geração Eólica (MW)")
# plt.legend(title="Estrato de Tensão")

# # Gráfico de dispersão da amostra estratificada
# plt.subplot(1, 2, 2)
# sns.scatterplot(
#     data=amostra, x="Carga_Total", y="Geracao_Eolica", hue="Estrato_Tensao", palette="viridis"
# )
# plt.title("Amostra Estratificada")
# plt.xlabel("Carga Total (MW)")
# plt.ylabel("Geração Eólica (MW)")
# plt.legend(title="Estrato de Tensão")

# plt.tight_layout()
# plt.show()



# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Simulate data for Carga_Total
# np.random.seed(42)
# num_pontos = 1000
# df = pd.DataFrame({
#     "Carga_Total": np.random.normal(1000, 200, num_pontos)  # MW
# })

# # Define strata based on Carga_Total
# bins = [600, 900, 1200, 1500]  # Define load ranges
# labels = ["Baixa", "Média", "Alta"]
# df["Estrato_Carga"] = pd.cut(df["Carga_Total"], bins=bins, labels=labels, right=False)

# # Define sample size per stratum
# amostra_por_estrato = {
#     "Baixa": 30,
#     "Média": 50,
#     "Alta": 20
# }

# # Perform stratified sampling
# def amostragem_estratificada(df, coluna_estrato, amostra_por_estrato):
#     amostras = []
#     for estrato, tamanho in amostra_por_estrato.items():
#         estrato_df = df[df[coluna_estrato] == estrato]
#         amostra = estrato_df.sample(n=tamanho, random_state=42)  # Random sampling
#         amostras.append(amostra)
#     return pd.concat(amostras)

# amostra = amostragem_estratificada(df, "Estrato_Carga", amostra_por_estrato)

# # Visualization
# plt.figure(figsize=(12, 6))

# # Histogram of original data
# plt.subplot(1, 2, 1)
# sns.histplot(data=df, x="Carga_Total", hue="Estrato_Carga", bins=30, palette="viridis", kde=True)
# plt.title("Distribuição Original de Carga Total")
# plt.xlabel("Carga Total (MW)")
# plt.ylabel("Frequência")

# # Histogram of sampled data
# plt.subplot(1, 2, 2)
# sns.histplot(data=amostra, x="Carga_Total", hue="Estrato_Carga", bins=30, palette="viridis", kde=True)
# plt.title("Amostra Estratificada de Carga Total")
# plt.xlabel("Carga Total (MW)")
# plt.ylabel("Frequência")

# plt.tight_layout()
# plt.show()


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = os.getcwd() + "\\sistemas\\EXLF\\BALANCE\\EXLF_2Q2024_R2_C1_loadstd10_geolstd10.txt"

# Replace with your full dataset
df = pd.read_csv(data, sep=";", header=0)

# Pre-define bins
mean = df["dATIVA"].mean()
stddev = df["dATIVA"].std()
bins = [mean - 2 * stddev, mean - stddev, mean, mean + stddev, mean + 2 * stddev]
bins = [mean - 3 * stddev, mean - stddev, mean + stddev, mean + 3 * stddev]

# Define strata based on dATIVA
# bins = [91000, 94000, 97000, 100000]  # Define meaningful ranges for dATIVA
labels = ["Low", "Medium", "High"]
df["Strata"] = pd.cut(df["dATIVA"], bins=bins, labels=labels, right=False)

# Perform stratified sampling
sample_size_per_stratum = {"Low": 2, "Medium": 2, "High": 1}

def stratified_sampling(df, strata_col, sample_sizes):
    samples = []
    for stratum, size in sample_sizes.items():
        stratum_df = df[df[strata_col] == stratum]
        sample = stratum_df.sample(n=size, random_state=42)  # Random sampling
        samples.append(sample)
    return pd.concat(samples)

sampled_df = stratified_sampling(df, "Strata", sample_size_per_stratum)

# Visualization
plt.figure(figsize=(12, 6))

# Original data histogram
plt.subplot(1, 2, 1)
sns.histplot(data=df, x="dATIVA", hue="Strata", bins=10, palette="Set2", kde=True)
plt.title("Original Data Distribution (dATIVA)")
plt.xlabel("dATIVA")
plt.ylabel("Frequency")

# Sampled data histogram
plt.subplot(1, 2, 2)
sns.histplot(data=sampled_df, x="dATIVA", hue="Strata", bins=10, palette="Set2", kde=True)
plt.title("Sampled Data Distribution (dATIVA)")
plt.xlabel("dATIVA")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()


def cxlf(
    powerflow,
):
    """
    
    Args:
        powerflow (_type_): Description
    """
    ## Inicialização
    

def cxic(
    powerflow,
):
    """
    
    Args:
        powerflow (_type_): Description
    """
    ## Inicialização
    pass

def cxct(
    powerflow,
):
    """
    
    Args:
        powerflow (_type_): Description
    """
    ## Inicialização
    pass