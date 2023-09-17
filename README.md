# Wallet 

This project aims to automatize my bank statements from Nubank, Itau and XP, considering expenses from cards and accounts transactions that must be seen in the same database.
The same is for investments, but only XP is implemented. Due to lack of open APIs, I depend on report files to be uploaded to the file system.
If you want to use, include your files in the data folder, with specific starting names:

Itau bank statement: "Extrato Conta Corrente-%.txt" \
Nubank bank statement: "NU_%.csv" \
Nubank card statement: "nubank-%.csv" \
XP card statement: "Fatura XP%.csv" \
XP investments rentability: "PosicaoDetalhada_%.xlsx" \

This project needs a postgres version 15 to work and you can use the dockerfile provided to setup.
For setup, use the steps described below.

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
All the database I used superset to create my finance view, but you can use any BI visualization tools.