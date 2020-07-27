from sqlalchemy import Column, Integer, String, DateTime

from db import Base


class Transaction(Base):
    EVENT_TYPE_SALE = "SALE"
    EVENT_TYPE_INCOMING = "INCOMING"
    EVENT_TYPES = [EVENT_TYPE_SALE, EVENT_TYPE_INCOMING]
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

