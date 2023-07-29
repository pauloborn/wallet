from lazyutils.config.Configuration import Config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base

# Create a PostgreSQL engine (replace 'username', 'password', 'host', and 'database' with your own values)
config = Config('./config/config.ini')  # Initialize logging handler also
DB_URI = config['postgres']['uri']
schema = config['postgres']['schema']

engine = create_engine(DB_URI)

Base = declarative_base(metadata=MetaData(schema=schema))
