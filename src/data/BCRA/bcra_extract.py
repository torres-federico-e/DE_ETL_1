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
from datetime import datetime

from typing import List, Dict


#%% Exceptions definitions

# Write an Error exception class that inherits from Exception, and that when called shows a custom error message

class DateRequestError(Exception):
    '''Date Request method Error'''
    def __str__(self):
        return "Both 'Single date' and a 'Date Range' dates requested.\nPlease choose only one Date Request type."

# raise(InconsistentDateRequest)


#%% Class definition

response= str
responses = List[response]
date = str
dates = List[date]

class BCRA:
    url_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    currency_code = {'EUR': '98', 'USD':'2'}
    

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
                print(f"Date Error.\n{e}")
                raise(e)
            
            # self.extract_locators = {'tag': locator_tag, **attributes} 
            # self.response_html = 
            # self.parsed_HTML = self.HTML_parse(HTML_responses)
        
    def get_date_list(start_date, end_date):
        '''Calculates list of dates with format 'YYYY-MM-DD' 
        '%Y-%m-%d' in datetime format string, compatible with BCRA API'''
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        dates = [datetime.strftime(start_date + timedelta(days=i), '%Y-%m-%d')
                    for i in range((end_date - start_date).days + 1)]
        return dates
        
        
        
        
    def extract_dates_rates(dates:List[dates]) --> Dict[response]:
        '''Makes API calls to BCRA API for the listed dates. 
        Returns a Dictionary with dates as keys and responses as values.
        * Return -> Dict[date:response]'''
        responses = dict()
        for date in dates:
            payload = {'moneda': currency_code, 'fecha': date}
            response = requests.post(self.url_endpoint, data=payload)
            #Updates dictionary with new date content
            responses = {**responses, date:response}
        return responses
            
    def HTML_parse(HTML_responses, encoding:str = 'iso-8859-1'):
        '''Parses response and returns BeautifulSoup parsed object from HTML response'''
        _parsed = list()
        for res in HTML_responses:
            res = res.content
            with open(res, encoding= encoding) as fp:
                parsed_html = BeautifulSoup(fp.read(), 'html.parser')
            _parsed.append(parsed_html)
        return _parsed
            
    def extract_tables(self, parsed_html: BeautifulSoup) -> HTML_table_str: 
        '''Locates and extracts Exchange Rate tables from within BeautifulSoup parsed objects ('soups')'''
        etag = self.page_elements_locators['tag']
        eid = self.page_elements_locators['id']
        rate_table = parsed_html.find(etag, {'id':eid})
        return rate_table
     
#%%




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
