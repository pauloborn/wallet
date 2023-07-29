from lazyutils.config.Configuration import ConfigFromEnv

config = ConfigFromEnv()  # Initialize logging handler also

import database.main
import wallet

wallet.run()
