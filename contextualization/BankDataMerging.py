# contextualization/BankDataMerging.py
import datetime
import logging
import os
import re
import shutil

from sqlalchemy.orm import Session
from lazyutils.config.Configuration import ConfigFromEnv

from models.BankStatements import ProcessedFiles, CategoryMap, Category, Subcategory


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

    def move_file_to_processed_folder(self, file_path):
        processed_folder = self.config['wallet']['processedfolder']
        os.makedirs(processed_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        destination_path = os.path.join(processed_folder, filename)

        shutil.move(file_path, destination_path)

    def is_file_processed(self, filename, session):
        processed_file = session.query(ProcessedFiles).filter_by(filename=filename, status="Processed").first()
        logging.debug(f'Checking if file was already processed {filename} - {processed_file}')
        return processed_file is not None

    def define_category(self, statement_name, session: Session) -> [str,str] :
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

    def merge_bank_stament_data(self, file_path):
        raise NotImplementedError


class ItauDataMerging(BankDataMerging):
    def merge_bank_stament_data(self, file_path):
        raise NotImplementedError

        # Logic for merging Itau data from the file_path
        # merged_data = pd.read_excel(file_path)
        # Additional Itau-specific merging steps
        # return merged_data


class XPDataMerging(BankDataMerging):
    def merge_bank_stament_data(self, file_path):
        # Logic for merging XP data from the file_path
        # Assuming XP data is in JSON format
        # merged_data = pd.read_json(file_path)
        # Additional XP-specific merging steps
        # return merged_data

        raise NotImplementedError
