import csv
import datetime
import logging
import os

from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.base import engine
from misc.convertors import money, num


class XPCardCardMerging(BankDataMerging):

    def merge_bank_statement_data(self, csv_folder):
        logging.info(f"Starting XP Credit Card process")

        csv_files = [file for file in os.listdir(csv_folder) if file.startswith("xp_") or file.startswith("Fatura XP")]

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
                        try:
                            date_str = str(row['Data'])
                            date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

                            establishment = str(row['Estabelecimento'])
                            amount_str = str(row['Valor'])
                            amount = -money(amount_str)

                            if self.build_bank_statement(
                                session=session,
                                bankname='XP',
                                date=date,
                                amount=amount,
                                description=establishment,
                                method='Card'
                            ):
                                lines_loaded += 1

                        except ValueError as ve:
                            logging.error(f"Unable to process line with values: {row}")
                            raise ValueError

                    # Update the list of processed files
                    self.update_processed_file(file_path, 'Processed', lines_loaded, session)

                    # Commit the changes to the models and close the session after processing each file
                    session.commit()

                # Move the processed file to the 'processed_files' folder
                self.move_file_to_processed_folder(file_path)
