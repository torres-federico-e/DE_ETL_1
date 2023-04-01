
#%% Exceptions definitions


class DateRequestError(Exception):
    '''Date Request method Error'''
    def __str__(self):
        return "Inconsistent date extraction request specified. Please choose a Single date request, or a Date Range request via Start_Date and End_Date."

