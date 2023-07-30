"""Include column method on class bank_statement

Revision ID: cda144881e95
Revises: 4da80646306d
Create Date: 2023-07-30 00:22:22.145011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cda144881e95'
down_revision = '4da80646306d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE finance.bank_statements ADD COLUMN method VARCHAR NOT NULL DEFAULT 'Account'")


def downgrade() -> None:
    op.drop_column('bank_statements', 'method')
