import folium
import pandas as pd
import os
import requests
import gspread as gs


gc = gs.service_account(filename='model-zoo-363409-d778a0fccb80.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10awekJr1rw0AikidtV5rVTpM0AI1zjwUcodCp5Q3SXE/edit#gid=1313466868')

ws = sh.worksheet('Лист7')

df = pd.DataFrame(ws.get_all_records())
print(list(df))
