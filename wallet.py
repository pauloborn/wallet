from lazyutils.config.Configuration import ConfigFromEnv

from contextualization.ItauDataMerging import ItauDataMerging
from contextualization.NubankCreditCardMerging import NubankCreditCardMerging
from contextualization.NubankDataMerging import NubankDataMerging
from contextualization.XPCardMerging import XPCardCardMerging


def run():
    config = ConfigFromEnv()  # Initialize logging handler also

    nubank = NubankDataMerging()
    nubank.merge_bank_statement_data(config['wallet']['csvfolder'])

    nubankcard = NubankCreditCardMerging()
    nubankcard.merge_bank_statement_data(config['wallet']['csvfolder'])

    xpcard = XPCardCardMerging()
    xpcard.merge_bank_statement_data(config['wallet']['csvfolder'])

    itau = ItauDataMerging()
    itau.merge_bank_statement_data(config['wallet']['csvfolder'])



if __name__ == '__main__':
    run()
