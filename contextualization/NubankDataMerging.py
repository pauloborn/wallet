# contextualization/NubankDataMerging.py

import csv
import logging
import os
import datetime

from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.BankStatements import Bank, BankStatement
from models.base import engine


class NubankDataMerging(BankDataMerging):

    def merge_bank_statement_data(self, csv_folder):
        logging.info(f"Starting Nubank account statement process")

        csv_files = [file for file in os.listdir(csv_folder) if file.startswith("NU_")]

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
                        date_str = row['Data']
                        date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

                        amount = float(row['Valor'].replace(',', '.'))
                        description = row['Descrição']

                        if self.build_bank_statement(
                            session=session,
                            bankname='Nubank',
                            date=date,
                            amount=amount,
                            description=description,
                            method='Account'
                        ):
                            lines_loaded += 1

                    # Update the list of processed files
                    self.update_processed_file(file, 'Processed', lines_loaded, session)

                    # Commit the changes to the models and close the session after processing each file
                    session.commit()

                # Move the processed file to the 'processed_files' folder
                self.move_file_to_processed_folder(file_path)

        logging.info("Processed all Nubank files")
