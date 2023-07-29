from lazyutils.config.Configuration import ConfigFromEnv

from contextualization.NubankDataMerging import NubankDataMerging


def run():
    config = ConfigFromEnv()  # Initialize logging handler also

    nubank = NubankDataMerging()
    nubank.merge_bank_stament_data(config['wallet']['csvfolder'])


if __name__ == '__main__':
    run()
