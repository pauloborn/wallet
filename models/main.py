import logging

from sqlalchemy.orm import Session

from models import BankStatements
from models.base import engine

logging.info(f'Loaded and updated all tables metadata')


def insert_banks():
    # Define the names of the banks to be inserted
    bank_names = ["Itau", "Nubank", "XP"]

    # Create a session instance
    with Session(engine) as session:

        try:
            # Check if the banks already exist in the models to avoid duplicates
            existing_banks = session.query(BankStatements.Bank).filter(BankStatements.Bank.name.in_(bank_names)).all()
            existing_bank_names = {bank.name for bank in existing_banks}

            # Insert only the banks that don't exist in the models
            banks_to_insert = [BankStatements.Bank(name=name) for name in bank_names if name not in existing_bank_names]

            if banks_to_insert:
                # Add the banks to the session and commit the changes to the models
                session.add_all(banks_to_insert)
                session.commit()

                logging.info("Banks inserted successfully.")
            else:
                logging.debug("All banks already exist in the models.")

        except Exception as e:
            # Handle any potential errors
            session.rollback()
            logging.error(f"Error inserting banks: {str(e)}")


# insert_banks()

def main():
    return None