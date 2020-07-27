import json
import logging

from dateutil.parser import parse as parse_date, ParserError
from kafka import KafkaConsumer

from models import Transaction, Storage
from db import session
from db_utils import get_or_create
from exceptions import NotEnoughStock, InvalidTransactionValue


logger = logging.getLogger(__name__)
consumer = KafkaConsumer("events")


def main():
    print("Waiting for messages")
    for raw_message in consumer:
        process_raw_message(raw_message)


def process_raw_message(raw_message):
    message = get_message_from_raw(raw_message)
    transaction, is_created = get_or_create_transaction(message)

    if not is_created:
        # We don't care about what status is the existing transaction is in.
        # It is a problem if it already exists.
        logger.error("Transaction <%s> already exists, skipping", transaction.uuid)
        return

    storage, is_created = get_or_create(
        session, Storage, store_id=transaction.store_id, item_id=transaction.item_id, defaults={"stock": 0}
    )
    process_transaction(transaction, storage)
    session.commit()


def get_message_from_raw(raw_message):
    raw_message_value = raw_message.value.decode("utf-8")
    message = json.loads(raw_message_value)
    return message


def get_or_create_transaction(message):
    raw_transaction = message
    defaults = make_transaction_defaults(raw_transaction)
    transaction, is_created = get_or_create(
        session, Transaction, defaults=defaults, uuid=raw_transaction["transaction_id"]
    )
    return transaction, is_created


def make_transaction_defaults(raw_transaction):
    defaults = {
        "event_type": get_validated_event_type(raw_transaction.get("event_type")),
        "date": get_validated_date(raw_transaction.get("date")),
        "store_id": get_validated_store_id(raw_transaction.get("store_number")),
        "item_id": get_validated_item_id(raw_transaction.get("item_number")),
        "value": get_validated_value(raw_transaction.get("value")),
        "status": Transaction.STATUS_PROCESSING,
    }

    if None in defaults.values():
        raise InvalidTransactionValue()

    return defaults


def get_validated_event_type(raw_value):
    if raw_value is None:
        raise InvalidTransactionValue()

    value = raw_value.upper()

    if value not in Transaction.EVENT_TYPES:
        raise InvalidTransactionValue()

    return value


def get_validated_date(raw_value):
    try:
        value = parse_date(raw_value)
    except (ParserError, TypeError):
        raise InvalidTransactionValue()

    return value


def get_validated_store_id(raw_value):
    return get_validated_int_value(raw_value)


def get_validated_item_id(raw_value):
    return get_validated_int_value(raw_value)


def get_validated_value(raw_value):
    return get_validated_int_value(raw_value)


def get_validated_int_value(raw_value):
    try:
        value = int(raw_value)
    except (ValueError, TypeError):
        raise InvalidTransactionValue()

    return value


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
