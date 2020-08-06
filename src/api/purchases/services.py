from django.db import transaction

from . import models as m
from storages import exceptions as storage_exc
from storages import models as storage_m


def create_purchase(validated_data):
    storage, is_created = storage_m.Storage.objects.get_or_create(
        store=validated_data['store'], 
        item=validated_data['item'], 
        defaults={'stock': 0}
    )
    purchase = _create_purchase(storage, validated_data)

    with transaction.atomic():
        purchase.save()
        storage.save()

    return purchase


def _create_purchase(storage, validated_data):
    if storage.stock < validated_data['quantity']:
        raise storage_exc.NotEnoughStock()

    purchase = m.Purchase(
        store=validated_data['store'],
        customer=validated_data['customer'],
        item=validated_data['item'],
        quantity=validated_data['quantity'],
    )

    storage.stock -= purchase.quantity

    return purchase
