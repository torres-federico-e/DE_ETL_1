
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

Response= str
Responses = List[Response]
Date = str
Dates = List[Date]
Parsed_HTML_tables =Dict[Dates:BeautifulSoup]
FilteredTables = Dict[Dates:Parsed_HTML_tables] = str



class BCRAExtractor:
    url_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    currency_code = {'EUR': '98', 'USD':'2'}

    def __init__(self, date = None, start_date = None, end_date = None, locator_tag='table', **attributes):    
        try: 
            self.is_valid_date_request(date, start_date, end_date)
            self.is_valid_date_format(date, start_date, end_date)    
        except Exception as e:
            print("Error while checking dates")
            raise e
        
        # Define dates vars safely
        self.dates = self._get_date_list(date, start_date, end_date)
        self.extract_locators = {'tag': locator_tag, **attributes} 
        self.response = self.extract_dates_rates(self.dates, self.currency_code['USD']) 
        # self.parsed_HTML = self.HTML_parse(self.response)


    
    def is_valid_date_request(self, date = None, start_date = None, end_date = None):
        '''Validates date requests for API. Returns Boolean, True only for Valid requests'''
        if (date and (start_date or end_date )) or (not date and not (start_date and end_date)):
            raise DateRequestError
            
    def is_valid_date_format(self, date = None, start_date = None, end_date = None, datefmt='%Y-%m-%d'):
        '''Validates date format for API. Returns Boolean, True only for Valid requests'''
        try:
            if date:
                datetime.strptime(date, datefmt)
            elif start_date and end_date:
                datetime.strptime(start_date, datefmt)
                datetime.strptime(end_date, datefmt)
            else:
                return False
        except ValueError:
            raise ValueError("Incorrect date specified. Please use format 'YYYY-MM-DD'")
        return True

    
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
    
    def extract_dates_rates(self, dates:List[Dates] = None, currency_code=None):
        '''Makes API calls to BCRA API for the listed dates. 
        Returns a Dictionary with dates as keys and responses as values.
        * Return -> Dict[date:response]'''
        responses = dict()
        for date in dates:
            # `date`: %Y-%m-%d format already for API request and Dict keys
            payload = {'moneda': currency_code, 'fecha': date}
            response = requests.post(self.url_endpoint, data=payload)
            # Extend dictionary with new keys content
            responses = {**responses, date:response}
        return responses


class BCRATransformer:
    '''Handles RAW HTML response transformation to 
    Structured data for final data target'''       
    def __init__(self, html_responses:Dict[responses]):
        self.responses = html_responses
        self.parsed = self.html_parse(self.responses)
        self.tables = self._extract_tables(self.parsed)
        self.dfs = self.html_to_df(self.tables)
        
    def html_parse(self, html_responses, encoding:str = 'iso-8859-1', parser:str = 'html.parser'):
        '''Parses RAW HTMLresponses per date received from Dict with 
        Dates as keys and Raw Html responses as values.
        Returns Dict of parsed BeautifulSoup objects
        with dates as keys for further processing'''
        # _parsed = list()
        _parsed = dict()
        for date, response in html_responses.items():            
            response = response.content
            with open(response, encoding= encoding) as fp:
                parsed_html = BeautifulSoup(fp.read(), parser)
            _parsed = {**_parsed, date:parsed_html}
            # _parsed.append(parsed_html)
        return _parsed

    def _extract_tables(self, parsed_html: BeautifulSoup) -> Dict[Dates:Parsed_HTML_tables]: 
        '''Processes dates and extracts Exchange Rate tables from
        BeautifulSoup parsed HTML (the actual 'soups' elements)
        Returns a Dict with dates as keys and list of matching 
        elements as values'''
        etag = self.extract_locators['tag']
        eid = self.extract_locators['id']
        
        for date, soup in parsed_html.items():
            rate_table = soup.find(etag, {'id':eid})
            result_tables = {**parsed_html, date:rate_table}
        return result_tables


    def html_to_df(self, date_tables: Dict[Dates:Parsed_HTML_tables]):
        '''Process and exports parsed tables to Pandas Dataframe'''
        final = dict()
        for date, tables in date_tables.items():
            table_list = []
            for table in tables:
                _df_table = pd.read_html(str(table))
                table_list.append(_df_table)
            final = {**final, date:table_list}
        return final
    
    
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


