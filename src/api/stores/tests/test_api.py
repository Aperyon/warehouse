import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
class TestStorePurchasesAPI:
    def test_store_purchase_empty_list(self, api_client, store_db):
        resp = api_client.get(reverse('store-purchases', kwargs={'pk': store_db.pk}))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == []
