from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
#Read config.ini file
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")
dbparam = config_obj["postgresql"]

# set your parameters for the database connection URI using the keys from the configfile.ini
USER_NAME = dbparam["USER_NAME"]
PASSWORD = dbparam["PASSWORD"]
HOSTNAME = dbparam["HOSTNAME"]
PORT = int(dbparam["PORT"])
DATABASE = dbparam["DATABASE"]

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER_NAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()