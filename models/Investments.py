from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from models.base import Base, engine
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
    UNDEFINED = 'Undefined'


class Investment(InvestmentModelBase):
    __tablename__ = 'investment'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    type = Column(ENUM(InvestmentType), nullable=False)
    purchase_date = Column(Date)
    purchase_price = Column(Float, nullable=False)
    sell_date = Column(Date), # TODO Implement when it recons that is was sold
    quantity = Column(Integer, nullable=False)
    due_date = Column(Date)  # For TesouroDireto, RendaFixa, Compromissadas, and COE

    bank_id = Column(Integer, ForeignKey('bank.id'), nullable=False)


class InvestmentRentability(InvestmentModelBase):
    __tablename__ = 'investment_rentability'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investment.id'))
    date = Column(Date, nullable=False)
    position = Column(Float, nullable=False)  # Rentability value
    rentability = Column(Float, nullable=False)  # Rentability in %Percentage
    rentability_value = Column(Float, nullable=False)  # Rentability value in $

    # Relationship with Investment model
    investment = relationship('Investment', back_populates='rentability')


class InvestmentTransaction(InvestmentModelBase):
    __tablename__ = 'investment_transaction'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investment.id'))
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationship with Investment model
    investment = relationship('Investment', back_populates='transaction')

    bankstatement_id = Column(Integer, ForeignKey('bank_statement.id'))
    selling = Column(Boolean, nullable=False)

    # Relationship with BankStatement model
    bankstatement = relationship('BankStatement', back_populates='transaction')

# Create the tables in the models
# InvestmentModelBase.metadata.create_all(engine)
