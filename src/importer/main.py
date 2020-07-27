import sys
import csv
import json
import logging

from dateutil.parser import parse as parse_date
from kafka import KafkaProducer

from common.exceptions import InvalidTransactionMessage
from common import utils as u


producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_URL"])
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main():
    file_name = sys.argv[1]

    for row_data in open_csv(file_name):
        try:
            message = get_validated_message(row_data)
        except InvalidTransactionMessage:
            logger.error("Invalid Message: `%s`", message)
            continue

        send_message(message)


def open_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            yield row


def get_validated_message(row_data):
    transaction_message = u.create_transaction_from_message(row_data)
    return json.dumps(transaction_message.serialize()).encode("utf-8")


def send_message(message: bytes, topic="events"):
    logger.debug("[SENDING] %s", message)
    producer.send(topic, message)


if __name__ == "__main__":
    main()
