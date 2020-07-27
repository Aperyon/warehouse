import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get("DB_URL"))

Session = sessionmaker(engine)
session = Session()

Base = declarative_base()


def create_all_tables():
    Base.metadata.create_all(engine)
