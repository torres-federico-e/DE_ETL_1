from src.models.BCRA import BCRATransformer



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