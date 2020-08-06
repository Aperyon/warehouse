import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestStorePurchasesAPI:
    def test_store_purchase_empty_list(self, api_client, store_db):
        resp = api_client.get(reverse('store-purchases', kwargs={'pk': store_db.pk}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == []
    
    def test_non_existent_store_is_404(self, api_client):
        resp = api_client.get(reverse('store-purchases', kwargs={'pk': 123}))
        assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    def test_store_purchase_list_with_one_item(self, api_client, store_db, purchase_db):
        resp = api_client.get(reverse('store-purchases', kwargs={'pk': store_db.pk}))
        assert resp.status_code == status.HTTP_200_OK
        assert json.loads(resp.content.decode('utf-8')) == [
            {
                'id': purchase_db.pk,
                'store_id': store_db.pk,
                'item': purchase_db.item,
                'quantity': purchase_db.quantity,
                'customer_id': purchase_db.customer.pk,
            }
        ]
    
    def test_different_store_purchase_list(self, api_client, store_db2, purchase_db):
        assert store_db2 != purchase_db.store
        resp = api_client.get(reverse('store-purchases', kwargs={'pk': store_db2.pk}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == []
