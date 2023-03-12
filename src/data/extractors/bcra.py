#%% Imports
import requests

#%% Data Extraction

url = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
currency_code = '2'
date = '2022-03-01'

payload = {'moneda': currency_code, 'fecha': date}
response = requests.post(url, data=payload)
print(response.content)  
res = response.content


#%%
with open('data_raw_bcra_api.html', 'wb') as f:
    f.write(res)
# %%
