

# Standard
import os
from datetime import datetime, timedelta
from typing import List, Dict

# Modules
import requests
from bs4 import BeautifulSoup
import yaml
import pandas as pd

# Internal
from src.models.BCRA.bcra_extract import BCRAExtractor
from src.errors.bcra_errors import InvalidDateRequestError, InvalidDateFormatError

# Type definitions
Response= str
Date = str
Raw_HTML = str
Raw_HTML_Responses = Dict[Date, Raw_HTML]
Parsed_HTML_tables = Dict[Date, BeautifulSoup]



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

