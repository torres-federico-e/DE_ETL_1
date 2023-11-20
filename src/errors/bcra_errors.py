
#%% Exceptions definitions


class InvalidDateRequestError(Exception):
    def __str__(self):
        return '''Choose either a Date Range or a Single date for the request with  `start_date`, `end_date`, or `date` parameters.'''

class InvalidDateFormatError(Exception):
    def __str__(self):
        return '''Invalid date format for API request. Please use valid (ISO8601) 'YYYY-MM-DD' format dates.'''

