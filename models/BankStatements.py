from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base import Base, engine

BankStatementsModelBase = Base


# Define the Banks table
class Bank(BankStatementsModelBase):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    # Add more fields if needed


class Category(BankStatementsModelBase):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)


class Subcategory(BankStatementsModelBase):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


# Define the CategoryMap table
class CategoryMap(BankStatementsModelBase):
    __tablename__ = 'category_map'
    id = Column(Integer, primary_key=True)
    statement_name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'), nullable=False)


# Define the BankStatements table
class BankStatement(BankStatementsModelBase):
    __tablename__ = 'bank_statement'

    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('bank.id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String, nullable=False)
    method = Column(String, default='Account', nullable=False)

    # Add foreign keys to the Category and SubCategory tables
    category_id = Column(Integer, ForeignKey('category.id'))
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'))

    # Establish relationships between BankStatement, Category, and StatementCategory
    category = relationship('Category', backref='bank_statement')
    subcategory = relationship('Subcategory', backref='bank_statement')


class ProcessedFiles(BankStatementsModelBase):
    __tablename__ = 'processed_file'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), unique=True, nullable=False)
    started_at = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    end_time = Column(DateTime, nullable=True)
    lines_loaded = Column(Integer, nullable=False)


# Create the tables in the models
# Base.metadata.create_all(engine)
