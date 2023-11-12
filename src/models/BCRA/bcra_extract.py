
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
    def __init__(self, start_date=None, end_date=None, date=None):
        self._is_valid_date(start_date, end_date, date)
        self._is_valid_request(start_date, end_date, date)
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.date_range = self.get_date_range(self.start_date, self.end_date, self.date)
    
    def _is_valid_request(self, start_date = None, end_date = None, date = None, ):
        '''Checks consistent requests. Single date or date range, but not both'''
        if (date and (start_date or end_date )) or (not date and not (start_date and end_date)):
            raise InvalidDateRequestError
            
    def _is_valid_date(self, start_date = None, end_date = None, date = None, datefmt='%Y-%m-%d') -> bool:
        '''Checks valid date string format.'''
        try:
            for dt in [date, start_date, end_date]:
                datetime.strptime(dt, datefmt)
        except ValueError:
            raise InvalidDateFormatError
        
    @staticmethod
    def get_date_range(start_date, end_date, date) -> List[Date]:
        '''Calculates calendar list of dates for Date Range provided. 
        If `date` was provided, takes precedence and overrides date range calculation.
        Returns BCRA API compatible 'YYYY-MM-DD'date format list.'''
        datefmt = '%Y-%m-%d'
        if date: 
            return [date]
        elif (start_date is not None and end_date is not None):
            start_date = datetime.strptime(start_date, datefmt)
            end_date = datetime.strptime(end_date, datefmt)
            dates = [datetime.strftime(start_date + timedelta(days=i), datefmt)
                        for i in range((end_date - start_date).days + 1)]
            return dates
        else: 
            return ['1970-01-01']
            


    


#%% Extractor Class
class BCRAExtractor:
    '''Extracts raw HTML requests from BCRA API for specified dates.'''

    # BCRA Endpoint
    default_api_endpoint = 'https://www.bcra.gob.ar/publicacionesestadisticas/Tipo_de_cambio_minorista_2.asp'
    
    # Supported Currencies
    currency_code = {
                     'EUR': '98', 
                     'USD':'2'
                     }

    def __init__(self, start_date = None, end_date = None, date = None, test_file = None 
                 , * ,config_file = None, locator_tag='table', **attributes):    
        self.start_date = start_date
        self.end_date = end_date
        self.date = date 
        self.test_file = test_file
        self.locator_tag = locator_tag
        self.data = self.process_HTML_extraction() 

    def process_HTML_extraction(self) -> Dict[Date, Raw_HTML]:
        '''Get HTML response from configuration, BCRA API or
         local test_file for testing '''
        if self.test_file is not None:
            # Process file
            responses = self.get_from_test_file()
        elif self.test_file is None:
            # Process Dates
            self.date_range = DateProcessor(date=self.date, start_date=self.start_date, end_date=self.end_date).date_range
            responses = self.get_API_rates(self.date_range, self.currency_code) 
        return responses
    
    @classmethod
    def get_API_rates(cls, dates:List[Date], currency_code=None)-> Dict[Date, Raw_HTML]:
        '''GET request to BCRA API for specific list of dates.
        Returns dictionary, dates as keys, raw response as values. '''
        responses = dict()
        for date in dates:
            # `date`: %Y-%m-%d format already for API request and Dict keys
            payload = {'moneda': currency_code, 'fecha': date}
            response = requests.post(cls.default_api_endpoint, data=payload)
            responses = responses.update({date:response.content})
        return responses

    def get_from_test_file(self):
        '''Loads test file as extraction response'''
        try: 
            with open(self.test_file, 'rb') as test_file:
                test_file = test_file.read()
        except FileNotFoundError as e:
            raise e.add_note("Provided Test file Does not Exist")
        date = self.get_date_range()
        test_response =  {date:test_file}
        return test_response
    
    def load_config_file(self, config_path):
        '''Class config file loader'''
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config



 


    
#%% Quickstart - Demo
##################################

if __name__ == '__main__':

    # Extract single date
    single = BCRAExtractor(date='2023-03-01') 
    # Extract date range
    range_ = BCRAExtractor(start_date='2023-02-01', end_date='2023-02-28')
    # extract and filter
    filter_ = BCRAExtractor(date='2023-03-01', locator_tag='table', attr_filter={'id':'tablita'})


