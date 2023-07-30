from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base, engine

InvestmentModelBase = Base


class Investment(InvestmentModelBase):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    purchase_date = Column(Date, nullable=False)
    purchase_price = Column(Float, nullable=False)

    # Relationship with InvestmentTransaction model
    transactions = relationship('InvestmentTransaction', back_populates='investment')


class InvestmentTransaction(InvestmentModelBase):
    __tablename__ = 'investment_transactions'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investments.id'), nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    # Relationship with Investment model
    investment = relationship('Investment', back_populates='transactions')


class InvestmentPortfolio(InvestmentModelBase):
    __tablename__ = 'investment_portfolio'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investments.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)

    # Relationship with Investment model
    investment = relationship('Investment')


class InvestmentRentability(InvestmentModelBase):
    __tablename__ = 'investment_rentability'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investments.id'), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    rentability_percentage = Column(Float, nullable=False)

    # Relationship with Investment model
    investment = relationship('Investment')


# Create the tables in the models
InvestmentModelBase.metadata.create_all(engine)
