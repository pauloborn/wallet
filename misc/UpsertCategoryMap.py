from sqlalchemy.orm import Session

from models.BankStatements import CategoryMap, Category, Subcategory
from models.base import engine

category_map = {
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
    "*PERRETTO VIAGENS*": ["Travel and Vacation", "Flights"],
    "*DIGISEC*": ["Work and Business", 'Business Expenses'],
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
    "*restaurante*": ["Food and groceries", "Groceries"]
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
                try:
                    session.add(CategoryMap(
                        statement_name=key,
                        category_id=category.id,
                        subcategory_id=subcategory.id
                    ))
                except AttributeError as e:
                    raise e

            session.commit()


if __name__ == '__main__':
    upsertCategoryMap()
