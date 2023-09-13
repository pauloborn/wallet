"""Implementing XP investments

Revision ID: d7835005f4ae
Revises: ec1d25170069
Create Date: 2023-08-11 22:58:03.125642

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd7835005f4ae'
down_revision = 'ec1d25170069'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('investment', 'purchase_date',
                    existing_type=sa.DATE(),
                    nullable=True)
    op.drop_column('investment', 'total_amount')
    op.add_column('investment_rentability', sa.Column('year', sa.Integer(), nullable=False))
    op.add_column('investment_rentability', sa.Column('month', sa.Integer(), nullable=False))
    op.add_column('investment_rentability', sa.Column('rentability', sa.Float()))
    op.add_column('investment_rentability', sa.Column('rentability_value', sa.Float()))
    op.drop_column('investment_rentability', 'rentability_percentage')


def downgrade() -> None:
    op.add_column('investment_rentability',
                  sa.Column('rentability_percentage', sa.DOUBLE_PRECISION(precision=53), autoincrement=False,
                            nullable=False))
    op.drop_column('investment_rentability', 'rentability_value')
    op.drop_column('investment_rentability', 'rentability')
    op.drop_column('investment_rentability', 'month')
    op.drop_column('investment_rentability', 'year')
    op.add_column('investment',
                  sa.Column('total_amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.alter_column('investment', 'purchase_date',
                    existing_type=sa.DATE(),
                    nullable=False)
