from sqlalchemy.ext.declarative import declarative_base
from config_reader import ConfigReader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

cr = ConfigReader()
host, port, dbname, user, password = cr.get_database_config()
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, dbname))
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine, checkfirst=True)