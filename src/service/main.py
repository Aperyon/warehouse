import sys
import json
import logging

from dateutil.parser import parse as parse_date, ParserError
from kafka import KafkaConsumer
from common.exceptions import NotEnoughStock, InvalidTransactionMessage
from common import utils as u

from models import Transaction, Storage
from db import session, create_all_db_tables
from db_utils import get_or_create


logging.basicConfig()
logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
# Make sure Kafka guarantees that each message is processed only once
consumer = KafkaConsumer("events")


def main():
    logger.info("Waiting for messages")
    for raw_message in consumer:
        process_raw_message(raw_message)


def process_raw_message(raw_message):
    message = get_message_from_raw(raw_message)

    try:
        transaction, is_created = get_or_create_transaction(message)
    except InvalidTransactionMessage:
        return

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
    defaults = make_transaction_defaults(message)
    transaction, is_created = get_or_create(session, Transaction, defaults=defaults, uuid=message["transaction_id"])
    return transaction, is_created


def make_transaction_defaults(message):
    transaction_message = u.create_transaction_from_message(message)
    defaults = {
        "transaction_id": transaction_message.transaction_id,
        "event_type": transaction_message.event_type,
        "date": transaction_message.date,
        "store_id": transaction_message.store_number,
        "item_id": transaction_message.item_number,
        "value": transaction_message.value,
        "status": Transaction.STATUS_PROCESSING,
    }

    return defaults


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
