import pandas as pd
import datetime
import numpy as np
from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from contextualization.XPInvestmentRentability import process_tesouro_direto, process_renda_fixa
from models.Investments import Investment, InvestmentType, InvestmentTransaction, InvestmentRentability
from openpyxl import load_workbook


def get_investmenttype_map(session: Session):
    category_map = {}

    for category in InvestmentType:
        category_map[category.name] = category

    return category_map


class XPInvestmentDataMerging(BankDataMerging):
    def merge_bank_statement_data(self, file_path):
        pass

    def __init__(self):
        super().__init__()
        self.category_map = None

    def process_investment_rows(self, rows, investment_type: InvestmentType, file_date) -> list:
        pd.DataFrame(rows)
        investments = []

        if investment_type is InvestmentType.TESOURO_DIRETO:
            investments.append(process_tesouro_direto(rows, file_date))
        elif investment_type is InvestmentType.RENDA_FIXA:
            investments.append(process_renda_fixa(rows, file_date))
        elif investment_type is InvestmentType.FUNDOS_IMOBILIARIOS:
            investments.append(process_fundos_imobiliarios(rows, file_date))
        elif investment_type is InvestmentType.COMPROMISSADAS:
            investments.append(process_compromissadas(rows, file_date))
        elif investment_type is InvestmentType.PREVIDENCIA_PRIVADA:
            investments.append(process_previdencia_privada(rows, file_date))
        elif investment_type is InvestmentType.FUNDOS_DE_INVESTIMENTO:
            investments.append(process_fundos_de_investimento(rows, file_date))
        elif investment_type is InvestmentType.COE:
            investments.append(process_coe(rows, file_date))
        else:
            pass

        return investments

    def process_investment_rentability_from_excel_file(self, excel_file_path, session: Session):

        self.category_map = get_investmenttype_map(session)

        wb = load_workbook(filename=excel_file_path, read_only=True)
        ws = wb['Sua carteira']
        file_date = datetime.datetime.strptime(ws.cell(row=1, column=6).value.split(' | ')[1], '%d/%m/%Y, %H:%M')

        df = pd.read_excel(excel_file_path, skiprows=5, header=None, engine='openpyxl')
        df.replace('', np.nan, inplace=True)
        df.replace(' ', np.nan, inplace=True)
        df['is_blank'] = df.isnull().all(axis=1)

        current_type = None
        investment_rows = []

        for index, row in df.iterrows():
            if row['is_blank']:
                continue

            if row[0] in self.category_map:
                if current_type:
                    self.process_investment_rows(investment_rows, current_type, file_date)

                current_type = self.category_map[row[0]]
                investment_rows = []
                continue

            investment_rows.append(row)

        for investmenttuple in investment_rows:
            investment = investmenttuple[0]
            investmentrentability = investmenttuple[1]

            # Check if investment already exists in the models
            existing_investment = session.query(Investment).filter_by(
                name=investment.name, type=investment.type, purchase_date=investment.purchase_date,
                purchase_price=investment.purchase_price, quantity=investment.quantity, due_date=investment.due_date
            ).first()

            if not existing_investment:
                session.add(investment)
                # session.commit()

            # Check if investmentrentability already exists in the models
            existing_investmentrentability = session.query(InvestmentRentability).filter_by(
                investment_id=investment.id, date=investmentrentability.date
                ).first()

            if existing_investmentrentability:
                existing_investmentrentability.rentability_percentage = investmentrentability.rentability_percentage
                existing_investmentrentability.rentability_value = investmentrentability.rentability_value
            else:
                session.add(investmentrentability)

        session.commit()


if __name__ == '__main__':
    xpinvest = XPInvestmentDataMerging()
    xpinvest.process_investment_rentability_from_excel_file(
        'C:\\Users\\paulo\\Development\\wallet\\data\\investments\\PosicaoDetalhada_Jul_23.xlsx', None)
