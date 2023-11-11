
# Standard lib
import os
from datetime import datetime, timedelta
from typing import List, Dict

# Modules
import requests
from bs4 import BeautifulSoup
import yaml
import pandas as pd

# internal
from src.errors.bcra_errors import InvalidDateRequestError, InvalidDateFormatError


# Type definitions
Response= str
Date = str
Raw_HTML = str
Raw_HTML_Responses = Dict[Date, Raw_HTML]
Parsed_HTML_tables = Dict[Date, BeautifulSoup]


#%% Date processor class
class DateProcessor:
    '''Processor class, handles date interpretation, validation and generation of calendar ranges'''
    pass




#%% Extractor Class
class BCRAExtractor:
    '''Processor class, handles BCRA API requests to extract exchange rates from for specified dates.'''

    # BCRA Endpoint
    default_api_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    
    # Supported Currencies
    currency_code = {
                     'EUR': '98', 
                     'USD':'2'
                     }

    def __init__(self, date = None, test_file = None , * , start_date = None, end_date = None
                ,config_path = 'src\config\ETL_config.yaml', mock = False 
                ,locator_tag='table', **attributes):    
        
        try: 
            #------------------------------------------------------------
            #TODO: Abstract Date validation to Date processor Class
            # Extraction validation
            #------------------------------------------------------------
            self._is_valid_date_request(date, start_date, end_date)
            self._is_valid_date_format(date, start_date, end_date)  
            
        except InvalidDateRequestError as e:
            print("Invalid Date Request {}".format(str(e)))
            raise e
        except InvalidDateFormatError  as e:
            print("Invalid date format: {}".format(str(e)))
            raise e
        
            #-------------------------------------------------------------


        self.config = self.load_config_file(config_path)
        self.dates = self._get_date_list(date, start_date, end_date)
        self.raw_html = self.get_html_response() 

    @classmethod
    def extract_exchange_rates(cls, dates:List[Date], currency_code=None)\
        -> Dict[Date, Raw_HTML]:
        '''
        Extracts exchange rates from  BCRA API for specific dates.
        Returns dictionary with dates and raw HTML as response.
         Returns -> Dict[Date, Raw_HTML]
        '''
        responses = dict()
        for date in dates:
            # `date`: %Y-%m-%d format already for API request and Dict keys
            payload = {'moneda': currency_code, 'fecha': date}
            response = requests.post(cls.default_api_endpoint, data=payload)
            # Extend dictionary with new keys content
            responses = {**responses, date:response.content}
        return responses

    def get_html_response(self) -> Dict[Date, Raw_HTML]:
        '''Get HTML response from BCRA API service for configured dates
          or from local test_file for debugging purposes'''
        if self.test_file is None:        
            responses = self.extract_exchange_rates(self.dates, self.currency_code)
        elif self.test_file is not None:
            # Check str is path + File
            if os.path.isfile(self.test_file):
                try: 
                    mock_response = self.load_test_file()
                    responses = mock_response if 'mock_response' in locals() else responses
                except FileNotFoundError as e:
                    raise e.add_note("Provided Test file Does not Exist")
        return responses
    
    def load_test_file(self):
        '''Loads test file as extraction response'''
        with open(test_file, 'rb') as test_file:
            test_file = test_file.read()
        mock_response =  {self.dates[0]:test_file}
        return mock_response
    
    def load_config_file(self, config_path):
        '''Class config file loader'''
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config

# 
# 
# ...
# 
# 

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


    
#%% Quickstart - Demo
##################################

if __name__ == '__main__':

    # Extract single date
    single = BCRAExtractor('2023-03-01') 
    # Extract date range
    range_ = BCRAExtractor(start_date='2023-02-01', end_date='2023-02-28')
    # extract and filter
    filter_ = BCRAExtractor('2023-03-01', locator_tag='table', attr_filter={'id':'tablita'})


