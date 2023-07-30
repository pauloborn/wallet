import pandas as pd
import datetime
from sqlalchemy.orm import Session

from models.Investments import Investment, InvestmentTransaction


class XPInvestmentDataMerging:
    def __init__(self):
        self.category_map = None

    # ... (other methods remain the same)

    def process_investment_transactions(self, excel_file_path, session: Session):
        df = pd.read_csv(excel_file_path, encoding='utf-8', skiprows=1, header=None)

        for _, row in df.iterrows():
            if len(row) >= 5:
                date_str = row[0]
                liquidation_date_str = row[1]
                description = row[2]
                value_str = row[3]
                balance_str = row[4]

                date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
                liquidation_date = datetime.datetime.strptime(liquidation_date_str, '%d/%m/%Y').date()
                value = float(value_str.replace(',', '.'))
                balance = float(balance_str.replace(',', '.'))

                # Check if the investment already exists
                investment = session.query(Investment).filter_by(description=description).first()

                if not investment:
                    # If the investment doesn't exist, create it
                    investment = Investment(description=description)
                    session.add(investment)

                # Create an InvestmentTransaction
                investment_transaction = InvestmentTransaction(
                    investment_id=investment.id,
                    date=date,
                    liquidation_date=liquidation_date,
                    value=value,
                    balance=balance
                )
                session.add(investment_transaction)

                # Update InvestmentPortfolio
                self.update_investment_portfolio(investment, date, balance, session)

        session.commit()

    def update_investment_portfolio(self, investment, date, balance, session: Session):
        # Check if InvestmentPortfolio entry already exists for the given date and investment
        investment_portfolio = session.query(InvestmentPortfolio).filter_by(
            investment_id=investment.id,
            date=date
        ).first()

        if investment_portfolio:
            # If the entry already exists, update the balance if it's newer than the existing one
            if date > investment_portfolio.date:
                investment_portfolio.balance = balance
        else:
            # If the entry doesn't exist, create a new one
            investment_portfolio = InvestmentPortfolio(
                investment_id=investment.id,
                date=date,
                balance=balance
            )
            session.add(investment_portfolio)

    def process_investment_patrimony_position(self, excel_file_path, session: Session):
        df = pd.read_csv(excel_file_path, encoding='utf-8', skiprows=15, header=None)
        df.dropna(axis=1, how='all', inplace=True)

        for _, row in df.iterrows():
            if len(row) >= 2:
                description = row[0]
                value_str = row[1]

                value = float(value_str.replace(',', '.'))

                # Check if the investment already exists
                investment = session.query(Investment).filter_by(description=description).first()

                if not investment:
                    # If the investment doesn't exist, create it
                    investment = Investment(description=description)
                    session.add(investment)

                # Calculate and update InvestmentRentability
                self.update_investment_rentability(investment, value, session)

        session.commit()

    def update_investment_rentability(self, investment, current_value, session: Session):
        # Calculate rentability based on the current value and past value (replace with actual calculation)
        rentability = 0.05  # 5% for illustration purposes

        # Create an InvestmentRentability entry
        investment_rentability = InvestmentRentability(
            investment_id=investment.id,
            rentability=rentability
        )
        session.add(investment_rentability)
