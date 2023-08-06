import pandas as pd
import datetime
import numpy as np
from sqlalchemy.orm import Session

from contextualization.BankDataMerging import BankDataMerging
from contextualization.XPInvestmentRentability import process_tesouro_direto
from models.Investments import Investment, InvestmentType, InvestmentTransaction, InvestmentRentability
from openpyxl import load_workbook


class XPInvestmentDataMerging(BankDataMerging):
    def merge_bank_statement_data(self, file_path):
        pass

    def __init__(self):
        super().__init__()
        self.category_map = None

    def text_to_investmenttype(self, text) -> InvestmentType:

        if text == InvestmentType.TESOURO_DIRETO:
            return InvestmentType.TESOURO_DIRETO
        elif text == InvestmentType.RENDA_FIXA:
            return InvestmentType.RENDA_FIXA
        elif text == InvestmentType.FUNDOS_IMOBILIARIOS:
            return InvestmentType.FUNDOS_IMOBILIARIOS
        elif text == InvestmentType.COMPROMISSADAS:
            return InvestmentType.COMPROMISSADAS
        elif text == InvestmentType.PREVIDENCIA_PRIVADA:
            return InvestmentType.PREVIDENCIA_PRIVADA
        elif text == InvestmentType.FUNDOS_DE_INVESTIMENTO:
            return InvestmentType.FUNDOS_DE_INVESTIMENTO
        elif text == InvestmentType.COE:
            return InvestmentType.COE

        return InvestmentType.UNDEFINED

    def process_investment_rows(self, rows, investmenttype: InvestmentType, file_date):
        pd.DataFrame(rows)
        investments = []

        if investmenttype is InvestmentType.TESOURO_DIRETO:
            investments.append(process_tesouro_direto(rows, file_date))
        elif investmenttype is InvestmentType.RENDA_FIXA:
            pass
        elif investmenttype is InvestmentType.FUNDOS_IMOBILIARIOS:
            pass
        elif investmenttype is InvestmentType.COMPROMISSADAS:
            pass
        elif investmenttype is InvestmentType.PREVIDENCIA_PRIVADA:
            pass
        elif investmenttype is InvestmentType.FUNDOS_DE_INVESTIMENTO:
            pass
        elif investmenttype is InvestmentType.COE:
            pass
        else:
            pass


    def process_investment_rentability_from_excel_file(self, excel_file_path, session: Session):

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

            # Check if the row is completely with empty cells

            if row[0] == InvestmentType.TESOURO_DIRETO.value:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.TESOURO_DIRETO
                investment_rows = []
                continue

            elif row[0] == InvestmentType.RENDA_FIXA.value:
                if current_type:
                    self.process_investment_rows(investment_rows, current_type)

                current_type = InvestmentType.RENDA_FIXA
                investment_rows = []
                continue

            elif row[0] == InvestmentType.FUNDOS_IMOBILIARIOS.value:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.FUNDOS_IMOBILIARIOS
                investment_rows = []
                continue

            elif row[0] == InvestmentType.COMPROMISSADAS.value:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.COMPROMISSADAS
                investment_rows = []
                continue

            elif row[0] == InvestmentType.PREVIDENCIA_PRIVADA.value:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.PREVIDENCIA_PRIVADA
                investment_rows = []
                continue

            elif row[0] == InvestmentType.FUNDOS_DE_INVESTIMENTO:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.FUNDOS_DE_INVESTIMENTO
                investment_rows = []
                continue

            elif row[0] == InvestmentType.COE.value:
                if current_type:
                    # TODO Process investment_rows
                    pass

                current_type = InvestmentType.COE
                investment_rows = []
                continue

            investment_rows.append(row)

            # if current_type == InvestmentType.TESOURO_DIRETO:
            # Check if is a header or the next 2 rows are empty

            # Tesouro Direto						R$ 12.895,62
            #
            # 2,9% | Pós-Fixado	Posição	% Alocação	Total aplicado	Qtd.	Disponível	Vencimento
            # LFT mar/2025	R$ 12.895,62	2,94%	R$ 10.108,80	0,95	0,95	01/03/2025
            #
            #
            #
            # investment_id = row[0]
            # date_str = row[1]
            # value_str = row[2]
            # balance_str = row[3]
            # rentability_str = row[4]
            # current_value_str = row[5]
            #
            # date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()
            # value = float(value_str.replace(',', '.'))
            # balance = float(balance_str.replace(',', '.'))
            # rentability = float(rentability_str.replace(',', '.'))
            # current_value = float(current_value_str.replace(',', '.'))

            # Check if the investment already exists


if __name__ == '__main__':
    xpinvest = XPInvestmentDataMerging()
    # Call process_investment_rentability_from_excel_file with Windows path 'C:\Users\paulo\Development\wallet\data\investments\PosicaoDetalhada_Jul_23.xlsx'
    xpinvest.process_investment_rentability_from_excel_file(
        'C:\\Users\\paulo\\Development\\wallet\\data\\investments\\PosicaoDetalhada_Jul_23.xlsx', None)
