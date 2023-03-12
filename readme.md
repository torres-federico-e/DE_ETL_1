# ETL project 1: Financial ETL
This ETL project serves as a real-world example of an actual ETL that tracks useful financial metrics from an unstructured source, such as an internal, unexposed API from Argentina's Central Bank (BCRA). The goal is to demonstrate the extraction and integration of useful financial metrics and data, as both a portfolio project and for personal use in making financial decisions.

## Objective:
- Extract official USD/ARS exchange rate data from an official government source API and transform; parse, and clean data ready for storage. 
- Integrate and embed it with other financial data sources, such as financial broker API source to include other financial  metrics.  
- Store on local database with possible extension to Cloud storage.

## Project structure
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