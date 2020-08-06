import datetime as dt

import pytest
from rest_framework.test import APIClient

from customers import models as customer_m
from stores import models as store_m
from storages import models as storage_m


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def store_db():
    return store_m.Store.objects.create(
        name='Example Store',
        open=dt.time(9),
        close=dt.time(17),
    )


@pytest.fixture
def store_db2():
    return store_m.Store.objects.create(
        name='Example Store 2',
        open=dt.time(9),
        close=dt.time(17),
    )


@pytest.fixture
def customer_db():
    return customer_m.Customer.objects.create(
        name='Test Customer',
        email='test@email.com'
    )


@pytest.fixture
def storage_db(store_db):
    return storage_m.Storage.objects.create(
        store=store_db,
        item='1',
        stock=1000
    )
