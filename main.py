import folium
import pandas as pd
import os
import requests
import gspread as gs
from folium.plugins import FloatImage
import os
from folium.plugins import MarkerCluster



gc = gs.service_account(filename='model-zoo-363409-d778a0fccb80.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10awekJr1rw0AikidtV5rVTpM0AI1zjwUcodCp5Q3SXE/edit#gid=1313466868')

ws = sh.worksheet('Лист7')

df = pd.DataFrame(ws.get_all_records())

print(list(df))
df['X'] = pd.to_numeric(df['X'], errors='coerce')
df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
df = df.dropna (subset=['X'])
# df.to_excel('data_survey.xlsx')
print (df['X'])
print (df['Y'])

m = folium.Map(location=[df['X'].mean(), df['Y'].mean()], zoom_start=12)
image_file = 'https://geo35.ru/upload/CAllcorp2/995/9957d6a37c0ccdd4085cf7a739e7ca14.png'
FloatImage(image_file, bottom=5, left=45).add_to(m)




cluster_marina = MarkerCluster(name="Марина",disableClusteringAtZoom=14).add_to(m)
cluster_natasha = MarkerCluster(name="Наташа",disableClusteringAtZoom=14).add_to(m)
cluster_map1 = MarkerCluster(name="МАП 1",disableClusteringAtZoom=14).add_to(m)
cluster_map2 = MarkerCluster(name="МАП 2",disableClusteringAtZoom=14).add_to(m)
cluster_garage = MarkerCluster(name="Гаражная амнистия",disableClusteringAtZoom=14).add_to(m)
cluster_pnv = MarkerCluster(name="ПНВ",disableClusteringAtZoom=14).add_to(m)
cluster_sud = MarkerCluster(name="Суд",disableClusteringAtZoom=14).add_to(m)
cluster_jopa = MarkerCluster(name="Попа",disableClusteringAtZoom=14).add_to(m)
cluster_win = MarkerCluster(name="Победа",disableClusteringAtZoom=14).add_to(m)



# df_marina = df.loc[df['Иконка'].isin(['m'])]
# df_natasha = df.loc[df['Иконка'].isin(['h'])]
# df_map1 = df.loc[df['Иконка'].isin(['1'])]
# df_map2 = df.loc[df['Иконка'].isin(['2'])]
#
# df_garage = df.loc[df['Цвет'].isin(['green'])]
# df_pnv = df.loc[df['Цвет'].isin(['orange'])]
# df_sud = df.loc[df['Цвет'].isin(['red'])]
# df_jopa = df.loc[df['Цвет'].isin(['black'])]
#
# df_win = df.loc[df['Иконка'].isin(['star'])]
#
# # layer_marina = folium.FeatureGroup(name='Марина', show=True)
# # layer_natasha = folium.FeatureGroup(name='Наташа', show=True)
# # layer_map1 = folium.FeatureGroup(name='МАП 1', show=True)
# # layer_map2 = folium.FeatureGroup(name='МАП 2', show=True)
# # layer_garage = folium.FeatureGroup(name='Гаражная амнистия', show=True)
# # layer_pnv = folium.FeatureGroup(name='ПНВ', show=True)
# # layer_sud = folium.FeatureGroup(name='Суд ', show=True)
# # layer_jopa = folium.FeatureGroup(name='Попа', show=True)
# # layer_win = folium.FeatureGroup(name='Победа', show=True)


for index, row in df.iterrows():
        marker = folium.Marker([row['X'], row['Y']],
                      popup=folium.Popup("<b>ГСК</b> " + row['ГСК'] + "<br><b>Ответственный</b> " + row[
                          'Ответственный'] + "<br><b>Статус</b> " + row[
                                             'Статус'] + "<br><b>Движение дела</b> " +  row[
                                             'Движение дела'], max_width=300),
                      icon=folium.Icon(color=row['Цвет'], icon=row['Иконка'], prefix='fa'))

        if row['Иконка'] == 'm':
            cluster_marina.add_child(marker)
        elif row['Иконка'] == 'h':
            cluster_natasha.add_child(marker)
        elif row['Иконка'] == '1':
            cluster_map1.add_child(marker)
        elif row['Иконка'] == '2':
            cluster_map2.add_child(marker)
        elif row['Цвет'] == 'green':
            cluster_garage.add_child(marker)
        elif row['Цвет'] == 'orange':
            cluster_pnv.add_child(marker)
        elif row['Цвет'] == 'red':
            cluster_sud.add_child(marker)
        elif row['Цвет'] == 'black':
            cluster_jopa.add_child(marker)
        elif row['Иконка'] == 'star':
            cluster_win.add_child(marker)


folium.LayerControl().add_to(m)
m.save("mymap1.html")

