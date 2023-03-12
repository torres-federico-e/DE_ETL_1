# <u>ETL project 1:</u> Financial ETL
The goal of this ETL project is to provide a real-world example of an organized and extensible ETL process that tracks and integrates useful financial metrics from an actual official API source, such as the internal, unexposed API on Argentina's Central Bank web page (BCRA). The project demonstrates the extraction and integration of useful financial data, building time series data from selected sources onto a database for both portfolio purposes and personal use in making financial decisions.

## Objective:
- Extract official USD/ARS exchange rate data from an official government source API and transform; parse, and clean data ready for storage. 
- Integrate and embed it with other financial data sources, such as financial broker API source to include other financial  metrics.  
- Store on local database with possible extension to Cloud storage.

## Project Template 1
```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── intermediate   <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    ├── client.py      <- Any external connection (via API for example) should be written here    
    ├── params.py      <- All parameters of the execution
    ├── pipeline.py    <- The ETL (extract-transform-load) pipeline itself containing the sequence of nodes
    │
    └── nodes          <- Scripts to containing each step of the ETL process.
         ├── data_preparation.py
         ├── data_gathering.py
         ├── data_transform.py
         ├── data_sotrage.py
         └── data_visualization.py
```


## Project Template 2:
```
etl_project/
|-- src/
|   |-- __init__.py
|   |-- data/
|   |   |-- __init__.py
|   |   |-- extract.py
|   |   |-- transform.py
|   |   |-- load.py
|   |-- jobs/
|   |   |-- __init__.py
|   |   |-- job_1.py
|   |   |-- job_2.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- model_1.py
|   |   |-- model_2.py
|   |-- utils/
|   |   |-- __init__.py
|   |   |-- util_1.py
|   |   |-- util_2.py
|-- tests/
|   |-- __init__.py
|   |-- test_extract.py
|   |-- test_transform.py
|   |-- test_load.py
|   |-- test_job_1.py
|   |-- test_job_2.py
|-- requirements.txt
|-- setup.py
|-- README.md
|-- .gitignore
```