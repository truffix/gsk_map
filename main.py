import folium
import pandas as pd
import os
import requests

sheet_id = "10awekJr1rw0AikidtV5rVTpM0AI1zjwUcodCp5Q3SXE"
sheet_name = "Лист7"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

url = url
df = pd.read_csv(url)
# print (url)