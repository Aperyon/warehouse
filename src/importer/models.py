import datetime as dt
import uuid

import attr


def event_type_validator(instance, attribute, value):
    if value not in instance.EVENT_TYPES:
        raise ValueError()


@attr.s
class TransactionMessage:
    EVENT_TYPE_SALE = "SALE"
    EVENT_TYPE_INCOMING = "INCOMING"
    EVENT_TYPES = [
        EVENT_TYPE_SALE,
        EVENT_TYPE_INCOMING,
    ]
    transaction_id = attr.ib(validator=attr.validators.instance_of(uuid.UUID))
    event_type = attr.ib(validator=event_type_validator)
    datetime = attr.ib(validator=attr.validators.instance_of(dt.datetime))
    store_id = attr.ib(validator=attr.validators.instance_of(int), converter=int)
    item_id = attr.ib(validator=attr.validators.instance_of(int), converter=int)
    value = attr.ib(validator=attr.validators.instance_of(int), converter=int)

    def serialize(self):
        return {
            "transaction_id": str(self.transaction_id),
            "event_type": self.event_type,
            "datetime": self.datetime.isoformat(),
            "store_id": self.store_id,
            "item_id": self.item_id,
            "value": self.value,
        }

