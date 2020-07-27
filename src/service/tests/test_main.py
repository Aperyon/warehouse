from unittest.mock import Mock


import main
from models import Transaction, Storage


def test_process_transaction_for_sale(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(main, "_process_sale_transaction", mock)

    transaction = Transaction(event_type=Transaction.EVENT_TYPE_SALE)
    storage = Storage()
    main.process_transaction(transaction, storage)

    mock.assert_called()


def test_process_transaction_for_incoming(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(main, "_process_incoming_transaction", mock)

    transaction = Transaction(event_type=Transaction.EVENT_TYPE_INCOMING)
    storage = Storage()
    main.process_transaction(transaction, storage)

    mock.assert_called()


def test_processing_income_transaction():
    transaction = Transaction(store_id=1, item_id=1, value=3, status=Transaction.STATUS_PROCESSING)
    storage = Storage(store_id=1, item_id=1, count=1)

    main._process_incoming_transaction(transaction, storage)

    assert transaction.status == Transaction.STATUS_COMPLETED
    assert storage.count == 4

