"""Insert banks models

Revision ID: 599e5ffeeb68
Revises: 109523718053
Create Date: 2023-07-29 17:59:08.353922

"""
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import insert
from alembic import op

from models.BankStatements import Bank

# revision identifiers, used by Alembic.
revision = '599e5ffeeb68'
down_revision = 'd57224f66148'
branch_labels = None
depends_on = None

bank_table = Table(
    'bank',
    Bank.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    extend_existing=True
)


def upgrade() -> None:
    # Insert initial data into the 'bank' table
    bank_data = [
        {'name': 'Nubank'},
        {'name': 'Itau'},
        {'name': 'XP'},
    ]
    op.bulk_insert(bank_table, bank_data)


def downgrade() -> None:
    # Delete the inserted data from the 'bank' table during rollback (downgrade)
    op.execute(
        "DELETE FROM finance.bank WHERE name in ('Nubank', 'Itau', 'XP')"
    )
