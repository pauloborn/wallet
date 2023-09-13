from lazyutils.structure.Singleton import Singleton
from sqlalchemy import text
from models.Investments import InvestmentType, Investment, InvestmentRentability


def investmenttype_map():
    """
    Function that converts InvestmentType to a dict to facilitate the readability of the code
    :return: A category map like: {'Tesouro Direto': InvestmentType.TESOURO_DIRETO}
    """

    category_map = {}

    for category in InvestmentType:
        category_map[category.value] = category

    return category_map


def update_retability(session):
    query = """

        with new_investment_rentability as (
            select
                ir.id,
                ir.investment_id, 
                ir."date", 
                ir."position",
                ir.rentability, 
                ir.rentability_value, 
                lag(ir."position", 1) OVER (PARTITION BY ir.investment_id ORDER BY ir.date ASC) as "position_before"
            from finance.investment_rentability ir
        )
        update finance.investment_rentability 
        set 
            "rentability_value" = investment_rentability."position" - new_investment_rentability."position_before",
            "rentability" = 
                (investment_rentability."position" - new_investment_rentability."position_before") 
                / new_investment_rentability."position_before"
        from new_investment_rentability
        where 
            new_investment_rentability.position_before is not null
            and investment_rentability.id = new_investment_rentability.id

    """

    session.execute(text(query))


class InvestmentsFactory(Singleton):
    added_investments = {}
    added_rentabilities = set()

    @staticmethod
    def create_key(investment: Investment, investment_rentability: InvestmentRentability):
        investment_key = (investment.bank_id, investment.name, investment.type)
        rentability_key = investment_key + (investment_rentability.date,)

        return investment_key, rentability_key

    def process_investment(self, investment: Investment, investment_rentability: InvestmentRentability,
                           investment_key, session):
        if investment_key not in self.added_investments:

            # Check if investment already exists in the models
            existing_investment = session.query(Investment).filter_by(
                name=investment.name, type=investment.type
            ).first()

            if not existing_investment:
                session.add(investment)
                self.added_investments[investment_key] = investment  # store the Investment object

            else:
                existing_investment.purchase_price = investment.purchase_price
                existing_investment.quantity = investment.quantity
                investment_rentability.investment = existing_investment
                investment = existing_investment
                self.added_investments[investment_key] = existing_investment

        else:
            investment = self.added_investments[investment_key]
            investment_rentability.investment = self.added_investments[investment_key]

        return investment, investment_rentability

    def process_investment_rentability(self, investment: Investment, investment_rentability: InvestmentRentability,
                                       rentability_key, session):
        if rentability_key not in self.added_rentabilities:
            existing_investmentrentability = session.query(InvestmentRentability).filter_by(
                investment_id=investment.id, date=investment_rentability.date.strftime('%Y-%m-%d')
            ).first()

            if existing_investmentrentability:
                existing_investmentrentability.rentability = investment_rentability.rentability
                existing_investmentrentability.rentability_value = investment_rentability.rentability_value
            else:
                session.add(investment_rentability)
                self.added_rentabilities.add(rentability_key)  # mark this rentability as added
