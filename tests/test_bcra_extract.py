from src.models.BCRA.bcra_transform import BCRATransformer
from src.models.BCRA.bcra_extract import BCRAExtractor

def test_static_test_file():
    test_file=r'C:\Users\Federico\Desktop\DE_ETL_1\src\data\BCRA\responses\mock_data_raw_1.html'
    raw_extraction = BCRAExtractor(file_path=test_file).result
    assert type(raw_extraction) == dict


def test_singe_date_extraction(date):
    result = BCRAExtractor(date=date).result
    assert '<title>Request Rejected</title>' not in str(result[date])


if __name__ == '__main__':  
    date = input("Date to extract (YYYY-MM-DD):")
    result = test_singe_date_extraction(date=date)
    print(result[date])