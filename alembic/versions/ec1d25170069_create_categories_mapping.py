"""Create categories mapping

Revision ID: ec1d25170069
Revises: 599e5ffeeb68
Create Date: 2023-07-29 19:02:54.369271

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, Integer, String

# revision identifiers, used by Alembic.
revision = 'ec1d25170069'
down_revision = 'd4914d5efc1e'
branch_labels = None
depends_on = None

categories_map = {
    "A Caicara": ["Food and groceries", "Dinning Out"],
    "SECRETARIA DA RECEITA FEDERAL DO BRASIL": ["Work and Business", "Business expenses"],
    "LIGGA TELECOM": ["Housing", "Internet"],
    "GIOVANNI MARTINS DE LIMA IANOSKI 09278663905": ["Terreiro", "Others"],
    "ADEMICON ADM DE CONSORCIO S A": ["Debt Repayment", "Consórcio"],
    "ALLPARK EMPREENDIMENTOS, PARTICIPACOES E": ["Work and Business", "Others"],
    "RESTAURANTE JDURSKI LTDA": ["Food and groceries", "Dinning Out"],
    "Leonardo Sierakowski Garcia": ["Personal", "Others"],
    "JURANDIR PEREIRA FERNANDES": ["Housing", "Garding"],
    "Associação Espiritualista Casa do Vô Benedito": ["Terreiro", "Doações"],
    "Bazar Espiritual": ["Terreiro", "Candles"],
    "Bazar Espiritual S Lui": ["Terreiro", "Guias & itens de toco"],
    "CONTABILIZEI TECNOLOGIA LTDA": ["Work and Business", "Business expenses"],
    "COPEL DISTRIBUICAO SA": ["Housing", "Utilities"],
    "COPEL TELECOM": ["Housing", "Utilities"],
    "Curitiba Sunset Cafe": ["Food and groceries", "Dinning Out"],
    "Ebw*Spotify": ["Entertainment", "Subscriptions"],
    "D Pizza Bacacheri": ["Food and groceries", "Dinning Out"],
    "Emporio Dionisio": ["Terreiro", "Guias & itens de toco"],
    "ENERGISA - COMPAGAS - COMPANHIA PARANAENSE DE GAS": ["Housing", "Utilities"],
    "Hiperzoo": ["Housing", "Others"],
    "Ifood *Ifood": ["Food and Groceries", "Groceries"],
    "Mr Hoppy Agua Verde": ["Food and Groceries", "Groceries"],
    "Netflix.Com": ["Entertainment", "Subscriptions"],
    "Pag*Maderoindustriae": ["Food and Groceries", "Groceries"],
    "Paypal *Hunkhands": ["Education", "Workshops and Courses"],
    "Paypal *Louadlerass": ["Education", "Workshops and Courses"],
    "Paypal *Twilio": ["Work and Business", "Work-Related costs"],
    "PJBANK PAGAMENTOS S.A.": ["Work and Business", "Workshops and Courses"],
    "TELEFONICA BRASIL S A": ["Housing", "Utilities"],
    "Amazonprimebr": ["Entertainment", "Subscriptions"],
    "Casa de Carnes Mikilas": ["Food and Groceries", "Dining Out"],
    "BANCO ITAUCARD S.A.": ["Debt Repayment", "Credit Card"],
    "Barbearia Dom Heitor": ["Personal", "Others"],
    "posto": ["Transportation", "Gasoline/Fuel"],
    "uber": ["Transportation", "Ride-Sharing/Uber"],
    "tim*": ["Housing", "Utilities"],
    "Ana Claudia Condeixa": ["Health and Sports", "Tennins"],
    "Vô Benedito": ["Terreiro", "Others"],
    "Subway": ["Food and Groceries", "Groceries"],
    "Lacqua Verde": ["Food and Groceries", "Groceries"],
    "Mercado Bella Vila Agu": ["Food and Groceries", "Groceries"],
    "Ponto Final Materiais": ["Housing", "Home maintenance"],
    "Sub Sao Braz Comercio": ["Food and Groceries", "Groceries"],
    "TELEFONICA": ["Housing", "Utilities"],
    "Madero": ["Fodd and Groceries", "Groceries"],
    "PAULO CESAR BORN MARTINELLI": ["Savings and Investments", "Investments Contributions"],
    "Bar ": ["Food and Groceries", "Dining Out"],
    "COMPAGAS": ["Housing", "Utilities"],
    "COPEL": ["Housing", "Utilities"],
    "Happy Garden": ["Housing", "Home maintenance"],
    "Airbnb": ["Travel and Vacation", "Hotels/Accommodation"],
    "Amo Janela": ["Food and Groceries", "Dinning Out"],
    "Baggio Pizzaria": ["Food and Groceries", "Groceries"],
    "Balaroti": ["Housing", "Home maintanence"],
    "Bondinho Pao de Acucar": ["Travel and Vacation", "Others"],
    "Cadre": ["Travel and Vacation", "Others"],
    "Casa de Carnes": ["Food and Groceries", "Groceries"],
    "Castelfranco": ["Food and Groceries", "Groceries"],
    "CELESTINO POITEVIN NETO": ["Health and Sports", "Others"],
    "Condor": ["Food and Groceries", "Groceries"],
    "Confeitaria Jauense": ["Food and Groceries", "Groceries"],
    "Cornershop": ["Food and Groceries", "Groceries"],
    "Cristiane Maria M Araujo": ["Terreiro", "Others"],
    "DARF": ["Work and Business", "Others"],
    "Dundee": ["Food and Groceries", "Groceries"],
    "Spotify": ["Entertainment", "Subscriptions"],
    "Estacionamento": ["Transportation", "Others"],
    "Farmacia": ["Health and Sports", "Vitamins and Supplements"],
    "Hamd Curitiba": ["Food and Groceries", "Groceries"],
    "Ifood": ["Food and Groceries", "Groceries"],
    "IUGU": ["Work and Business", "Others"],
    "Leroy Merlin": ["Housing", "Home maintanence"],
    "LOCAWEB": ["Terreiro", "Others"],
    "Loop Food": ["Food and Groceries", "Groceries"],
    "Marcelo Oliveira Camargo": ["Health and Sports", "Tennis"],
    "Mercado ": ["Food and Groceries", "Groceries"],
    "Supermercados": ["Food and Groceries", "Groceries"],
    "Mustang Sally": ["Food and Groceries", "Dinning Out"],
    "Padaria": ["Food and Groceries", "Groceries"],
    "Casadecarnes": ["Food and Groceries", "Groceries"],
    "Panvel": ["Health and Sports", "Vitamins and Supplements"],
    "Panif": ["Food and Groceries", "Groceries"],
    "PAULO MARTINELLI": ["Debt Repayment", "Others"],
    "Alipay": ["Others", "Others"],
    "Petro Kennedy": ["Transportation", "Gasoline/Fuel"],
    "Pizza": ["Food and Groceries", "Groceries"],
    "Riachuelo": ["Personal", "Clothes"],
    "Suryana": ["Food and Groceries", "Groceries"],
    "VIVO*": ["Housing", "Utilities"],
    "Zaca Dog": ["Food and Groceries", "Dinning Out"],
    "ADEMILAR": ["Debt Repayment", "Consórcio"],
    "Alpargatas": ["Personal", "Clothes"],
    "Tenis": ["Health and Sports", "Tennis"],
    "Centauro": ["Personal", "Clothes"]
}


def upgrade() -> None:
    for statement_name, (category_name, subcategory_name) in categories_map.items():
        op.execute(
            f"""
                INSERT INTO finance.category_map (statement_name, category_id, subcategory_id)
                SELECT '{statement_name}', c.id, sc.id FROM finance.category c
                    JOIN finance.subcategory sc ON (c.id = sc.category_id)
                WHERE c.name = '{category_name}' AND sc.name = '{subcategory_name}' 
            """
        )


def downgrade() -> None:
    category_map_table = sa.table('category_map',
                                  column('id', Integer),
                                  column('statement_name', String),
                                  column('category_id', Integer),
                                  column('subcategory_id', Integer)
                                  )

    sa.delete(category_map_table)
