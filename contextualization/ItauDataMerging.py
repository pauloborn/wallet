import datetime
import logging
import os

from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from models.base import engine


class ItauDataMerging(BankDataMerging):

    def merge_bank_statement_data(self, folder_path):
        logging.info(f"Starting Itau account statement process")

        text_files = [file for file in os.listdir(folder_path) if file.startswith("Extrato Conta Corrente-")]

        for file in text_files:
            with Session(engine) as session:

                if self.is_file_processed(file, session):
                    logging.info(f"Skipping previously processed file: {file}")
                    continue

                file_path = os.path.join(folder_path, file)
                with open(file_path, 'r', encoding='iso-8859-1') as textfile:
                    lines_loaded = 0
                    for line in textfile:
                        line = line.strip()
                        date_str, description, amount_str = line.split(';')

                        date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
                        amount = float(amount_str.replace(',', '.').strip())

                        if self.build_bank_statement(
                                session=session,
                                bankname='Itau',
                                date=date,
                                amount=amount,
                                description=description,
                                method='Account'):
                            lines_loaded += 1

                    # Update the list of processed files
                    self.update_processed_file(file, 'Processed', lines_loaded, session)

                    # Commit the changes to the models and close the session after processing each file
                    session.commit()

                # Move the processed file to the 'processed_files' folder
                self.move_file_to_processed_folder(file_path)
