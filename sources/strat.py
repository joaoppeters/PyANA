# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def strat(
):
    """
    
    Args
        powerflow:
    """
    import pandas as pd
    import numpy as np

    # Criando um DataFrame fictício
    data = {
        "ID": range(1, 10001),
        "Idade": np.random.randint(18, 70, size=10000),
        "Renda": np.random.randint(2000, 10000, size=10000)
    }
    df = pd.DataFrame(data)
    print(df.head())

    # Criando os estratos com base na faixa etária
    bins = [18, 30, 50, 70]  # Faixas de idade
    labels = ["18-30", "31-50", "51-70"]
    df["Faixa_Etaria"] = pd.cut(df["Idade"], bins=bins, labels=labels, right=False)

    # Tamanho da amostra desejada por estrato
    amostra_por_estrato = {
        "18-30": 5,
        "31-50": 7,
        "51-70": 3
    }

    # Função para realizar a amostragem estratificada
    def amostragem_estratificada(df, coluna_estrato, amostra_por_estrato):
        amostras = []
        for estrato, tamanho in amostra_por_estrato.items():
            estrato_df = df[df[coluna_estrato] == estrato]
            amostra = estrato_df.sample(n=tamanho, random_state=42)  # Amostragem aleatória
            amostras.append(amostra)
        return pd.concat(amostras)

    # Realizando a amostragem estratificada
    amostra = amostragem_estratificada(df, "Faixa_Etaria", amostra_por_estrato)

    # Exibindo os resultados
    print("Amostra Estratificada:")
    print(amostra)


def get_mean_stddev(
    filename: str,
):
    """
    Get mean and standard deviation from a file.

    Args:
        filename (str): The name of the file.

    Returns:
        tuple: A tuple containing the mean and standard deviation.
    """
    ## Inicialização
    with open(filename, "r") as file:
        data = file.readlines()
    
    load = [float(value.split(";")[3]) for value in data[1:]]
    min_value = min(load)
    max_value = max(load)
    mean = (min_value + max_value) / 2
    std_dev = (max_value - min_value) / 6  # Assuming a range of 4 standard deviations

    print(mean, std_dev/mean*100)

    return mean, std_dev

    # import numpy as np
    # import matplotlib.pyplot as plt
    # from scipy.stats import norm

    # # Generate random data from the estimated normal distribution
    # data = np.random.normal(loc=mean, scale=std_dev, size=1000)

    # # Plot the histogram of the generated data
    # plt.hist(data, bins=100, density=True, alpha=0.6, color='g')

    # # Plot the probability density function (PDF) of the normal distribution
    # x = np.linspace(min_value, max_value, 100)
    # plt.plot(x, norm.pdf(x, mean, std_dev), 'r', label='Normal PDF')

    # # Add labels and title
    # plt.xlabel('Value')
    # plt.ylabel('Probability Density')
    # plt.title('Estimated Normal Distribution from Min and Max')
    # plt.legend()

    # plt.show()

strat()