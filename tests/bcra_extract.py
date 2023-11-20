from src.models.BCRA.bcra_transform import BCRATransformer


# TODO: define final production tests to validate working classes
def test_BCRA_transformer_class():
     # extraction dates
    # ex_1 = BCRAExtractor('2023-02-01', testing_mode=False)
    ex_test = BCRAExtractor('2023-02-01', testing_mode=True)
    
    #TODO: how to make quick Dependency Injection testing object 
    BCRA_data = BCRAExtractor(r'src\data\bcra\data_raw_bcra_api.html')
    
    # visualization result, single date
    BCRA_data.data['2023-02-01']
    
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

    # Example date
    test_file=r'C:\Users\Federico\Desktop\DE_ETL_1\src\data\BCRA\responses\mock_data_raw_1.html'
    
    extractions = BCRAExtractor(test_file=test_file).data

    for date,extraction in extractions.items():
        with open(f'EXTRACTION_{date}.html', 'wb') as file:
            file.write(extractions[date])