import sys
import csv
import json
import logging
import uuid

from dateutil.parser import parse as parse_date
from kafka import KafkaProducer

from exceptions import InvalidTransactionMessage
from models import TransactionMessage


producer = KafkaProducer(bootstrap_servers="localhost:9092")
logger = logging.getLogger(__name__)


def main():
    csv_filename = sys.argv[1]
    content = parse_csv_file(csv_filename)

    for row_data in content:
        try:
            message = get_validated_message(row_data)
        except InvalidTransactionMessage:
            logger.error("Invalid Message: `%s`", message)
            continue

        send_message(message)


def parse_csv_file(csv_filename):
    with open(csv_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            yield row


def get_validated_message(row_data):
    transaction_message = get_transaction_message(row_data)
    return json.dumps(transaction_message.serialize()).encode("utf-8")


def get_transaction_message(row_data):
    try:
        return TransactionMessage(
            transaction_id=uuid.UUID(row_data["transaction_id"]),
            event_type=row_data["event_type"].upper(),
            date=parse_date(row_data["date"]),
            store_number=row_data["store_number"],
            item_number=row_data["item_number"],
            value=row_data["value"],
        )
    except (ValueError, TypeError, KeyError) as e:
        raise InvalidTransactionMessage(f"Original Exception: `{e}`")


def send_message(message: bytes, topic="events"):
    logger.debug("[SENDING] %s", message)
    producer.send(topic, message)


if __name__ == "__main__":
    main()
