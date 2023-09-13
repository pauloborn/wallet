import logging
import os
import pandas as pd
from datetime import datetime

from sqlalchemy.orm import Session
from contextualization.BankDataMerging import BankDataMerging
from models.base import engine


class XPDataMerging(BankDataMerging):
    SKIP_ROWS = 12

    def read_excel_data(self, file_path):
        logging.info(f"Processing file {file_path}")

        df = pd.read_excel(file_path, skiprows=self.SKIP_ROWS, header=1,
                           engine='openpyxl', usecols='B:G', skipfooter=16)

        df.columns = ['Movimentação', 'Liquidação', 'Lançamento', 'Unknown', 'Valor (R$)', 'Saldo (R$)']

        return df

    def process_data(self, df, session):

        # Iterate over data frame
        lines_loaded = 0

        for index, row in df.iterrows():

            try:
                date = row['Liquidação']

                amount = float(row['Valor (R$)'])
                description = row['Lançamento']

                if type(date) is datetime and type(amount) is float:
                    if self.build_bank_statement(
                            session=session,
                            bankname='XP',
                            date=date,
                            amount=amount,
                            description=description,
                            method='Account'
                    ):
                        lines_loaded += 1
                else:
                    logging.info(f"Linha inválida: {row}")

            except AttributeError as ae:
                logging.info(f"Error processing line: ===== {date} - {amount} - {description} ===== ")
            except ValueError as ve:
                logging.info(f"Error processing line: ===== {row} ===== ")

        return lines_loaded

    def merge_bank_statement_data(self, csv_folder):
        logging.info(f"Starting XP account statement process")

        excel_files = [file for file in os.listdir(csv_folder) if file.startswith("Extrato 3052778")]

        for excel in excel_files:
            file_path = os.path.join(csv_folder, excel)
            with Session(engine) as session:
                file_path = os.path.join(csv_folder, excel)
                df = self.read_excel_data(file_path)

                lines_loaded = self.process_data(df, session)

                # Update the list of processed files
                self.update_processed_file(excel, 'Processed', lines_loaded, session)

                session.commit()

            # Move the processed file to the 'processed_files' folder
            self.move_file_to_processed_folder(file_path)

        logging.info("Processed all XP bank statement files")
