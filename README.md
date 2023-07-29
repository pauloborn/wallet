# wallet

## Project structure
````bash
wallet
|--- main.py 
|--- wallet.py
|--- data
|    |--- bank_statements
|    |--- investments
|--- contextualization
|    |-- __init__.py
|    |-- BankDataMerging.py
|    |   |-- NubankDataMerging.py
|    |   |-- ItauDataMerging.py
|    |   |-- XPDataMerging.py
|    |-- contextualization.py
|    |-- InvestmentsMerging.py
|    |   |-- XPInvestmentsMerging.py
|    |   |-- NUInvestmentsMerging.py
|    |   |-- ItauInvestmentsMerging.py
|--- alembic
|--- config
|--- requirements.txt
|--- README.md
|--- alembic.ini
|--- Dockerfile

````

# How to run
## Creating the docker container
docker build -t wallet . \
docker run -p 5432:5432 -e CONFIG_PATH=/app/config wallet

## Alembic
alembic upgrade head

## Python
TBD

## Superset visualization
TBD