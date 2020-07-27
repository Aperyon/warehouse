from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

from db import Base, engine


class Transaction(Base):
    EVENT_TYPE_SALE = "SALE"
    EVENT_TYPE_INCOMING = "INCOMING"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_REJECTED = "REJECTED"

    __tablename__ = "Transactions"

    uuid = Column(String, primary_key=True)
    event_type = Column(String)
    date = Column(DateTime)
    store_id = Column(Integer)
    item_id = Column(Integer)
    value = Column(Integer)
    status = Column(String)


class Storage(Base):
    __tablename__ = "Storages"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    item_id = Column(Integer)
    stock = Column(Integer)


Session = sessionmaker(engine)
session = Session()

Base.metadata.create_all(engine)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True
