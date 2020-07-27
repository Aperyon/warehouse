import datetime as dt
from unittest.mock import Mock

import pytest

import main
from models import Transaction, Storage
from exceptions import InvalidTransactionValue


@pytest.fixture
def raw_transaction():
    return {
        "event_type": Transaction.EVENT_TYPE_INCOMING,
        "date": "2020-07-27T12:00:00Z",
        "store_number": "1",
        "item_number": "2",
        "value": "3",
    }


def test_calls_for_process_transaction_for_sale(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(main, "_process_sale_transaction", mock)

    transaction = Transaction(event_type=Transaction.EVENT_TYPE_SALE)
    storage = Storage()
    main.process_transaction(transaction, storage)

    mock.assert_called()


def test_calls_for_process_transaction_for_incoming(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(main, "_process_incoming_transaction", mock)

    transaction = Transaction(event_type=Transaction.EVENT_TYPE_INCOMING)
    storage = Storage()
    main.process_transaction(transaction, storage)

    mock.assert_called()


def test_processing_incoming_transaction():
    transaction = Transaction(store_id=1, item_id=1, value=3, status=Transaction.STATUS_PROCESSING)
    storage = Storage(store_id=1, item_id=1, stock=1)

    main._process_incoming_transaction(transaction, storage)

    assert transaction.status == Transaction.STATUS_COMPLETED
    assert storage.stock == 4


class TestProcessingSaleTransaction:
    def test_not_enough_stock(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(main.logger, "error", mock)

        transaction = Transaction(store_id=1, item_id=1, value=3, status=Transaction.STATUS_PROCESSING)
        storage = Storage(store_id=1, item_id=1, stock=1)

        main._process_sale_transaction(transaction, storage)

        mock.assert_called()
        assert storage.stock == 1
        assert transaction.status == Transaction.STATUS_REJECTED

    def test_enough_stock(self):
        transaction = Transaction(store_id=1, item_id=1, value=3, status=Transaction.STATUS_PROCESSING)
        storage = Storage(store_id=1, item_id=1, stock=10)

        main._process_sale_transaction(transaction, storage)

        assert storage.stock == 7
        assert transaction.status == Transaction.STATUS_COMPLETED


class TestMakingTransactionDefaultsFromRaw:
    def test_valid_raw(self, raw_transaction):
        defaults = main.make_transaction_defaults(raw_transaction)
        assert len(defaults.keys()) == 6
        assert defaults["event_type"] == Transaction.EVENT_TYPE_INCOMING
        assert defaults["date"] == dt.datetime(2020, 7, 27, 12, tzinfo=dt.timezone.utc)
        assert defaults["store_id"] == 1
        assert defaults["item_id"] == 2
        assert defaults["value"] == 3

    @pytest.mark.parametrize(
        "update_keys",
        [
            {"event_type": "WRONG_VALUE"},
            {"date": "WRONG_VALUE"},
            {"store_number": "WRONG_VALUE"},
            {"item_number": "WRONG_VALUE"},
            {"value": "WRONG_VALUE"},
        ],
    )
    def test_invalid_event_type(self, raw_transaction, update_keys):
        raw_transaction.update(update_keys)
        with pytest.raises(InvalidTransactionValue):
            main.make_transaction_defaults(raw_transaction)

    @pytest.mark.parametrize(
        "missing_key", ["event_type", "date", "store_number", "item_number", "value",],
    )
    def test_missing_value(self, raw_transaction, missing_key):
        raw_transaction.pop(missing_key)
        with pytest.raises(InvalidTransactionValue):
            main.make_transaction_defaults(raw_transaction)

