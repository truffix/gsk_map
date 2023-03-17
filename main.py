import folium
import pandas as pd
import gspread as gs
from folium.plugins import FloatImage
from folium.plugins import MarkerCluster
from folium.plugins import Search, FeatureGroupSubGroup
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

@app.route("/map", methods=["GET"])
def map():
    print("/map")
    return render_template("mymap1.html")

gc = gs.service_account(filename='model-zoo-363409-d778a0fccb80.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10awekJr1rw0AikidtV5rVTpM0AI1zjwUcodCp5Q3SXE/edit#gid=1313466868')
ws = sh.worksheet('Лист7')

def generate_map():

    df = pd.DataFrame(ws.get_all_records())

    df['X'] = pd.to_numeric(df['X'], errors='coerce')
    df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
    df = df.dropna (subset=['X'])


    # print (df)
    # print(list(df))
    df.to_excel('111.xlsx')


    m = folium.Map(location=[df['X'].mean(), df['Y'].mean()], zoom_start=12)
    image_file = 'https://geo35.ru/upload/CAllcorp2/995/9957d6a37c0ccdd4085cf7a739e7ca14.png'
    FloatImage(image_file, bottom=5, left=45).add_to(m)


    layer1 = folium.FeatureGroup(name='Все ГСК', show=True)
    m.add_child(layer1)

    cluster_marina = FeatureGroupSubGroup(layer1, name="Марина",control=True)
    m.add_child(cluster_marina)
    cluster_natasha = FeatureGroupSubGroup(layer1,name="Наташа",control=True)
    m.add_child(cluster_natasha)
    cluster_map1 = FeatureGroupSubGroup(layer1,name="МАП 1",control=True)
    m.add_child(cluster_map1)
    cluster_map2 = FeatureGroupSubGroup(layer1,name="МАП 2",control=True)
    m.add_child(cluster_map2)
    cluster_garage = FeatureGroupSubGroup(layer1,name="Гаражная амнистия",control=True)
    m.add_child(cluster_garage)
    cluster_pnv = FeatureGroupSubGroup(layer1,name="ПНВ",control=True)
    m.add_child(cluster_pnv)
    cluster_sud = FeatureGroupSubGroup(layer1,name="Суд",control=True)
    m.add_child(cluster_sud)
    cluster_jopa = FeatureGroupSubGroup(layer1,name="Попа",control=True)
    m.add_child(cluster_jopa)
    cluster_win = FeatureGroupSubGroup(layer1,name="Победа",control=True)
    m.add_child(cluster_win)
    cluster_yandex = FeatureGroupSubGroup(layer1,name="Яндекс",control=True)
    m.add_child(cluster_yandex)


    for index, row in df.iterrows():
            marker = folium.Marker([row['X'], row['Y']],
                          popup=folium.Popup("<b>ГСК</b> " + row['ГСК'] + "<br><b>Ответственный</b> " + row[
                              'Ответственный\n(Цветкова, Павлова)'] + "<br><b>Статус</b> " + row[
                                                 'Статус\n(ГА, ПНВ, СУД)'] + "<br><b>Движение дела</b> " +  row[
                                                 'Движение дела\n(дата/что сделано/результат)'], max_width=300),name = row['ГСК'],
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
            elif row['Цвет'] == 'lightgray':
                cluster_yandex.add_child(marker)

    servicesearch = Search(
        layer=layer1,
        search_label="name",
        geom_type='Point',
        placeholder='Название ГСК',
        collapsed=False,
        position="topright"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save("templates/mymap1.html")

username = 'geo35'
token = '3fe69bd7ba44d4bdd6568f4c3e23ef7cf5f75604'
domain_name = "geo35.pythonanywhere.com"

def reload():
    response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
            username=username, domain_name=domain_name
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    if response.status_code == 200:
        print('reloaded OK')
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

def logi_def(x, y):
    logi = pd.read_csv('log.csv')
    logi = logi[['Время', 'Сообщение']]
    df_logi = pd.DataFrame({'Время': [x],
                        'Сообщение': [y]})

    logi = logi.append(df_logi, ignore_index=True)
    logi.to_csv('log.csv')

def check():




if __name__ == "__main__":
   app.run(port=8080)
