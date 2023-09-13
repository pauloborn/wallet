from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, mapped_column
from models.base import Base
from enum import Enum

InvestmentModelBase = Base


class InvestmentType(Enum):
    TESOURO_DIRETO = 'Tesouro Direto'
    RENDA_FIXA = 'Renda Fixa'
    FUNDOS_IMOBILIARIOS = 'Fundos Imobiliários'
    COMPROMISSADAS = 'Compromissadas'
    PREVIDENCIA_PRIVADA = 'Previdência Privada'
    FUNDOS_DE_INVESTIMENTO = 'Fundos de Investimentos'
    COE = 'COE'
    ACOES = 'Ações'
    UNDEFINED = 'Undefined'


class Investment(InvestmentModelBase):
    __tablename__ = 'investment'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    type = Column(ENUM(InvestmentType), nullable=False)
    purchase_date = Column(Date)
    purchase_price = Column(Float, nullable=False)
    sell_date = Column(Date)
    quantity = Column(Integer, nullable=False)
    due_date = Column(Date)  # For TesouroDireto, RendaFixa, Compromissadas, and COE

    bank_id = mapped_column(ForeignKey('bank.id'), nullable=False)

    bank = relationship('Bank', back_populates='investment')
    investment_rentability = relationship('InvestmentRentability', back_populates='investment')
    investment_transaction = relationship('InvestmentTransaction', back_populates='investment')


class InvestmentRentability(InvestmentModelBase):
    __tablename__ = 'investment_rentability'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investment.id'))
    date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    position = Column(Float, nullable=False)  # Rentability value
    rentability = Column(Float)  # Rentability in %Percentage
    rentability_value = Column(Float)  # Rentability value in $

    # Relationship with Investment model
    investment = relationship('Investment', back_populates='investment_rentability')

    def __init__(self, investment, date, position, rentability, rentability_value):
        self.investment = investment
        self.date = date
        self.month = date.month
        self.year = date.year
        self.position = position
        self.rentability = rentability
        self.rentability_value = rentability_value


class InvestmentTransaction(InvestmentModelBase):
    __tablename__ = 'investment_transaction'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investment.id'))
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationship with Investment model
    investment = relationship('Investment', back_populates='investment_transaction')

    bankstatement_id = Column(Integer, ForeignKey('bank_statement.id'))
    selling = Column(Boolean, nullable=False)

    # Relationship with BankStatement model
    bank_statement = relationship('BankStatement', back_populates='investment_transaction')

# Create the tables in the models
# InvestmentModelBase.metadata.create_all(engine)
