import logging

from models.base import Base
from models.BankStatements import BankStatementsModelBase
from models.Investments import InvestmentModelBase

logging.info(f'Loaded and updated all tables metadata')

WalletMetadata = Base.metadata

