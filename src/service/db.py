import time
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DB_URL"))

Session = sessionmaker(engine)
session = Session()

Base = declarative_base()


def create_all_db_tables():
    tries = 0
    while tries < 10:
        tries += 1
        try:
            Base.metadata.create_all(engine)
        except:
            time.sleep(2)
