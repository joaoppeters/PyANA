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


# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the dataset
# data = os.getcwd() + "\\sistemas\\EXLF\\RTOT\\EXLF_2Q2024_R2_C1_loadstd10_geolstd10.txt"

# # Replace with your full dataset
# df = pd.read_csv(data, sep=";", header=0)

# # Pre-define bins
# mean = df["dATIVA"].mean()
# stddev = df["dATIVA"].std()
# bins = [mean - 2 * stddev, mean - stddev, mean, mean + stddev, mean + 2 * stddev]
# bins = [mean - 3 * stddev, mean - stddev, mean + stddev, mean + 3 * stddev]

# # Define strata based on dATIVA
# # bins = [91000, 94000, 97000, 100000]  # Define meaningful ranges for dATIVA
# labels = ["Low", "Medium", "High"]
# df["Strata"] = pd.cut(df["dATIVA"], bins=bins, labels=labels, right=False)

# # Perform stratified sampling
# sample_size_per_stratum = {"Low": 2, "Medium": 2, "High": 1}

# def stratified_sampling(df, strata_col, sample_sizes):
#     samples = []
#     for stratum, size in sample_sizes.items():
#         stratum_df = df[df[strata_col] == stratum]
#         sample = stratum_df.sample(n=size, random_state=42)  # Random sampling
#         samples.append(sample)
#     return pd.concat(samples)

# sampled_df = stratified_sampling(df, "Strata", sample_size_per_stratum)

# # Visualization
# plt.figure(figsize=(12, 6))

# # Original data histogram
# plt.subplot(1, 2, 1)
# sns.histplot(data=df, x="dATIVA", hue="Strata", bins=10, palette="Set2", kde=True)
# plt.title("Original Data Distribution (dATIVA)")
# plt.xlabel("dATIVA")
# plt.ylabel("Frequency")

# # Sampled data histogram
# plt.subplot(1, 2, 2)
# sns.histplot(data=sampled_df, x="dATIVA", hue="Strata", bins=10, palette="Set2", kde=True)
# plt.title("Sampled Data Distribution (dATIVA)")
# plt.xlabel("dATIVA")
# plt.ylabel("Frequency")

# plt.tight_layout()
# plt.show()


def cxlf(
    powerflow,
):
    """

    Args:
        powerflow (_type_): Description
    """

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from os import listdir
    from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
    import seaborn as sns
    from sklearn.cluster import AffinityPropagation, KMeans, DBSCAN, MeanShift
    from sklearn.metrics import silhouette_score
    from sklearn.mixture import GaussianMixture
    from sklearn.preprocessing import StandardScaler
    from yellowbrick.cluster import KElbowVisualizer

    ## Inicialização
    file = powerflow.maindir + "\\sistemas\\EXLF\\EXLF_" + powerflow.name + ".REL"
    linecount = 0
    rf = open(f"{file}", "r", encoding="utf-8", errors="ignore")
    rflines = rf.readlines()
    rf.close()
    flag = True
    while flag:
        linecount += 1
        if rflines[linecount] == " RELATORIO DE TOTAIS DE AREA\n":
            while linecount < len(rflines):
                linecount += 1
                try:
                    if rflines[linecount].split()[0] == "TOTAL":
                        basecase = [
                            float(rflines[linecount].split()[1]),
                            float(rflines[linecount + 1].split()[0]),
                            float(rflines[linecount].split()[3]),
                            float(rflines[linecount + 1].split()[2]),
                        ]
                        flag = False
                        break
                except:
                    pass

    folder_path = powerflow.maindir + "\\sistemas\\EXLF\\RTOT\\"
    files = [
        f
        for f in listdir(folder_path)
        if f.startswith("EXLF_" + powerflow.name + "_") and f.endswith(".txt")
    ]

    data = pd.concat(
        [pd.read_csv(folder_path + file, delimiter=";", header=0) for file in files],
        ignore_index=True,
    )
    data["x"] = data["pATIVA"] - data["dATIVA"]
    data["y"] = data["pREATIVA"] - data["dREATIVA"]

    # figure(num=1, figsize=(10, 8))
    # scatter(basecase[0]-basecase[2], basecase[1]-basecase[3], marker="d", color="black", s=35, zorder=2)
    # scatter(data["x"].to_list(), data["y"].to_list(), marker="o", s=10,)
    # legend()
    # xlabel("ΔP (MW)")
    # ylabel("ΔQ (MVAr)")
    # show()

    df = data[["x", "y"]]

    # ====== 1. PLOTAR PONTOS ORIGINAIS ======
    plt.figure(figsize=(6, 5))
    plt.scatter(
        basecase[0] - basecase[2],
        basecase[1] - basecase[3],
        marker="d",
        color="black",
        s=35,
        zorder=2,
    )
    plt.scatter(df["x"], df["y"], s=50, color="gray", alpha=0.7)
    plt.title("Pontos Originais (Antes do Clustering)")
    plt.xlabel("ΔP (MW)")
    plt.ylabel("ΔQ (MVAr)")

    # Normalizar os dados
    scaler = StandardScaler()
    X = scaler.fit_transform(df)

    # Criar um DataFrame para armazenar os resultados
    df_clusters = df.copy()

    # ====== 2. DEFINIR O NÚMERO ÓTIMO DE CLUSTERS PARA K-MEANS ======
    fig, ax = plt.subplots(figsize=(6, 4))
    kmeans_model = KMeans(random_state=42)
    visualizer = KElbowVisualizer(kmeans_model, k=(1, 10), metric="distortion", ax=ax)
    visualizer.fit(X)

    # Número ótimo de clusters
    optimal_k = visualizer.elbow_value_

    # ====== 3. K-MEANS ======
    for nclstr in range(2, 10):
        kmeans = KMeans(n_clusters=nclstr, random_state=42)
        df_clusters["KMeans"] = kmeans.fit_predict(X)

        # # ====== 4. DBSCAN (automático, baseado na densidade) ======
        # dbscan = DBSCAN(eps=0.5, min_samples=5)
        # df_clusters['DBSCAN'] = dbscan.fit_predict(X)

        # # ====== 5. HIERARCHICAL CLUSTERING ======
        # linked = linkage(X, method='ward')

        # # Determinar o número ideal de clusters pela Silhueta
        # best_k_hierarchical = max(range(2, 10), key=lambda k: silhouette_score(X, fcluster(linked, k, criterion='maxclust')))
        # df_clusters['Hierarchical'] = fcluster(linked, best_k_hierarchical, criterion='maxclust')

        # # Plotando o dendrograma
        # plt.figure(figsize=(8, 5))
        # dendrogram(linked)
        # plt.title("Dendrograma - Hierarchical Clustering")

        # # ====== 6. MEAN SHIFT ======
        # meanshift = MeanShift()
        # df_clusters['MeanShift'] = meanshift.fit_predict(X)

        # # ====== 7. GAUSSIAN MIXTURE MODEL (GMM) ======
        # # Definir o número ideal de clusters pela Silhueta
        # best_k_gmm = max(range(2, 10), key=lambda k: silhouette_score(X, GaussianMixture(n_components=k, random_state=42).fit_predict(X)))
        # gmm = GaussianMixture(n_components=best_k_gmm, random_state=42)
        # df_clusters['GMM'] = gmm.fit_predict(X)

        # # ====== 8. AFFINITY PROPAGATION ======
        # affinity_propagation = AffinityPropagation(damping=0.7, preference=-150)
        # df_clusters['AffinityPropagation'] = affinity_propagation.fit_predict(X)
        # num_clusters_ap = len(np.unique(df_clusters['AffinityPropagation']))  # Número de clusters gerados

        # ====== 8. FUNÇÃO PARA PLOTAR OS CLUSTERS ======
        def plot_clusters(method, labels):
            """Gera gráficos de dispersão para visualizar os clusters."""
            plt.figure(figsize=(6, 5))
            sns.scatterplot(x=df["x"], y=df["y"], hue=labels, palette="tab10", s=50)
            plt.scatter(
                basecase[0] - basecase[2],
                basecase[1] - basecase[3],
                marker="d",
                color="black",
                s=35,
                zorder=2,
            )
            plt.title(f"{method} Clustering")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.legend(title="Cluster")

        # Criando gráficos para cada método
        plot_clusters("K-Means", df_clusters["KMeans"])
    # plot_clusters("DBSCAN", df_clusters['DBSCAN'])
    # plot_clusters("Hierarchical", df_clusters['Hierarchical'])
    # plot_clusters("Mean Shift", df_clusters['MeanShift'])
    # plot_clusters("GMM", df_clusters['GMM'])
    # plot_clusters("Affinity Propagation", df_clusters['AffinityPropagation'])

    plt.show()


def cxic(
    powerflow,
):
    """

    Args:
        powerflow (_type_): Description
    """

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from os.path import exists
    from os import listdir, mkdir
    import seaborn as sns
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from yellowbrick.cluster import KElbowVisualizer

    from ulog import usxic

    ## Inicialização
    file = powerflow.maindir + "\\sistemas\\EXLF\\SXLF_" + powerflow.name + ".REL"
    linecount = 0
    rf = open(f"{file}", "r", encoding="utf-8", errors="ignore")
    rflines = rf.readlines()
    rf.close()
    flag = True
    while flag:
        linecount += 1
        if rflines[linecount] == " RELATORIO DE TOTAIS DE AREA\n":
            while linecount < len(rflines):
                linecount += 1
                try:
                    if rflines[linecount].split()[0] == "TOTAL":
                        basecase = [
                            float(rflines[linecount].split()[1]),
                            float(rflines[linecount + 1].split()[0]),
                            float(rflines[linecount].split()[3]),
                            float(rflines[linecount + 1].split()[2]),
                        ]
                        flag = False
                        break
                except:
                    pass

    folder_path = powerflow.maindir + "\\sistemas\\EXLF\\RTOT\\"
    files = [
        f
        for f in listdir(folder_path)
        if f.startswith("EXLF_" + powerflow.name + "_") and f.endswith(".txt")
    ]

    data = pd.concat(
        [
            pd.read_csv(folder_path + file, delimiter=";", header=0).assign(
                filename=file
            )
            for file in files
        ],
        ignore_index=True,
    )
    data["x"] = data["pATIVA"] - data["dATIVA"]
    data["y"] = data["pREATIVA"] - data["dREATIVA"]
    df = data[
        [
            "x",
            "y",
            "filename",
        ]
    ]

    # ====== 1. PLOTAR PONTOS ORIGINAIS ======
    plt.figure(figsize=(6, 5))
    plt.scatter(
        basecase[0] - basecase[2],
        basecase[1] - basecase[3],
        marker="d",
        color="black",
        s=35,
        zorder=2,
    )
    plt.scatter(df["x"], df["y"], s=50, color="gray", alpha=0.7)
    plt.title("Pontos Originais (Antes do Clustering)")
    plt.xlabel("ΔP (MW)")
    plt.ylabel("ΔQ (MVAr)")

    # Normalizar os dados
    scaler = StandardScaler()
    X = scaler.fit_transform(df[["x", "y"]])

    # Criar um DataFrame para armazenar os resultados
    df_clusters = df.copy()

    # Definir o número ótimo de clusters
    fig, ax = plt.subplots(figsize=(6, 4))
    kmeans_model = KMeans(random_state=42)
    visualizer = KElbowVisualizer(kmeans_model, k=(1, 10), metric="distortion", ax=ax)
    visualizer.fit(X)
    # visualizer.show()

    # Número ótimo de clusters
    optimal_k = visualizer.elbow_value_

    # Aplicar K-Means
    pf_kmeans = KMeans(
        n_clusters=7,
        random_state=42,
    )
    df_clusters["KMeans"] = pf_kmeans.fit_predict(X)
    pf_centroids = pf_kmeans.cluster_centers_
    for i in range(0, 7):
        print(df_clusters[df_clusters.KMeans == i].shape)

    # ====== 8. FUNÇÃO PARA PLOTAR OS CLUSTERS ======
    def plot_clusters(method, labels):
        """Gera gráficos de dispersão para visualizar os clusters."""
        plt.figure(figsize=(6, 5))
        sns.scatterplot(x=df["x"], y=df["y"], hue=labels, palette="tab10", s=50)
        plt.title(f"{method} Clustering")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend(title="Cluster")

    # Criando gráficos para cada método
    plot_clusters("K-Means", df_clusters["KMeans"])
    plt.show()

    # === 1. DESNORMALIZAR OS CENTRÓIDES ===
    centroids_original_scale = scaler.inverse_transform(pf_centroids)

    # === 2. IDENTIFICAR PONTOS MAIS PRÓXIMOS NO df ===
    def find_closest_points(centroids, df):
        closest_points = []
        for centroid in centroids:
            distances = np.linalg.norm(df[["x", "y"]].values - centroid, axis=1)
            closest_idx = np.argmin(distances)
            closest_points.append(df.iloc[closest_idx])  # Retorna a linha completa
        return pd.DataFrame(closest_points)

    df_centroids = find_closest_points(centroids_original_scale, df)

    # Identificar os pontos correspondentes no dataframe original "data"
    df_centroids_data = data.merge(
        df_centroids[["x", "y", "filename"]], on=["x", "y", "filename"], how="inner"
    )
    print(df_centroids_data)

    for key, value in df_centroids_data.iterrows():
        name = value.filename.removesuffix(".txt")
        folder = powerflow.maindir + "\\sistemas\\EXLF\\" + name
        savfile = "EXLF_" + powerflow.name + "JPMOD" + str(value.CASO) + ".SAV"
        powerflow.sxic = powerflow.maindir + "\\sistemas\\EXIC\\" + powerflow.name
        if not exists(powerflow.sxic):
            mkdir(powerflow.sxic)

        usxic(
            powerflow,
            folder_path=folder,
            savfiles=[savfile],
            start=6,
            stop=15,
            midstop=10,
            mult=0.1,
            time=8,
        )


def cxct(
    powerflow,
):
    """

    Args:
        powerflow (_type_): Description
    """
    ## Inicialização
    pass
