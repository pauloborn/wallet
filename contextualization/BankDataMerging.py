# contextualization/BankDataMerging.py
import datetime
import logging
import os
import re
import shutil

from sqlalchemy.orm import Session
from lazyutils.config.Configuration import ConfigFromEnv

from models.BankStatements import ProcessedFiles, CategoryMap, Category, Subcategory, Bank, BankStatement


class BankDataMerging:

    def __init__(self):
        self.config = ConfigFromEnv()  # Initialize logging handler also
        self.category_map = None

    def update_processed_file(self, filename, status, lines_loaded, session):
        processed_file = session.query(ProcessedFiles).filter_by(filename=filename).first()
        if processed_file:
            processed_file.status = status
            processed_file.end_time = datetime.datetime.now()
            processed_file.lines_loaded = lines_loaded
        else:
            processed_file = ProcessedFiles(
                filename=filename,
                started_at=datetime.datetime.now(),
                status=status,
                end_time=datetime.datetime.now(),
                lines_loaded=lines_loaded
            )
            session.add(processed_file)

    def move_file_to_processed_folder(self, file_path, processed_folder='processedfolder'):
        processed_folder = self.config['wallet'][processed_folder]
        os.makedirs(processed_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        destination_path = os.path.join(processed_folder, filename)

        shutil.move(file_path, destination_path)

    @staticmethod
    def is_file_processed(filename, session):
        processed_file = session.query(ProcessedFiles).filter_by(filename=filename, status="Processed").first()
        logging.debug(f'Checking if file was already processed {filename} - {processed_file}')
        return processed_file is not None

    def define_category(self, statement_name, session: Session) -> [str, str]:
        if self.category_map is None:
            self.category_map = {}
            for cat in session.query(CategoryMap).all():
                self.category_map[cat.statement_name] = [cat.category_id, cat.subcategory_id]

        # Iterate through the categories_map and check for a match with the statement_name using regular expressions
        for key, value in self.category_map.items():
            pattern = ".*?" + re.sub("[^a-zA-Z0-9 \n\.]", ".?", key.lower()) + ".*?"
            if re.match(pattern, statement_name.lower()):
                category_id, subcategory_id = value
                return category_id, subcategory_id

        # If no match is found, return default values
        cid = session.query(Category).filter_by(name='Other').first().id
        scid = session.query(Subcategory).filter_by(name='Others').first().id
        return cid, scid

    def build_bank_statement(self, session: Session, bankname: str, date, amount, description, method) -> bool:
        """

        :rtype: bool - True if any bank_statement was updated or inserted and False if any wasn't updated
        :param session: Session
        :param bankname: str
        :param date: datetime
        :param amount: float
        :param description: str
        :param method: str
        """
        # Get the bank_id for Credit
        credit = session.query(Bank).filter_by(name=bankname).first()

        # Get the category and subcategory for the statement
        category_id, subcategory_id = self.define_category(description, session)

        # Check if the statement already exists in the models
        existing_statement = session.query(BankStatement).filter_by(
            bank_id=credit.id, date=date, amount=amount, description=description, method=method
        ).first()

        if existing_statement:
            if existing_statement.category_id == category_id and existing_statement.subcategory_id == subcategory_id:
                logging.info(f"Skipping duplicate statement: {date}, {amount}, {description}")
                return False
            else:
                existing_statement.category_id = category_id
                existing_statement.subcategory_id = subcategory_id
                return True
        else:

            # Create and add a new bank statement
            statement = BankStatement(
                bank_id=credit.id,
                date=date,
                amount=amount,
                description=description,
                method=method,
                category_id=category_id,
                subcategory_id=subcategory_id
            )

            session.add(statement)

            return True

    def merge_bank_statement_data(self, file_path):
        raise NotImplementedError
