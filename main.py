from lazyutils.config.Configuration import ConfigFromEnv

config = ConfigFromEnv()  # Initialize logging handler also

import models.main
import wallet

wallet.run()
