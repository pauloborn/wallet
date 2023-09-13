from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.BankStatements import CategoryMap, Category, Subcategory, BankStatement
import models.Investments
from models.base import engine

category_map = {
    "*OPERAÇÕES EM BOLSA*": ["Savings and Investments", "Investment Contributions"],
    "COMPRA *": ["Savings and Investments", "Investment Contributions"],
    "APLICAÇÃO COMPROMISSADA*": ["Savings and Investments", "Investment Contributions"],
    "OPERAÇÕES EM BOLSA*": ["Savings and Investments", "Investment Contributions"],
    "Pagamento recebido*": ["Debt Repayment", "Credit Card Payments"],

    "*Cartão Nubank*": ["Debt Repayment", "Credit Card Payments"],
    "*Ana Claudia Condeixa De França*": ["Health and Sports", "Tennis"],
    "*Anaclaudiacondeix*": ["Health and Sports", "Tennis"],
    "*GPS*": ["Work and Business", 'Business Expenses'],
    "*DAS - Simples Nacional*": ["Work and Business", 'Business Expenses'],
    "*Ifd*Br": ["Food and groceries", "Groceries"],
    "*DETRAN*": ["Transportation", "Others"],
    "*JURANDIR*": ["Housing", "Utilities"],
    "*LIGGA*": ["Housing", "Utilities"],
    "*SECRETARIA DA RECEITA FEDERAL*": ["Work and Business", 'Business Expenses'],
    "*INSIDER*": ["Personal", "Clothes"],
    "*CONTABILIZEI*": ["Work and Business", 'Business Expenses'],
    "*Pagamento de fatura*": ["Debt Repayment", "Credit Card Payments"],
    "*AUTO POSTO*": ["Transportation", "Gasoline / Fuel"],
    "*Autoposto*": ["Transportation", "Gasoline / Fuel"],
    "*posto*": ["Transportation", "Gasoline / Fuel"],
    "*Petro*": ["Transportation", "Gasoline / Fuel"],
    "*PERRETTO VIAGENS*": ["Travel and Vacation", "Flights"],
    "*DIGISEC*": ["Work and Business", "Business Expenses"],
    "*NETSHOES*": ["Personal", "Clothes"],
    "*Best Park*": ["Transportation", "Others"],
    "*REK PARKING*": ["Transportation", "Others"],
    "*Estaciona*": ["Transportation", "Others"],
    "*park*": ["Transportation", "Others"],
    "*SANTANDER SX VISA*": ["Debt Repayment", "Credit Card Payments"],
    "*ITAUCARD*": ["Debt Repayment", "Credit Card Payments"],
    "*TONICO MATERIAIS*": ["Terreiro", "Others"],
    "*Bar*": ["Food and groceries", "Dining Out"],
    "*pizza*": ["Food and groceries", "Groceries"],
    "*restaurante*": ["Food and groceries", "Groceries"],
    "*Ifood*": ["Food and groceries", "Groceries"],
    "*Mercado*": ["Food and groceries", "Groceries"],
    "*Lanchonete*": ["Food and groceries", "Groceries"],
    "*Paes*": ["Food and groceries", "Groceries"],
    "*Madero*": ["Food and groceries", "Groceries"],
    "*Hamd*": ["Food and groceries", "Groceries"],
    "*The Coffee*": ["Food and groceries", "Groceries"],
    "*Supermercado*": ["Food and groceries", "Groceries"],
    "*Festval*": ["Food and groceries", "Groceries"],
    "*Mikilas*": ["Food and groceries", "Groceries"],
    "*Food*": ["Food and groceries", "Groceries"],
    "*Sisignore*": ["Food and groceries", "Groceries"],
    "*Gol*": ["Travel and Vacation", "Flights"],
    "*British*": ["Travel and Vacation", "Flights"],
    "*Airbnb*": ["Travel and Vacation", "Hotels / Accommodation"],
    "*Miro.Com*": ["Work and Business", "Others"],

    "*ARABY CULINARIA SIRIA*": ["Food and groceries", "Groceries"],
    "*Uber*": ["Transportation", "Others"],
    "*Sergio Atsuchi Endo*": ["Food and groceries", "Groceries"],
    "*CLEUSA APARECIDA AGUIAR*": ["Housing", "Utilities"],

    "*rendimento*": ['Income', 'Revenue'],
    "*dividendo*": ['Income', 'Dividends'],
    "*JUROS S/ CAPITAL*": ['Income', 'Revenue'],
    "*Pgto Juros*": ['Income', 'Revenue']

}


def upsertCategoryMap():
    with Session(engine) as session:
        for key, value in category_map.items():
            catmap = session.query(CategoryMap).filter_by(statement_name=key).first()
            category = session.query(Category).filter_by(name=value[0]).first()
            subcategory = session.query(Subcategory).filter_by(name=value[1]).first()

            if catmap:
                catmap.category_id = category.id
                catmap.subcategory_id = subcategory.id
            else:
                session.add(CategoryMap(
                    statement_name=key,
                    category_id=category.id,
                    subcategory_id=subcategory.id
                ))

            session.commit()


def reclassify_categories():
    bankmerging = BankDataMerging()

    with Session(engine) as session:
        for stmt in session.query(BankStatement).all():
            category_id, subcategory_id = bankmerging.define_category(stmt.description, session)

            stmt.category_id = category_id
            stmt.subcategory_id = subcategory_id

        session.commit()


if __name__ == '__main__':
    upsertCategoryMap()
    reclassify_categories()


# TODO Implement Investment View in SuperSet


"""
update finance.bank_statements set category_id = 6, subcategory_id = 36  where amount = -878;
update finance.bank_statements set category_id = 12, subcategory_id = 57 where amount = -200 and description ilike 'Transferência enviada pelo Pix%' and category_id = 13;
update finance.bank_statements set category_id = 6, subcategory_id = 38 where amount = -50 and description ilike 'Transferência enviada pelo Pix' and category_id = 13 and date >= '2023-01-01';
update finance.bank_statements set category_id = 9, subcategory_id = 48 where amount = -1000 and description ilike 'Transferência enviada pelo Pix%' and description not ilike '%Conta primaria%';
"""