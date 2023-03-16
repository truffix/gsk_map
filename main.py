import folium
import pandas as pd
import gspread as gs
from folium.plugins import FloatImage
from folium.plugins import MarkerCluster
from flask import Flask, render_template, send_from_directory
import os
from datetime import timedelta
import datetime
import threading
from threading import Thread
import requests

import schedule
import time

from threading import Timer

app = Flask(__name__)

@app.route("/", methods=["GET"])
def status():
    print("/")
    return "Status: OK"



gc = gs.service_account(filename='model-zoo-363409-d778a0fccb80.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10awekJr1rw0AikidtV5rVTpM0AI1zjwUcodCp5Q3SXE/edit#gid=1313466868')
ws = sh.worksheet('Лист7')

df = pd.DataFrame(ws.get_all_records())

df['X'] = pd.to_numeric(df['X'], errors='coerce')
df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
df['X'] = df['X'].round(7)
df['Y'] = df['Y'].round(7)
df = df.dropna (subset=['X'])


print (df)
print(list(df))
df.to_excel('111.xlsx')


m = folium.Map(location=[df['X'].mean(), df['Y'].mean()], zoom_start=12)
image_file = 'https://geo35.ru/upload/CAllcorp2/995/9957d6a37c0ccdd4085cf7a739e7ca14.png'
FloatImage(image_file, bottom=5, left=45).add_to(m)




cluster_marina = MarkerCluster(name="Марина",disableClusteringAtZoom=13).add_to(m)
cluster_natasha = MarkerCluster(name="Наташа",disableClusteringAtZoom=13).add_to(m)
cluster_map1 = MarkerCluster(name="МАП 1",disableClusteringAtZoom=13).add_to(m)
cluster_map2 = MarkerCluster(name="МАП 2",disableClusteringAtZoom=13).add_to(m)
cluster_garage = MarkerCluster(name="Гаражная амнистия",disableClusteringAtZoom=14).add_to(m)
cluster_pnv = MarkerCluster(name="ПНВ",disableClusteringAtZoom=13).add_to(m)
cluster_sud = MarkerCluster(name="Суд",disableClusteringAtZoom=13).add_to(m)
cluster_jopa = MarkerCluster(name="Попа",disableClusteringAtZoom=13).add_to(m)
cluster_win = MarkerCluster(name="Победа",disableClusteringAtZoom=13).add_to(m)
cluster_yandex = MarkerCluster(name="Яндекс",disableClusteringAtZoom=13).add_to(m)



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
        elif row['Иконка'] == 'location-dot':
            cluster_yandex.add_child(marker)


folium.LayerControl().add_to(m)
m.save("mymap1.html")

app.run(host="0.0.0.0", port=4000, debug=True)
