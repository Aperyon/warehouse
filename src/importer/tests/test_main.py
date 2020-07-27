from unittest.mock import Mock

from .. import main


def test_opening_csv():
    file_name = "tests/resources/example.csv"
    content = main.open_csv(file_name)
    assert {"name": "Tom", "age": "27"} == next(content)
    assert {"name": "Dan", "age": "30"} == next(content)
    assert {"name": "John", "age": "90"} == next(content)


def test_getting_validated_message():
    row_message = {
        "transaction_id": "cacedece-bee3-414d-a252-d37ad0443608",
        "event_type": "sale",
        "date": "2020-07-27T12:00:00Z",
        "store_number": "1",
        "item_number": "2",
        "value": "3",
    }
    expected = b'{"transaction_id": "cacedece-bee3-414d-a252-d37ad0443608", "event_type": "SALE", "date": "2020-07-27T12:00:00Z", "store_number": 1, "item_number": 2, "value": 3}'
    actual = main.get_validated_message(row_message)
    assert actual == expected


def test_send_message(monkeypatch):
    mock_send = Mock()
    monkeypatch.setattr(main.producer, "send", mock_send)
    main.send_message(b"Hello")
    mock_send.assert_called_with("events", b"Hello")
