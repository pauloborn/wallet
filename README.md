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

This will create the postgres database with the schema finance already created.

## Alembic
To create your data modeling in postgres, install and run alembic, checking if in the config.ini and alembic.ini are updated accordingly with postgres database.
alembic upgrade head

## Python
To tun the application you must be in the project root, with CONFIG_PATH environment set to the same project root, something simples as CONFIG_PATH=. should do the trick.


## Superset visualization
TBD