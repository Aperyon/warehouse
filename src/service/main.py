import json
import logging

from dateutil.parser import parse as parse_date
from kafka import KafkaConsumer

from models import Transaction, Storage
from db import session
from db_utils import get_or_create
from exceptions import NotEnoughStock


logger = logging.getLogger(__name__)
consumer = KafkaConsumer("events")


# TODO: handle duplicated transactions


def main():
    print("Waiting for messages")
    for raw_message in consumer:
        transaction = get_or_create_transaction(raw_message)
        storage, is_created = get_or_create(
            session, Storage, store_id=transaction.store_id, item_id=transaction.item_id, defaults={"stock": 0}
        )
        process_transaction(transaction, storage)
        session.commit()


def get_or_create_transaction(raw_message):
    raw_transaction_value = raw_message.value.decode("utf-8")
    raw_transaction = json.loads(raw_transaction_value)

    defaults = {
        "event_type": raw_transaction["event_type"].upper(),
        "date": parse_date(raw_transaction["date"]),
        "store_id": int(raw_transaction["store_number"]),
        "item_id": int(raw_transaction["item_number"]),
        "value": int(raw_transaction["value"]),
        "status": Transaction.STATUS_PROCESSING,
    }
    transaction, is_created = get_or_create(
        session, Transaction, defaults=defaults, uuid=raw_transaction["transaction_id"]
    )
    return transaction


def process_transaction(transaction, storage):
    if transaction.event_type == Transaction.EVENT_TYPE_SALE:
        _process_sale_transaction(transaction, storage)
    elif transaction.event_type == Transaction.EVENT_TYPE_INCOMING:
        _process_incoming_transaction(transaction, storage)


def _process_sale_transaction(transaction, storage):
    try:
        _validate_stock(transaction, storage)
    except NotEnoughStock:
        return

    storage.stock -= transaction.value
    transaction.status = Transaction.STATUS_COMPLETED


def _validate_stock(transaction, storage):
    if storage.stock < transaction.value:
        transaction.status = Transaction.STATUS_REJECTED
        logger.error(
            "Unable to sell %s of item <%s> in store <%s>, only %s left",
            transaction.value,
            transaction.item_id,
            transaction.store_id,
            storage.stock,
        )
        raise NotEnoughStock()


def _process_incoming_transaction(transaction, storage):
    storage.stock += transaction.value
    transaction.status = transaction.STATUS_COMPLETED


if __name__ == "__main__":
    main()
