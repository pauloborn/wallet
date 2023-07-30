import csv
import datetime
import logging
import os

from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.base import engine


class NubankCreditCardMerging(BankDataMerging):

    def merge_bank_statement_data(self, csv_folder):
        logging.info(f"Starting Nubank Credit Card process")

        csv_files = [file for file in os.listdir(csv_folder) if file.startswith("nubank-")]

        for file in csv_files:
            with Session(engine) as session:

                if self.is_file_processed(file, session):
                    logging.info(f"Skipping previously processed file: {file}")
                    continue

                file_path = os.path.join(csv_folder, file)
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.DictReader(csvfile)
                    lines_loaded = 0
                    for row in csvreader:
                        date_str = row['date']
                        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                        amount = -float(row['amount'])
                        title = row['title']

                        if self.build_bank_statement(
                            session=session,
                            bankname='Nubank',
                            date=date,
                            amount=amount,
                            description=title,
                            method='Card'
                        ):
                            lines_loaded += 1

                    # Update the list of processed files
                    self.update_processed_file(file, 'Processed', lines_loaded, session)

                    # Commit the changes to the models and close the session after processing each file
                    session.commit()

                # Move the processed file to the 'processed_files' folder
                self.move_file_to_processed_folder(file_path)
