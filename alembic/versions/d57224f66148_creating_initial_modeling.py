"""Creating initial modeling

Revision ID: d57224f66148
Revises: 
Create Date: 2023-08-06 18:48:39.969318

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd57224f66148'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='finance'
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='finance'
    )
    op.create_table('processed_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('lines_loaded', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('filename'),
    schema='finance'
    )
    op.create_table('investment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', postgresql.ENUM('TESOURO_DIRETO', 'RENDA_FIXA', 'FUNDOS_IMOBILIARIOS', 'COMPROMISSADAS', 'PREVIDENCIA_PRIVADA', 'FUNDOS_DE_INVESTIMENTO', 'COE', 'ACOES', 'UNDEFINED', name='investmenttype'), nullable=False),
    sa.Column('purchase_date', sa.Date(), nullable=False),
    sa.Column('purchase_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank_id'], ['finance.bank.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='finance'
    )
    op.create_table('subcategory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['finance.category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='finance'
    )
    op.create_table('bank_statement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('method', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('subcategory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['finance.bank.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['finance.category.id'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['finance.subcategory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='finance'
    )
    op.create_table('category_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('statement_name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['finance.category.id'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['finance.subcategory.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('statement_name'),
    schema='finance'
    )
    op.create_table('investment_rentability',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('investment_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('position', sa.Float(), nullable=False),
    sa.Column('rentability_percentage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['investment_id'], ['finance.investment.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='finance'
    )
    op.create_table('investment_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('investment_id', sa.Integer(), nullable=True),
    sa.Column('transaction_date', sa.Date(), nullable=False),
    sa.Column('transaction_type', sa.String(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('bankstatement_id', sa.Integer(), nullable=True),
    sa.Column('selling', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['bankstatement_id'], ['finance.bank_statement.id'], ),
    sa.ForeignKeyConstraint(['investment_id'], ['finance.investment.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='finance'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investment_transaction', schema='finance')
    op.drop_table('investment_rentability', schema='finance')
    op.drop_table('category_map', schema='finance')
    op.drop_table('bank_statement', schema='finance')
    op.drop_table('subcategory', schema='finance')
    op.drop_table('investment', schema='finance')
    op.drop_table('processed_file', schema='finance')
    op.drop_table('category', schema='finance')
    op.drop_table('bank', schema='finance')
    # ### end Alembic commands ###
