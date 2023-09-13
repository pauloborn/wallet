"""Create categories and subcategories

Revision ID: d4914d5efc1e
Revises: ec1d25170069
Create Date: 2023-07-29 19:07:58.026692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, Integer, String, ForeignKey

# revision identifiers, used by Alembic.
revision = 'd4914d5efc1e'
down_revision = '599e5ffeeb68'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.drop_constraint('subcategory_name_key', 'subcategory', type_='unique')

    # Insert the categories and subcategories data
    category_table = sa.table('category',
                              column('id', Integer),
                              column('name', String)
                              )
    op.bulk_insert(
        category_table,
        [
            {'id': 1, 'name': 'Housing'},
            {'id': 2, 'name': 'Food and groceries'},
            {'id': 3, 'name': 'Transportation'},
            {'id': 4, 'name': 'Entertainment'},
            {'id': 5, 'name': 'Travel and Vacation'},
            {'id': 6, 'name': 'Health and Sports'},
            {'id': 7, 'name': 'Education'},
            {'id': 8, 'name': 'Savings and Investments'},
            {'id': 9, 'name': 'Debt Repayment'},
            {'id': 10, 'name': 'Work and Business'},
            {'id': 11, 'name': 'Personal'},
            {'id': 12, 'name': 'Terreiro'},
            {'id': 13, 'name': 'Other'}
        ]
    )

    subcategory_table = sa.table('subcategory',
                                 column('id', Integer),
                                 column('name', String),
                                 column('category_id', Integer)
                                 )
    op.bulk_insert(
    subcategory_table,
    [
        {'name': 'Rent / Mortgage', 'category_id': 1},
        {'name': 'Utilities', 'category_id': 1},
        {'name': 'Home Maintenance', 'category_id': 1},
        {'name': 'Property Taxes', 'category_id': 1},
        {'name': 'Others', 'category_id': 1},
        {'name': 'Groceries', 'category_id': 2},
        {'name': 'Dining Out', 'category_id': 2},
        {'name': 'Snacks and Drinks', 'category_id': 2},
        {'name': 'Others', 'category_id': 2},
        {'name': 'Gasoline / Fuel', 'category_id': 3},
        {'name': 'Public Transportation', 'category_id': 3},
        {'name': 'Vehicle Maintenance', 'category_id': 3},
        {'name': 'Ride - Sharing / Uber', 'category_id': 3},
        {'name': 'Others', 'category_id': 3},
        {'name': 'Movies and Shows', 'category_id': 4},
        {'name': 'Hobbies', 'category_id': 4},
        {'name': 'Subscriptions', 'category_id': 4},
        {'name': 'Events and Tickets', 'category_id': 4},
        {'name': 'Flights', 'category_id': 4},
        {'name': 'Hotels / Accommodation', 'category_id': 5},
        {'name': 'Sightseeing and Tours', 'category_id': 5},
        {'name': 'Souvenirs', 'category_id': 5},
        {'name': 'Others', 'category_id': 5},
        {'name': 'Health Insurance', 'category_id': 6},
        {'name': 'Medical Expenses', 'category_id': 6},
        {'name': 'Tennis', 'category_id': 6},
        {'name': 'Vitamins and Supplements', 'category_id': 6},
        {'name': 'Others', 'category_id': 6},
        {'name': 'Books and Learning Materials', 'category_id': 7},
        {'name': 'Workshops and Courses', 'category_id': 7},
        {'name': 'Others', 'category_id': 7},
        {'name': 'Retirement Savings', 'category_id': 8},
        {'name': 'Investment Contributions', 'category_id': 8},
        {'name': 'Others', 'category_id': 8},
        {'name': 'Credit Card Payments', 'category_id': 9},
        {'name': 'Loan Repayments', 'category_id': 9},
        {'name': 'Consórcio', 'category_id': 9},
        {'name': 'Others', 'category_id': 9},
        {'name': 'Business Expenses', 'category_id': 10},
        {'name': 'Work-Related Costs', 'category_id': 10},
        {'name': 'Others', 'category_id': 10},
        {'name': 'Clothes', 'category_id': 11},
        {'name': 'Building tools', 'category_id': 11},
        {'name': 'Others', 'category_id': 11},
        {'name': 'Candles', 'category_id': 12},
        {'name': 'Guias & itens de toco', 'category_id': 12},
        {'name': 'Donations', 'category_id': 12},
        {'name': 'Others', 'category_id': 12},
        {'name': 'Others', 'category_id': 13}
    ]
)


def downgrade() -> None:
    op.execute("DELETE FROM subcategory")
    op.execute("DELETE FROM category")
