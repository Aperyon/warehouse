import json 

import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from purchases import models as m


@pytest.mark.django_db
class TestPurchaseCreation:
    def test_create_purchase(self, api_client, store_db, customer_db, storage_db):
        data = {
            'store_id': store_db.pk,
            'item': storage_db.item,
            'quantity': 1,
            'customer_id': customer_db.pk
        }
        resp = api_client.post(reverse('purchase-list'), data)
        assert resp.status_code == status.HTTP_201_CREATED, resp.data
        assert m.Purchase.objects.count() == 1

        purchase = m.Purchase.objects.first()
        assert len(resp.data) == 5
        assert resp.data['store_id'] == store_db.pk
        assert resp.data['customer_id'] == customer_db.pk
        assert resp.data['item'] == storage_db.item
        assert resp.data['quantity'] == 1
        assert resp.data['id'] == purchase.pk

        storage_db.refresh_from_db()
        assert storage_db.stock == 999

    def test_not_enough_stock(self, api_client, store_db, customer_db):
        data = {
            'store_id': store_db.pk,
            'item': '123',
            'quantity': 1,
            'customer_id': customer_db.pk
        }
        resp = api_client.post(reverse('purchase-list'), data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(resp.content.decode('utf-8')) == {'non_field_error': 'Not enough stock'}
        assert len(resp.data) == 1
        assert not m.Purchase.objects.exists()
    
    def test_wrong_store(self, api_client, store_db2, customer_db, storage_db):
        assert store_db2 != storage_db.store

        data = {
            'store_id': store_db2.pk,
            'item': '123',
            'quantity': 1,
            'customer_id': customer_db.pk
        }
        resp = api_client.post(reverse('purchase-list'), data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert json.loads(resp.content.decode('utf-8')) == {'non_field_error': 'Not enough stock'}
        assert len(resp.data) == 1
        assert not m.Purchase.objects.exists()
