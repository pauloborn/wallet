"""Creating properly columns

Revision ID: 4da80646306d
Revises: ec1d25170069
Create Date: 2023-07-29 20:39:03.541988

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey

# revision identifiers, used by Alembic.
revision = '4da80646306d'
down_revision = 'ec1d25170069'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('bank_statements', Column('subcategory_id', Integer, ForeignKey('subcategory.id')))


def downgrade() -> None:
    op.drop_column('bank_statements', 'subcategory_id')
