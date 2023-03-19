#%% Data Extraction - Example script

# url = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
# currency_code = '2'
# date = '2022-03-01'

# payload = {'moneda': currency_code, 'fecha': date}
# response = requests.post(url, data=payload)
# print(response.content)  
# res = response.content


# with open('data_raw_bcra_api.html', 'wb') as f:
#     f.write(res)


#%% Imports
import requests

#%% Exceptions definitions

# Write an Error exception class that inherits from Exception, and that when called shows a custom error message

class DateRequestError(Exception):
    '''Date Request method Error'''
    def __str__(self):
        return "Both 'Single date' and a 'Date Range' dates requested.\nPlease choose only one Date Request type."

# raise(InconsistentDateRequest)


#%% Class definition

class BCRA:
    url_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    currency_code = ('EUR': '98', 'USD':'2')
    

    def __init__(self, date = None, start_date = None, end_date = None, 
                 currency = 'USD', locator_tag, attributes):
        
        # if both extraction date  methods given: raise error
       if date &&  (start_date | end_date):
           raise DateRequestError
       else:   
            # try date parsing
            try:
                # Then define dates vars safely
                self.date = date
                self.dates = self.get_dates(start_date, end_date)
            except e:
                print(f"Date parsing Error. Failed to parse dates \n\n\t{e}")
                raise(e)
            
            # self.extract_locators = {'tag': locator_tag, **attributes} 
            # self.response_html = 
            # self.parsed_HTML = self.HTML_parse(HTML_responses)
        
from .data_models import BCRA_extractor
# Use cases:

# Extract single date
res_extr = BCRA_extractor('2023-03-01') 
# Extract date range
res_extr = BCRA_extractor(start_date='2023-02-01', end_date='2023-02-28')
# extract and filter
res_extr = BCRA_extractor('2023-03-01', locator_tag='table', attr_filter={'id':'tablita'})




#%%
with open('data_raw_bcra_api.html', 'wb') as f:
    f.write(res)
# %%
