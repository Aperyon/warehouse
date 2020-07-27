import json
import logging

from dateutil.parser import parse as parse_date
from kafka import KafkaConsumer

from models import Transaction, session as db_session, get_or_create, Storage

logger = logging.getLogger(__name__)
consumer = KafkaConsumer("events")


# TODO: handle duplicated transactions


class NotEnoughStock(Exception):
    pass


def main():
    print("Waiting for messages")
    for raw_message in consumer:
        transaction = create_transaction(raw_message)
        storage, is_created = get_or_create(
            db_session, Storage, store_id=transaction.store_id, item_id=transaction.item_id, defaults={"stock": 0}
        )
        process_transaction(transaction, storage)
        db_session.commit()


def create_transaction(raw_message):
    raw_value = raw_message.value
    value = raw_value.decode("utf-8")
    raw_message = json.loads(value)

    defaults = {
        "event_type": raw_message["event_type"].upper(),
        "date": parse_date(raw_message["date"]),
        "store_id": int(raw_message["store_number"]),
        "item_id": int(raw_message["item_number"]),
        "value": int(raw_message["value"]),
        "status": Transaction.STATUS_PROCESSING,
    }
    transaction, is_created = get_or_create(
        db_session, Transaction, defaults=defaults, uuid=raw_message["transaction_id"]
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
