from dataclasses import dataclass
from uuid import uuid4
import sys
import csv
import json

from kafka import KafkaProducer


# TODO: use kafka
# TODO: make sure there is only one iteration of the file content
# TODO: validate message
producer = KafkaProducer(bootstrap_servers="localhost:9092")


EVENT_TYPE_INCOMING = "incomining"
EVENT_TYPE_SALE = "sale"


@dataclass
class Message:
    transaction_id: str
    event_type: str
    date: str
    store_number: int
    item_number: int
    value: int


def main():
    csv_filename = sys.argv[1]
    print("Filename", csv_filename)
    content = parse_csv_file(csv_filename)

    for row_data in content:
        message = serialize_row_data(row_data)
        send_message(message)


def parse_csv_file(csv_filename):
    content = []
    line_number = 0
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if line_number == 0:
                keys = row
            else:
                row_data = {key: value for key, value in zip(keys, row)}
                content.append(row_data)
            line_number += 1
    print(content)
    return content


def serialize_row_data(row_data):
    return json.dumps(row_data).encode("utf-8")


def send_message(message: bytes, topic="events"):
    print("Sending message", message)
    producer.send(topic, message)


if __name__ == "__main__":
    main()

