from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base import Base, engine

ModelBase = Base


# Define the Banks table
class Bank(ModelBase):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    # Add more fields if needed


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)


class Subcategory(Base):
    __tablename__ = 'subcategory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


# Define the CategoryMap table
class CategoryMap(Base):
    __tablename__ = 'category_map'
    id = Column(Integer, primary_key=True)
    statement_name = Column(String, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'), nullable=False)


# Define the BankStatements table
class BankStatement(ModelBase):
    __tablename__ = 'bank_statements'

    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(String, nullable=False)

    # Add foreign keys to the Category and SubCategory tables
    category_id = Column(Integer, ForeignKey('category.id'))
    subcategory_id = Column(Integer, ForeignKey('subcategory.id'))

    # Establish relationships between BankStatement, Category, and StatementCategory
    category = relationship('Category', backref='bank_statements')
    subcategory = relationship('Subcategory', backref='bank_statements')


# Define the Investments table
class Investment(ModelBase):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    quantity = Column(Numeric, nullable=False)
    purchase_date = Column(Date, nullable=False)
    purchase_price = Column(Numeric, nullable=False)


# Define the InvestmentUpdates table
class InvestmentUpdate(ModelBase):
    __tablename__ = 'investment_updates'

    id = Column(Integer, primary_key=True)
    investment_id = Column(Integer, ForeignKey('investments.id'), nullable=False)
    update_date = Column(Date, nullable=False)
    value = Column(Numeric, nullable=False)


class ProcessedFiles(ModelBase):
    __tablename__ = 'processed_files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), unique=True, nullable=False)
    started_at = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    end_time = Column(DateTime, nullable=True)
    lines_loaded = Column(Integer, nullable=False)


# Create the tables in the models
Base.metadata.create_all(engine)
