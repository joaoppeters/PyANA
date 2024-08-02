import geopandas as gpd
import matplotlib.pyplot as plt

# Carregar o shapefile do estado do Rio de Janeiro
rj_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\RJ_UF_2022\\RJ_UF_2022.shp"
rj = gpd.read_file(rj_shpfile)

# Carregar o shapefile das cidades do Rio de Janeiro
rj_city_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\RJ_UF_2022\\RJ_Municipios_2022.shp"
rj_city = gpd.read_file(rj_city_shpfile)

# Carregar o shapefile do estado do Espirito Santo
es_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\ES_UF_2022\\ES_UF_2022.shp"
es = gpd.read_file(es_shpfile)

# Carregar o shapefile das cidades do Espirito Santo
es_city_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\ES_UF_2022\\ES_Municipios_2022.shp"
es_city = gpd.read_file(es_city_shpfile)

# Ajustar os limites dos eixos
minx, miny, maxx, maxy = rj.total_bounds
minx2, miny2, maxx2, maxy2 = es.total_bounds

# Plotar o(s) estado(s)
fig1, ax1 = plt.subplots(figsize=(10, 8))
rj.plot(ax=ax1, color="white", edgecolor="black")
es.plot(ax=ax1, color="white", edgecolor="black")

ax1.set_xlim(min(minx, minx2), -39)
ax1.set_ylim(min(miny, miny2), max(maxy, maxy2))
ax1.set_xticks([])
ax1.set_yticks([])

# Destacar uma cidade específica
city_highlight = rj_city[rj_city['NM_MUN'] == 'Volta Redonda']
city_highlight.plot(ax=ax1, color='blue', edgecolor='black', label='2x Volta Redonda')
city_highlight = rj_city[rj_city['NM_MUN'] == 'Rio de Janeiro']
city_highlight.plot(ax=ax1, color='blue', edgecolor='black', label='2x Rio de Janeiro')
# city_highlight = rj_city[rj_city['NM_MUN'] == 'Mato Alto']
# city_highlight.plot(ax=ax1, color='red', edgecolor='black')
city_highlight = rj_city[rj_city['NM_MUN'] == 'Duque de Caxias']
city_highlight.plot(ax=ax1, color='red', edgecolor='black', label='1x Duque de Caxias')
city_highlight = es_city[es_city['NM_MUN'] == 'Itapemirim']
city_highlight.plot(ax=ax1, color='red', edgecolor='black', label='1x Itapemirim')
city_highlight = es_city[es_city['NM_MUN'] == 'Serra']
city_highlight.plot(ax=ax1, color='green', edgecolor='black', label='3x Serra')
# city_highlight = es_city[es_city['NM_MUN'] == 'Carapina'] # Serra
# city_highlight.plot(ax=ax1, color='red', edgecolor='black')
# city_highlight = es_city[es_city['NM_MUN'] == 'Itabira'] # minas gerais
# city_highlight.plot(ax=ax1, color='red', edgecolor='black')
city_highlight = es_city[es_city['NM_MUN'] == 'Barra de São Francisco']
city_highlight.plot(ax=ax1, color='red', edgecolor='black', label="1x Barra de São Francisco")
city_highlight = es_city[es_city['NM_MUN'] == 'Conceição do Castelo']
city_highlight.plot(ax=ax1, color='red', edgecolor='black', label='1x Conceição do Castelo')

plt.legend()





# Carregar o shapefile do estado de Minas Gerais
mg_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\MG_UF_2022\\MG_UF_2022.shp"
mg = gpd.read_file(mg_shpfile)

# Carregar o shapefile das cidades de Minas Gerais
mg_city_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\MG_UF_2022\\MG_Municipios_2022.shp"
mg_city = gpd.read_file(mg_city_shpfile)

# Plotar o(s) estado(s)
fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.set_xticks([])
ax2.set_yticks([])
mg.plot(ax=ax2, color="white", edgecolor="black")

# Destacar uma cidade específica
city_highlight = mg_city[mg_city['NM_MUN'] == 'Ouro Preto']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Ouro Preto')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Paracatu']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Paracatu')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Betim']
city_highlight.plot(ax=ax2, color='blue', edgecolor='black', label='2x Betim')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Três Marias']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Três Marias')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Belo Horizonte']
city_highlight.plot(ax=ax2, color='green', edgecolor='black', label='3x Belo Horizonte')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Belo Vale']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Belo Vale')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Coronel Pacheco']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Coronel Pacheco')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Poços de Caldas']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Poços de Caldas')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Patrocínio']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Patrocínio')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Juiz de Fora']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Juiz de Fora')
city_highlight = mg_city[mg_city['NM_MUN'] == 'Santa Luzia']
city_highlight.plot(ax=ax2, color='red', edgecolor='black', label='1x Santa Luzia')

plt.legend()





# Carregar o shapefile do estado de Sao Paulo
sp_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\SP_UF_2022\\SP_UF_2022.shp"
sp = gpd.read_file(sp_shpfile)

# Carregar o shapefile das cidades de Sao Paulo
sp_city_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\SP_UF_2022\\SP_Municipios_2022.shp"
sp_city = gpd.read_file(sp_city_shpfile)

# Plotar o(s) estado(s)
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.set_xticks([])
ax3.set_yticks([])
sp.plot(ax=ax3, color="white", edgecolor="black")

# Destacar uma cidade específica
# city_highlight = sp_city[sp_city['NM_MUN'] == 'Congonhas'] # São Paulo
# city_highlight.plot(ax=ax3, color='red', edgecolor='black')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Guaratinguetá']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Guaratinguetá')
# city_highlight = sp_city[sp_city['NM_MUN'] == 'Ipê'] # Campinas
# city_highlight.plot(ax=ax3, color='red', edgecolor='black')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Bragança Paulista']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Bragança Paulista')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Botucatu']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Botucatu')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Campinas']
city_highlight.plot(ax=ax3, color='green', edgecolor='black', label='3x Campinas')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Itapeva']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Itapeva')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Lençóis Paulista']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Lençóis Paulista')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Pradópolis']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Pradópolis')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Birigui']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Birigui')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Presidente Prudente']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Presidente Prudente')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Avaré']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Avaré')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Batatais']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Batatais')
# city_highlight = sp_city[sp_city['NM_MUN'] == 'Itambaracá']
# city_highlight.plot(ax=ax3, color='red', edgecolor='black')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Paulínia']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Paulínia')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Catanduva']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Catanduva')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Limeira']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Limeira')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Presidente Venceslau']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Presidente Venceslau')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Ibaté']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Ibaté')
city_highlight = sp_city[sp_city['NM_MUN'] == 'São Paulo']
city_highlight.plot(ax=ax3, color='brown', edgecolor='black', label='4x São Paulo')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Caçapava']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Caçapava')
city_highlight = sp_city[sp_city['NM_MUN'] == 'Amparo']
city_highlight.plot(ax=ax3, color='red', edgecolor='black', label='1x Amparo')

plt.legend()

plt.show()
