
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
class DateRequest:
    '''Date Processor: handles date request interpretation, validation and parsing, and processes calendar date range'''

    def __init__(self, *, start_date=None, end_date=None, date=None):
        # validation checks
        self._is_valid_date(start_date, end_date, date)
        self._is_valid_request(start_date, end_date, date)

        # definitions
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.range = self.get_calendar_range_list(
            start_date=self.start_date
            , end_date=self.end_date
            , date=self.date)
    
    def _is_valid_request(self, start_date = None, end_date = None, date = None, ):
        '''Checks for consistent date request mode. Single date or date range, but not both'''
        if (date and (start_date or end_date )):
            raise InvalidDateRequestError
        else: 
            pass
            
    def _is_valid_date(self, start_date = None, end_date = None, date = None, datefmt='%Y-%m-%d') -> bool:
        '''Checks for valid string format.'''
        try:
            for dt in [date, start_date, end_date]:
                if dt is not None:
                    datetime.strptime(dt, datefmt)
        except ValueError:
            raise InvalidDateFormatError
        
    @staticmethod
    def get_calendar_range_list(start_date=None, end_date=None, date=None) -> List[Date]:
        '''Exports calendar list for a valid Date Range request.
        If single date mode is passed, overrides date range calculation.
        String date format is 'YYYY-MM-DD' BCRA API compatible '''

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
    currency_dict = {
                     'EUR': '98', 
                     'USD':'2'
                     }

    def __init__(self, date = None, start_date = None, end_date = None, currency= 'USD',
                 locator_tag='table', test_file = None , * ,config_file = None, **attributes):    
        self.currency = currency
        self.date_range = None
        self.start_date = start_date
        self.end_date = end_date
        self.date = date
        self.test_file = test_file
        self.locator_tag = locator_tag
        self.data = self.get_HTML_extraction() 

    def get_HTML_extraction(self) -> Dict[Date, Raw_HTML]:
        '''Get HTML response from configuration, BCRA API or
         local test_file for testing '''
        if self.test_file is not None:
            # Process file
            responses = self.get_from_test_file()
        elif self.test_file is None:
            # Process Dates
            self.date_range = DateRequest(start_date = self.start_date, 
                                            end_date = self.end_date, 
                                            date = self.date).range
            responses = self.get_API_rates(self.date_range, self.currency) 
        return responses
    
    @classmethod
    def get_API_rates(cls, dates:List[Date], currency_code='USD')-> Dict[Date, Raw_HTML]:
        '''Makes requests to BCRA API extracting currency data for dates.
        Returns dictionary, dates as keys, raw response as values. '''
        result = dict()
        for date in dates:
            # `date`: %Y-%m-%d format already for API request and Dict keys
            payload = {'moneda': cls.currency_dict[currency_code], 'fecha': date}
            response = requests.post(cls.default_api_endpoint, data=payload)
            result.update({date:response.content})
        return result

    def get_from_test_file(self):
        '''Loads default test extraction from local file'''
        try: 
            with open(self.test_file, 'rb') as test_file:
                test_file = test_file.read()
        except FileNotFoundError as e:
            raise e.add_note("Provided Test file Does not Exist")
        default_date = DateRequest().get_calendar_date_range_list()[0] 
        test_response =  {default_date:test_file}
        return test_response
    
    def load_config_file(self, config_file):
        '''Class config file loader'''
        with open(config_file) as f:
            config = yaml.safe_load(f)
        return config



 


    

if __name__ == '__main__':

    # Quickstart - Demo
    #---------------------------------------------
    # Extract single date
    single = BCRAExtractor(date='2023-03-01') 
    
    # Extract date range
    range_ = BCRAExtractor(start_date='2023-02-01', end_date='2023-02-28')
    
    # Extract and filter by attribute
    filter_ = BCRAExtractor(date='2023-03-01', locator_tag='table', attr_filter={'id':'tablita'})


