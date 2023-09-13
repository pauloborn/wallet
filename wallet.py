from lazyutils.config.Configuration import ConfigFromEnv

from contextualization.ItauDataMerging import ItauDataMerging
from contextualization.NubankCreditCardMerging import NubankCreditCardMerging
from contextualization.NubankDataMerging import NubankDataMerging
from contextualization.XPCardMerging import XPCardCardMerging
from contextualization.XPDataMerging import XPDataMerging
from contextualization.XPInvestment import XPInvestmentDataMerging


def run():
    config = ConfigFromEnv()  # Initialize logging handler also

    xp_investment = XPInvestmentDataMerging()
    xp_investment.merge_bank_statement_data(config['wallet']['investmentfolder'])

    nubank = NubankDataMerging()
    nubank.merge_bank_statement_data(config['wallet']['csvfolder'])

    nubankcard = NubankCreditCardMerging()
    nubankcard.merge_bank_statement_data(config['wallet']['csvfolder'])

    xpcard = XPCardCardMerging()
    xpcard.merge_bank_statement_data(config['wallet']['csvfolder'])

    itau = ItauDataMerging()
    itau.merge_bank_statement_data(config['wallet']['csvfolder'])

    xpbankstatement = XPDataMerging()
    xpbankstatement.merge_bank_statement_data(config['wallet']['csvfolder'])


if __name__ == '__main__':
    run()
