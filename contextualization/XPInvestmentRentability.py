from datetime import datetime

import pandas as pd

from models.Investments import Investment, InvestmentTransaction, InvestmentType, InvestmentRentability


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


def process_tesouro_direto(rows, file_date) -> list:

    investments = []
    dfs = detect_df_subheaders(rows)
    for df in dfs:
        for _, row in df.iterrows():
            name = f'{InvestmentType.TESOURO_DIRETO.value} - {df.columns[0]} - {row[df.columns[0]]}'
            investment = Investment(name,
                                    InvestmentType.TESOURO_DIRETO,
                                    purchase_date=None,
                                    purchase_price=float(row['Total aplicado'].replace('R$', '').replace(',', '.')),
                                    quantity=int(row['Qtd.']),
                                    due_date=datetime.strptime(row['Vencimento'], '%d/%m/%Y').date()
                                    )

            investmentrentability = InvestmentRentability(investment=investment,
                                                          date=file_date,
                                                          position=float(row['Posição'].replace(',', '.')),
                                                          rentability_percentage=None
                                                          # TODO Load from the database and calculate the rentability
                                                          )

            investments.append((investment, investmentrentability))

        return investments

    # for row in rows:
    #     if investmenttype in [InvestmentType.TESOURO_DIRETO.value, InvestmentType.FUNDOS_IMOBILIARIOS.value,
    #                           InvestmentType.FUNDOS_DE_INVESTIMENTO.value, InvestmentType.COE.value]:
    #
    #         if row[1] == 'Posição':
    #             continue
    #
    #         pass
    #
    #     elif investmenttype in [InvestmentType.RENDA_FIXA.value, InvestmentType.COMPROMISSADAS.value]:
    #
    #         if row[1] == 'Posição a mercado':
    #             continue
    #
    #         pass
    #
    #     elif investmenttype in [InvestmentType.PREVIDENCIA_PRIVADA.value]:
    #
    #         if row[2] == 'Posição':
    #             continue
    #
    #         pass
