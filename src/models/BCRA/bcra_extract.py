
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
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime, timedelta

from typing import List, Dict


#%% Exceptions definitions

class DateRequestError(Exception):
    '''Date Request method Error'''
    def __str__(self):
        return "Inconsistent date extraction request specified. Please choose a Single date request, or a Date Range request via Start_Date and End_Date."



#%% Class definition

# f5avr1354712366aaaaaaaaaaaaaaaa_cspm_ = IHCEKDFDOHJADMMGLBMDDODJJMBJEECBKPFLOCBMNBPABGANKBGILFFHDPAIMMBHKCFBFJLLDKLKPHBFDNFALNNBACKDBDFMFFIOLFKINHKOOKJEHJMIAKFLIGEECFGD
# f5_cspm = IHCEKDFDOHJADMMGLBMDDODJJMBJEECBKPFLOCBMNBPABGANKBGILFFHDPAIMMBHKCFCFJLLAELKPHBFDNFALNNBCHKDBDFMFFIOLFKINHKOOKJEHJMIAKFLIGEECFGD

response= str
responses = List[response]
date = str
dates = List[date]
HTML_table_str = str


class BCRAExtractor:
    url_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    currency_code = {'EUR': '98', 'USD':'2'}

    def __init__(self, date = None, start_date = None, end_date = None, locator_tag='table', **attributes):    
        
        self.dates = self._get_date_list(date, start_date, end_date)
        self.extract_locators = {'tag': locator_tag, **attributes} 
        self.response = self.extract_dates_rates(self.dates, self.currency_code['USD']) 
        # self.parsed_HTML = self.HTML_parse(self.response)


    def _get_date_list(self, date, start_date, end_date):
        '''Calculates list of dates if Date Range extraction was specified with
        `start_date` and `end_date` and complying with date format 'YYYY-MM-DD'
        for compatible requests with BCRA API'''
        datefmt = '%Y-%m-%d'
        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, datefmt)
            end_date = datetime.strptime(end_date, datefmt)
            dates = [datetime.strftime(start_date + timedelta(days=i), datefmt)
                        for i in range((end_date - start_date).days + 1)]
            return dates
        elif date:
            return [date]
          
    def extract_dates_rates(self, dates:List[dates] = None, currency_code=None):
    # -> Dict[str:responses]:
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
            
    def HTML_parse(self, html_response, encoding:str = 'iso-8859-1'):
        '''Parses response and returns BeautifulSoup parsed object from HTML response'''
        _parsed = list()
        for res in html_response:
            res = res.content
            with open(res, encoding= encoding) as fp:
                parsed_html = BeautifulSoup(fp.read(), 'html.parser')
            _parsed.append(parsed_html)
        return _parsed
            
    def _extract_tables(self, parsed_html: BeautifulSoup) -> HTML_table_str: 
        '''Locates and extracts Exchange Rate tables from within BeautifulSoup parsed objects ('soups')'''
        etag = self.page_elements_locators['tag']
        eid = self.page_elements_locators['id']
        rate_table = parsed_html.find(etag, {'id':eid})
        return rate_table

    def _HTML_to_df(self, html_str_table: HTML_table_str):
        '''Exports extracted individual table to Pandas Dataframe'''
        return pd.read_html(str(html_str_table))
    
    
#%%

if __name__ == '__main__':
    res = BCRAExtractor('2023-03-01')

    
#%% USE CASES
##################################

# from .data_models import BCRA_extractor
# # Use cases:

# # Extract single date
# res_extr = BCRA_extractor('2023-03-01') 
# # Extract date range
# res_extr = BCRA_extractor(start_date='2023-02-01', end_date='2023-02-28')
# # extract and filter
# res_extr = BCRA_extractor('2023-03-01', locator_tag='table', attr_filter={'id':'tablita'})


