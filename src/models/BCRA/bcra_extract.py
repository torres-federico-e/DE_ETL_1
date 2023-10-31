
#%% Data Extraction - Example script
# --------------------------------------------------------

# url = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
# currency_code = '2'
# date = '2022-03-01'

# payload = {'moneda': currency_code, 'fecha': date}
# response = requests.post(url, data=payload)
# print(response.content)  
# res = response.content


# with open('data_raw_bcra_api.html', 'wb') as f:
#     f.write(res)


#%%   emulate main.py file for imports
#----------------------------------------------------------
import os

if os.path.exists('../../../src'): 
    os.chdir('../../../')


#%% Imports
from datetime import datetime, timedelta
from typing import List, Dict
import yaml

from bs4 import BeautifulSoup
import pandas as pd
import requests


from src.errors.bcra_errors import InvalidDateRequestError, InvalidDateFormatError



#%% Typing aliases

Response= str
Date = str
Raw_HTML = str
Raw_HTML_Responses = Dict[Date, Raw_HTML]
Parsed_HTML_tables = Dict[Date, BeautifulSoup]


#%% Date processor class
class DateProcessor:
    '''Date processor class, handles interpretation, generation of calendar dates lists, and date lists export'''
    pass


#%% Extractor Class
class BCRAExtractor:
    '''Processor class, handles requestss to BCRA API for specified dates.'''

    # Official BCRA Endpoint
    url_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    # Accepted Currencies
    currency_code = {'EUR': '98', 'USD':'2'}

    def __init__(self, date = None, test_file = None , * , start_date = None, end_date = None
                ,config_path = 'src\config\ETL_config.yaml', mock = False 
                ,locator_tag='table', **attributes):    
        try: 
            # Extraction validation
            self._is_valid_date_request(date, start_date, end_date)
            self._is_valid_date_format(date, start_date, end_date)  
            
        except InvalidDateRequestError as e:
            print("Invalid Date Request {}".format(str(e)))
            raise e
        except InvalidDateFormatError  as e:
            print("Invalid date format: {}".format(str(e)))
            raise e
        
        self.config = self.load_config_file(config_path)
        self.dates = self._get_date_list(date, start_date, end_date)
        self.raw_html = self.get_html_reponse(self.dates, self.currency_code['USD']) 


    def load_config_file(self, config_path):
        '''Class config file loader'''
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config
    
    def load_mock_response(self):
        '''Loads testing mock response'''
        file_path = self.config.get('BCRA_extraction').get('test_file')
        with open(file_path, 'rb') as test_file:
            test_file = test_file.read()
        mock_response =  {self.dates[0]:test_file}
        return mock_response
    
    def _is_valid_date_request(self, date = None, start_date = None, end_date = None):
        '''Validates date requests for API'''
        if (date and (start_date or end_date )) or (not date and not (start_date and end_date)):
            raise InvalidDateRequestError
            
    def _is_valid_date_format(self, date = None, start_date = None, end_date = None, datefmt='%Y-%m-%d') -> bool:
        '''Validates correct date format for API request. Returns-> bool'''
        try:
            if date:
                datetime.strptime(date, datefmt)
            if start_date and end_date:
                datetime.strptime(start_date, datefmt)
                datetime.strptime(end_date, datefmt)
        except ValueError:
            raise InvalidDateFormatError
    
    def _get_date_list(self, date, start_date, end_date) -> List[Date]:
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
    
    def get_html_reponse(self, dates:List[Date] = None, currency_code=None) -> Dict[Date, Raw_HTML]:
        if self.mock == False:        
            responses = self.extract_exchange_rates(dates, currency_code)
        elif self.mock == True:
            mock_response = self.raw_html = self.load_mock_response()
            responses = mock_response if 'mock_response' in locals() else responses
        return responses
    
    def extract_exchange_rates(self, dates:List[Date], currency_code=None)-> Dict[Date, Raw_HTML]:
        '''Makes API calls to BCRA API for the listed dates. 
        Returns a Dictionary with dates as keys and responses as values.
        * Return -> Dict[Date, Raw_HTML]
        '''
        responses = dict()
        for date in dates:
            # `date`: %Y-%m-%d format already for API request and Dict keys
            payload = {'moneda': currency_code, 'fecha': date}
            response = requests.post(self.url_endpoint, data=payload)
            # Extend dictionary with new keys content
            responses = {**responses, date:response.content}
        return responses


if __name__ == '__main__':
    # Real Extraction Demo
    ex_test = BCRAExtractor('2023-02-01', mock=True)
    


#%% Transformer Class
class BCRATransformer:
    '''Handles transormation between RAW HTML to 
    Structured data for final target'''
    
    def __init__(self, extractor:BCRAExtractor, extract_filters = None):
        self.extract_locators =  {'locator_tag':'table'} if extract_filters is None else extract_filters
        self.responses = extractor.raw_html
        self.parsed = self.html_parse(self.responses)
        self.tables = self._extract_tables(self.parsed)
        self.dfs = self.html_to_df(self.tables)
        
    def html_parse(self
                , html_responses:Dict[Date, Raw_HTML]
                , encoding:str = 'iso-8859-1'
                , parser:str = 'html.parser') -> Dict[Date, BeautifulSoup]:
        '''Takes Dict with dates as keys and Raw_HTML as values and
        parses them into BeautifulSoup objects with 'html.parser' by default.
        -> returns dict.'''
        # _parsed = list()
        _parsed = dict()
        for date, response in html_responses.items():            
            parsed_html = BeautifulSoup(response.decode(encoding=encoding), parser)
            _parsed = {**_parsed, date:parsed_html}
            # _parsed.append(parsed_html)
        return _parsed

    def _extract_tables(self, parsed_html: BeautifulSoup) -> Dict[Date, Parsed_HTML_tables]: 
        '''Takes parsed BeautifulSoup objects and extracts the Exchange Rate tables.
        Returns only filtered, matching HTML objects. 
        returns -> Dict[Date, BeautifulSoup] '''
        etag = self.extract_locators['tag']
        eid = self.extract_locators['id']
        for date, soup in parsed_html.items():
            rate_table = soup.find(etag, {'id':eid})
            result_tables = {**parsed_html, date:rate_table}
        return result_tables

    def html_to_df(self, date_tables: Dict[Date, Parsed_HTML_tables]) -> Dict[Date, pd.DataFrame]:
        '''Takes BeautifulSoup parsed tables and transforms to Pandas Dataframe
        returns -> Dict[Date, Dataframe]'''
        final = dict()
        for date, tables in date_tables.items():
            table_list = []
            for table in tables:
                _df_table = pd.read_html(str(table))
                table_list.append(_df_table)
            final = {**final, date:table_list}
        return final













    
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


