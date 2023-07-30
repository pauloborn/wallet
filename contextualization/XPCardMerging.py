import csv
import datetime
import logging
import os

from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.BankStatements import Bank, BankStatement
from models.base import engine


class XPCardCardMerging(BankDataMerging):

    def merge_bank_stament_data(self, csv_folder):
        logging.info(f"Starting XP Credit Card process")

        csv_files = [file for file in os.listdir(csv_folder) if file.startswith("xp_")]

        for file in csv_files:
            with Session(engine) as session:

                if self.is_file_processed(file, session):
                    logging.info(f"Skipping previously processed file: {file}")
                    continue

                file_path = os.path.join(csv_folder, file)
                with open(file_path, 'r', encoding='utf-8-sig') as csvfile:

                    csvreader = csv.DictReader(csvfile, delimiter=';')
                    lines_loaded = 0
                    for row in csvreader:
                        date_str = str(row['Data'])
                        date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

                        establishment = str(row['Estabelecimento'])
                        amount_str = str(row['Valor'])
                        amount = -float(amount_str.replace('R$', '').replace(',', '.').strip())

                        # Get the bank_id for XP Bank
                        xp_bank = session.query(Bank).filter_by(name='XP').first()

                        # Get the category and subcategory for the statement
                        category_id, subcategory_id = self.define_category(establishment, session)

                        # Check if the statement already exists in the models
                        existing_statement = session.query(BankStatement).filter_by(
                            bank_id=xp_bank.id, date=date, amount=amount, description=establishment, method='Card'
                        ).first()

                        if existing_statement:
                            if existing_statement.category_id == category_id and existing_statement.subcategory_id == subcategory_id:
                                logging.info(f"Skipping duplicate statement: {date}, {amount}, {establishment}")
                            else:
                                existing_statement.category_id = category_id
                                existing_statement.subcategory_id = subcategory_id
                        else:
                            # Create and add a new bank statement
                            statement = BankStatement(
                                bank_id=xp_bank.id,
                                date=date,
                                amount=amount,
                                description=establishment,
                                method='Card',
                                category_id=category_id,
                                subcategory_id=subcategory_id
                            )

                            session.add(statement)
                            lines_loaded += 1

                    # Update the list of processed files
                    self.update_processed_file(file_path, 'Processed', lines_loaded, session)

                    # Commit the changes to the models and close the session after processing each file
                    session.commit()

                # Move the processed file to the 'processed_files' folder
                self.move_file_to_processed_folder(file_path)
