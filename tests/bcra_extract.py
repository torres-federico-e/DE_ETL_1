from src.models.BCRA import BCRATransformer


# TODO: define final production tests to validate working classes
def test_BCRA_transformer_class():
     # extraction dates
    # ex_1 = BCRAExtractor('2023-02-01', testing_mode=False)
    ex_test = BCRAExtractor('2023-02-01', testing_mode=True)
    
    #TODO: how to make quick Dependency Injection testing object 
    BCRA_data = BCRAExtractor(r'src\data\bcra\data_raw_bcra_api.html')
    
    # visualization result, single date
    BCRA_data.raw_html['2023-02-01']
    
    # transformation raw to parsed
    br = BCRATransformer(BCRA_data)


# TODO: define final production tests to validate working classes
def test_BCRA_extractor_class():
     # extraction dates
    # ex_1 = BCRAExtractor('2023-02-01', testing_mode=False)
    ex_test = BCRAExtractor('2023-02-01', testing_mode=True)
    
    #TODO: how to make quick Dependency Injection testing object 
    # BCRA_data = BCRAExtractor(r'src\data\bcra\data_raw_bcra_api.html')
    
    # # visualization result, single date
    # BCRA_data.raw_html['2023-02-01']
    
    # transformation raw to parsed
    # br = BCRATransformer(BCRA_data)







from src.models.BCRA.bcra_extract import BCRAExtractor

if __name__ == '__main__':
    date = '20230301'
    # TODO: opening test_file raises DateError
    # Need to make available test_file only load into datevalidation logic
    response = BCRAExtractor(test_file=r'C:\Users\Federico\Desktop\DE_ETL_1\src\data\BCRA\responses\mock_data_raw_1.html')
    print(response)
    
    export_name = f'EXTRACTION.html'
    with open(export_name, 'wb') as file:
        file.write(response[date])