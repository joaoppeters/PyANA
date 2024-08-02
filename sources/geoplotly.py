import chart_studio
import chart_studio.plotly as py
import geopandas as gpd
import plotly.graph_objects as go

chart_studio.tools.set_credentials_file(username='joaoppeters', api_key='PBhlGZaWsykigce0Bap1')

def city_highlight(
    fig,
    data,
    cityname,
    color,
    show,
):
    if color == 'red':
        name = '1x'
    elif color == 'blue':
        name = '2x'
    elif color == 'green':
        name = '3x'
    elif color == 'brown':
        name = '4x'
            
    highlight = data[data['NM_MUN'] == cityname]
    fig.add_trace(go.Scattermapbox(
        lon=highlight.geometry.x,
        lat=highlight.geometry.y,
        text=highlight['NM_MUN'],
        mode='markers',
        marker=dict(color=color, size=10),
        name=name,
        showlegend=show,
    ))

# Carregar o shapefile do estado do Espírito Santo
es_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\ES_UF_2022\\ES_UF_2022.shp"
es = gpd.read_file(es_shpfile)

# Carregar o shapefile das cidades do Espírito Santo
es_cities  = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\ES_UF_2022\\ES_Municipios_2022.shp"
esct = gpd.read_file(es_cities)

# Converter geometrias de cidades para pontos (centroides)
esct['geometry'] = esct['geometry'].centroid

#------------------------------------------------------------

# Carregar o shapefile do estado de Minas Gerais
mg_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\MG_UF_2022\\MG_UF_2022.shp"
mg = gpd.read_file(mg_shpfile)

# Carregar o shapefile das cidades de Minas Gerais
mg_cities  = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\MG_UF_2022\\MG_Municipios_2022.shp"
mgct = gpd.read_file(mg_cities)

# Converter geometrias de cidades para pontos (centroides)
mgct['geometry'] = mgct['geometry'].centroid

#------------------------------------------------------------

# Carregar o shapefile do estado do Rio de Janeiro
rj_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\RJ_UF_2022\\RJ_UF_2022.shp"
rj = gpd.read_file(rj_shpfile)

# Carregar o shapefile das cidades do Rio de Janeiro
rj_cities  = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\RJ_UF_2022\\RJ_Municipios_2022.shp"
rjct = gpd.read_file(rj_cities)

# Converter geometrias de cidades para pontos (centroides)
rjct['geometry'] = rjct['geometry'].centroid

#------------------------------------------------------------

# Carregar o shapefile do estado de São Paulo
sp_shpfile = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\SP_UF_2022\\SP_UF_2022.shp"
sp = gpd.read_file(sp_shpfile)

# Carregar o shapefile das cidades de São Paulo
sp_cities  = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\BRASIL\\SP_UF_2022\\SP_Municipios_2022.shp"
spct = gpd.read_file(sp_cities)

# Converter geometrias de cidades para pontos (centroides)
spct['geometry'] = spct['geometry'].centroid

#------------------------------------------------------------

# Converter para GeoJSON
es_geojson = es.__geo_interface__
mg_geojson = mg.__geo_interface__
rj_geojson = rj.__geo_interface__
sp_geojson = sp.__geo_interface__

#------------------------------------------------------------

# Criar uma figura de mapa
fig = go.Figure()

# Adicionar Espírito Santo ao mapa
fig.add_trace(go.Choroplethmapbox(
    geojson=es_geojson,
    locations=[0],  # Uma localização arbitrária para plotar o estado inteiro
    z=[1],  # Valor arbitrário para coloração
    colorscale=[[0, 'lightblue'], [1, 'lightblue']],  # Cor fixa
    showscale=False,
    name='Espírito Santo'
))
city_highlight(fig=fig, data=esct, cityname='Itapemirim', color='red', show=True,)
city_highlight(fig=fig, data=esct, cityname='Serra', color='green', show=True,)
city_highlight(fig=fig, data=esct, cityname='Barra de São Francisco', color='red', show=False,)
city_highlight(fig=fig, data=esct, cityname='Conceição do Castelo', color='red', show=False,)

#------------------------------------------------------------

# Adicionar Minas Gerais ao mapa
fig.add_trace(go.Choroplethmapbox(
    geojson=mg_geojson,
    locations=[0],  # Uma localização arbitrária para plotar o estado inteiro
    z=[1],  # Valor arbitrário para coloração
    colorscale=[[0, 'lightblue'], [1, 'lightblue']],  # Cor fixa
    showscale=False,
    name='Minas Gerais'
))
# Destacar uma cidade específica
city_highlight(fig=fig, data=mgct, cityname='Ouro Preto', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Paracatu', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Betim', color='blue', show=True,)
city_highlight(fig=fig, data=mgct, cityname='Três Marias', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Belo Horizonte', color='green', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Belo Vale', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Coronel Pacheco', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Poços de Caldas', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Patrocínio', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Juiz de Fora', color='red', show=False,)
city_highlight(fig=fig, data=mgct, cityname='Santa Luzia', color='red', show=False,)

#------------------------------------------------------------

# Adicionar Rio de Janeiro ao mapa
fig.add_trace(go.Choroplethmapbox(
    geojson=rj_geojson,
    locations=[0],
    z=[1],
    colorscale=[[0, 'lightblue'], [1, 'lightblue']],  # Cor fixa
    showscale=False,
    name='Rio de Janeiro'
))
# Destacar uma cidade específica
city_highlight(fig=fig, data=rjct, cityname='Volta Redonda', color='blue', show=False,)
city_highlight(fig=fig, data=rjct, cityname='Rio de Janeiro', color='blue', show=False,)
city_highlight(fig=fig, data=rjct, cityname='Duque de Caxias', color='red', show=False,)

#------------------------------------------------------------

# Adicionar São Paulo ao mapa
fig.add_trace(go.Choroplethmapbox(
    geojson=sp_geojson,
    locations=[0],
    z=[1],
    colorscale=[[0, 'lightblue'], [1, 'lightblue']],  # Cor fixa
    showscale=False,
    name='São Paulo'
))

# Destacar uma cidade específica

city_highlight(fig=fig, data=spct, cityname='Guaratinguetá', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Bragança Paulista', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Botucatu', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Campinas', color='green', show=False,)
city_highlight(fig=fig, data=spct, cityname='Itapeva', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Lençóis Paulista', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Pradópolis', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Birigui', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Presidente Prudente', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Avaré', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Batatais', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Paulínia', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Catanduva', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Limeira', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Presidente Venceslau', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Ibaté', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='São Paulo', color='brown', show=True,)
city_highlight(fig=fig, data=spct, cityname='Caçapava', color='red', show=False,)
city_highlight(fig=fig, data=spct, cityname='Amparo', color='red', show=False,)

#------------------------------------------------------------

# Calcular o centro aproximado
center_lat = (mg.geometry.centroid.y.mean() + sp.geometry.centroid.y.mean() +
              es.geometry.centroid.y.mean() + rj.geometry.centroid.y.mean()) / 4
center_lon = (mg.geometry.centroid.x.mean() + sp.geometry.centroid.x.mean() +
              es.geometry.centroid.x.mean() + rj.geometry.centroid.x.mean()) / 4

# Configurar layout do mapa para focar no Brasil
fig.update_layout(
    mapbox=dict(
        style='carto-positron',  # Estilo do mapa
        center=dict(lat=center_lat, lon=center_lon),  # Centro aproximado entre MG e SP
        zoom=5  # Ajustar o zoom para focar nos estados
    ),
    title='Mapa dos Estados da Região Sudeste do Brasil',
    legend_title_text='Número de Medidores (PMUs)',
    legend=dict(
        x=0.02,  # Posição horizontal da legenda
        y=0.98,  # Posição vertical da legenda
        bgcolor='rgba(255, 255, 255, 0.8)',  # Cor de fundo com transparência
        bordercolor='rgba(0, 0, 0, 0.1)',  # Cor da borda
        borderwidth=1
    ),
    margin={"r":0,"t":30,"l":0,"b":0},
)


# # Mostrar o mapa
# fig.show()
fig.write_html('sudeste.html')



# # Assumindo que 'fig' é o seu objeto de figura Plotly
# url = py.plot(fig, filename='mapa_regiao_sudeste', auto_open=False)
# print(url)