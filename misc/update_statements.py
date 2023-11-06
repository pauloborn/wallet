import csv
from datetime import datetime

from sqlalchemy.orm import Session

from models.BankStatements import BankStatement
from models.Investments import Investment
from models.base import engine
from models.view.categoryview import CategoryView


def update_statements(file_csv: str):
    """
    Update category and subcategory for matching records in BankStatement model
    by reading data from a CSV file and saving the updates to the database.
    :param file_csv: The path to the CSV file.
    :type file_csv: str
    """

    try:
        with Session(engine) as session:
            category_view = CategoryView(session)

            with open(file_csv, 'r', newline='', encoding='utf-8-sig') as csvfile:
                csv_reader = csv.DictReader(csvfile, delimiter=';')

                for row in csv_reader:
                    date_str = row['date']
                    date = datetime.strptime(date_str, '%d/%m/%Y').date()
                    amount = float(row['amount'])
                    description = row['description']
                    category_str = row['category']
                    category_id = category_view.category_id_from_name(category_str)
                    subcategory_str = row['subcategory']
                    subcategory_id = category_view.subcategory_id_from_name(subcategory_str, category_id)

                    # Search for matching records in BankStatement model
                    matching_records = session.query(BankStatement).filter_by(
                        date=date, amount=amount, description=description
                    ).all()

                    # Update category and subcategory for matching records
                    for record in matching_records:
                        record.category_id = category_id
                        record.subcategory_id = subcategory_id

            session.commit()

    except Exception as e:
        print(f"Error updating BankStatement records: {str(e)}")
        raise e


if __name__ == '__main__':
    file_csv = "C:\\Users\\paulo\\Development\\wallet\\data\\misc\\20231106_005258.csv"
    update_statements(file_csv)
