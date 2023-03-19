# <u>ETL project 1:</u> Financial ETL
Example of an extensible ETL process with Real-world data recollection. This process extracts and integrates data from the official backend API of Argentina's Central Bank institution (BCRA), an unexposed API source allowing easy collection and access of otherwise unaccessible data. The project demonstrates the extraction and integration of useful data from diverse financial sources into a valid schema and posterior storage into a database system.

## Objective:
- Extract official exchange rate data from an official backend government API for ARS/USD. 
- Transform, parse, and clean data, makint it ready for storage. 
- Integrate and embed it with other financial data sources form brokers, into a coherent dataset and schema.
- Loading data onto persistence layer, a local database (with possible future extension to Cloud storage).  

## Nice Features
- Extraction from unexposed API: The project leverages a real-world API from the BCRA National reporting website for data extraction. This allows access to data that is not publicly available through other means.  

- Rich HTML extraction: Use of Python Multi-level Hierarchical Dataframes and custom extraction classes to easily extract raw HTML data from official BCRA website API. This also allows easy psoterior data manipulation and organization, supporting reusability by other team-members (abstracting complex complex table data parsing and supporting `stack()` and `unstack()` methods for data simplicity).

- Data transformation: The extracted data is transformed into appropriate schema data types using Pydantic. This helps to enforce data integrity and ensure that the data is usable for downstream processing.The extracted data is also cleaned and formatted for further processing.  

- Extensible design: The project is designed to be extensible, with support for multiple sources and classes. This allows for easy integration of new data sources and data types as needed.  

- Custom exceptions and error messages: Custom exception and descriptive error messages, making it easier for developers to collaborate and reuse code. This helps to improve code quality and reduce development time.




<br><br>
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