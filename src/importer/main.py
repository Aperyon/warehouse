import sys
import csv
import json
import logging

from kafka import KafkaProducer


# TODO: validate message
producer = KafkaProducer(bootstrap_servers="localhost:9092")
logger = logging.getLogger(__name__)


EVENT_TYPE_INCOMING = "incomining"
EVENT_TYPE_SALE = "sale"


def main():
    csv_filename = sys.argv[1]
    content = parse_csv_file(csv_filename)

    for row_data in content:
        message = serialize_row_data(row_data)
        send_message(message)


def parse_csv_file(csv_filename):
    with open(csv_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            yield row


def serialize_row_data(row_data):
    return json.dumps(row_data).encode("utf-8")


def send_message(message: bytes, topic="events"):
    logger.debug("[SENDING] %s", message)
    producer.send(topic, message)


if __name__ == "__main__":
    main()
