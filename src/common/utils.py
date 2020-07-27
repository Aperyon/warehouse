import uuid

from dateutil.parser import parse as parse_date

from . import exceptions
from .models import TransactionMessage


def create_transaction_from_message(message):
    try:
        return TransactionMessage(
            transaction_id=uuid.UUID(message["transaction_id"]),
            event_type=message["event_type"].upper(),
            date=parse_date(message["date"]),
            store_number=message["store_number"],
            item_number=message["item_number"],
            value=message["value"],
        )
    except (ValueError, TypeError, KeyError) as e:
        raise exceptions.InvalidTransactionMessage(f"Original Exception: `{e}`")
