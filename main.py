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


marker_cluster = MarkerCluster(name="home goods",disableClusteringAtZoom=14).add_to(m)

df_marina = df.loc[df['Иконка'].isin(['m'])]
df_natasha = df.loc[df['Иконка'].isin(['h'])]
df_map1 = df.loc[df['Иконка'].isin(['1'])]
df_map2 = df.loc[df['Иконка'].isin(['2'])]

df_garage = df.loc[df['Цвет'].isin(['green'])]
df_pnv = df.loc[df['Цвет'].isin(['orange'])]
df_sud = df.loc[df['Цвет'].isin(['red'])]
df_jopa = df.loc[df['Цвет'].isin(['black'])]

df_win = df.loc[df['Иконка'].isin(['star'])]


print (df_win)


for index, row in df.iterrows():
        folium.Marker([row['X'], row['Y']],
                      popup=folium.Popup("<b>ГСК</b> " + row['ГСК'] + "<br><b>Ответственный</b> " + row[
                          'Ответственный'] + "<br><b>Статус</b> " + row[
                                             'Статус'] + "<br><b>Движение дела</b> " +  row[
                                             'Движение дела'], max_width=300),
                      icon=folium.Icon(color=row['Цвет'], icon=row['Иконка'], prefix='fa')).add_to(marker_cluster)

m.save("mymap1.html")

