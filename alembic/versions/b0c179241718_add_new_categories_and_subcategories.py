"""Add new categories and subcategories

Revision ID: b0c179241718
Revises: 4b041af532ae
Create Date: 2023-09-12 22:23:12.998334

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer, String, insert, delete


# revision identifiers, used by Alembic.
revision = 'b0c179241718'
down_revision = '4b041af532ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Define the categories table object
    categories = table('category',
                       column('id', Integer),
                       column('name', String)
                       )
    # Insert the "Income" category and fetch its ID
    op.execute(insert(categories).values(id=14, name='Income'))
    income_category_id = 14

    # Define the subcategories table object
    subcategories = table('subcategory',
                          column('id', Integer),
                          column('name', String),
                          column('category_id', Integer)
                          )

    # Insert the subcategories linked with "Income" category
    op.bulk_insert(subcategories,
                   [{'name': 'Dividends', 'category_id': income_category_id},
                    {'name': 'Revenue', 'category_id': income_category_id},
                    {'name': 'CLT', 'category_id': income_category_id},
                    {'name': 'Others', 'category_id': income_category_id}]
                   )


def downgrade() -> None:
    subcategories = table('subcategory',
                          column('id', Integer),
                          column('name', String),
                          column('category_id', Integer)
                          )

    categories = table('category',
                       column('id', Integer),
                       column('name', String)
                       )

    op.execute(delete(subcategories).where(subcategories.c.category_id == 14))
    op.execute(delete(categories).where(categories.c.id == 14))
