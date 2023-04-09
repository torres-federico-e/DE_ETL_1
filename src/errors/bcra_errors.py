
#%% Exceptions definitions


class InvalidDateRequestError(Exception):
    def __str__(self):
        return '''Inconsistent date extraction request. 
Please choose either a Single date request, or a Date Range request using `start_date` and `end_date`.'''

class InvalidDateFormatError(Exception):
    def __str__(self):
        return '''Invalid date format for API request.
Please use valid 'YYYY-MM-DD' (ISO8601) format dates.'''

