"""Implementing XP investments

Revision ID: 4b041af532ae
Revises: d7835005f4ae
Create Date: 2023-08-11 23:54:30.509983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b041af532ae'
down_revision = 'd7835005f4ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('investment', sa.Column('sell_date', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('investment', 'sell_date')
