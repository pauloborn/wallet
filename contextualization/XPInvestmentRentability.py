from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from models.Investments import Investment, InvestmentType, InvestmentRentability


def money(num: str):
    return float(num.replace('R$', '').replace(',', '.'))


def detect_df_subheaders(rows) -> list:
    df = pd.DataFrame(rows)
    df = df.reset_index(drop=True)
    header_rows = df[df[0].str.contains('\\|') & df[0].str.contains('%')].index.tolist()

    dfs = []
    start = header_rows[0]
    for end in header_rows[1:]:
        dfs.append(df.iloc[start:end])
        start = end
    dfs.append(df.iloc[start:])

    for i, _df in enumerate(dfs):
        columns = _df.iloc[0].tolist()
        columns[0] = columns[0].split(' | ')[1]

        _df.columns = columns
        dfs[i] = _df.iloc[1:]

    return dfs


def process_tesouro_direto(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.TESOURO_DIRETO.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.TESOURO_DIRETO,
                                    purchase_date=None,
                                    purchase_price=money(line['Total aplicado']),
                                    quantity=int(line['Qtd.']),
                                    due_date=datetime.strptime(line['Vencimento'], '%d/%m/%Y').date()
                                    )

            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=money(line['Posição']),
                                                           rentability=None,
                                                           rentability_value=None
                                                           # TODO Load from the database and calculate the rentability
                                                           )

            investments.append((investment, investment_rentability))

        return investments


def process_renda_fixa(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.RENDA_FIXA.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.RENDA_FIXA,
                                    purchase_date=datetime.strptime(line['Data aplicação'], '%d/%m/%Y').date(),
                                    purchase_price=money(line['Valor aplicado']),
                                    quantity=1,
                                    due_date=datetime.strptime(line['Data vencimento'], '%d/%m/%Y').date()
                                    )

            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=money(line['Posição a mercado']),
                                                           rentability_percentage=None,
                                                           rentability_value=None
                                                           # TODO Load from the database and calculate the rentability
                                                           )

            investments.append((investment, investment_rentability))

    return investments


def process_fundos_imobiliarios(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.FUNDOS_IMOBILIARIOS.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.FUNDOS_IMOBILIARIOS,
                                    purchase_date=file_date,
                                    purchase_price=money(line['Última cotação']),
                                    quantity=line['Qtd. total'],
                                    due_date=None
                                    )

            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=money(line['Posição']),
                                                           rentability=None,
                                                           rentability_value=None
                                                           # TODO Load from the database and calculate the rentability
                                                           )
            investments.append((investment, investment_rentability))

    return investments


def process_compromissadas(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.COMPROMISSADAS.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.COMPROMISSADAS,
                                    purchase_date=datetime.strptime(line['Data aplicação'], '%d/%m/%Y').date(),
                                    purchase_price=money(line['Valor aplicado']),
                                    quantity=1,
                                    due_date=datetime.strptime(line['Data vencimento'], '%d/%m/%Y').date()
                                    )

            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=money(line['Posição']),
                                                           rentability=None,
                                                           rentability_value=None
                                                           # TODO Load from the database and calculate the rentability
                                                           )
            investments.append((investment, investment_rentability))

    return investments


def process_previdencia_privada(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.PREVIDENCIA_PRIVADA.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.PREVIDENCIA_PRIVADA,
                                    purchase_date=None,
                                    purchase_price=money(line['Valor aplicado']),
                                    quantity=1,
                                    due_date=None
                                    )

            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=money(line['Posição']),
                                                           rentability=line['Rentabilidade'],
                                                           rentability_value=line['Rentabilidade bruto']
                                                           )
            investments.append((investment, investment_rentability))

    return investments


def process_fundos_de_investimento(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.FUNDOS_DE_INVESTIMENTO.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.FUNDOS_DE_INVESTIMENTO,
                                    purchase_date=datetime.strptime(line['Data da cota'], '%d/%m/%Y').date(),
                                    purchase_price=money(line['Valor aplicado']),
                                    quantity=1,
                                    due_date=None
                                    )

            position = money(line['Valor líquido'])
            rentability = money(line['Rentabilidade'])
            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=position,
                                                           rentability=rentability,
                                                           rentability_value= position * rentability
                                                           )
            investments.append((investment, investment_rentability))

    return investments


def process_coe(rows, file_date):
    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, line in df.iterrows():
            name = f'{InvestmentType.COE.value} - {df.columns[0]} - {line[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.COE,
                                    purchase_date=None,
                                    purchase_price=money(line['Valor aplicado']),
                                    quantity=1,
                                    due_date=datetime.strptime(line['Vencimento'], '%d/%m/%Y').date()
                                    )

            position = money(line['Posição'])
            rentability = money(line['Rentabilidade'])
            investment_rentability = InvestmentRentability(investment=investment,
                                                           date=file_date,
                                                           position=position,
                                                           rentability=rentability,
                                                           rentability_value=money(line['Rentabilidade bruto'])
                                                           )
            investments.append((investment, investment_rentability))

    return investments

