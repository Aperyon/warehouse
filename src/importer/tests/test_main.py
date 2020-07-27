import datetime as dt
import uuid

import pytest

import main
import exceptions
from models import TransactionMessage


@pytest.fixture
def raw_transaction_dict():
    return {
        "transaction_id": "cacedece-bee3-414d-a252-d37ad0443608",
        "event_type": "sale",
        "date": "2020-07-27T12:00:00Z",
        "store_number": "1",
        "item_number": "2",
        "value": "3",
    }


def test_correct_transaction_message(raw_transaction_dict):
    expected_transaction_message = TransactionMessage(
        transaction_id=uuid.UUID("cacedece-bee3-414d-a252-d37ad0443608"),
        event_type="SALE",
        datetime=dt.datetime(2020, 7, 27, 12, tzinfo=dt.timezone.utc),
        store_id=1,
        item_id=2,
        value=3,
    )
    assert main.get_transaction_message(raw_transaction_dict) == expected_transaction_message


@pytest.mark.parametrize(
    "updated_keys",
    [
        {"event_type": "WRONG"},
        {"date": "WRONG"},
        {"store_number": "WRONG"},
        {"item_number": "WRONG"},
        {"value": "WRONG"},
        {"transaction_id": "WRONG"},
    ],
)
def test_wrong_data_types(raw_transaction_dict, updated_keys):
    raw_transaction_dict.update(updated_keys)
    with pytest.raises(exceptions.InvalidTransactionMessage):
        main.get_transaction_message(raw_transaction_dict)


@pytest.mark.parametrize(
    "missing_key", ["event_type", "date", "store_number", "item_number", "value", "transaction_id",],
)
def test_missing_keys(raw_transaction_dict, missing_key):
    raw_transaction_dict.pop(missing_key)
    with pytest.raises(exceptions.InvalidTransactionMessage):
        main.get_transaction_message(raw_transaction_dict)
