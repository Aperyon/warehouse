from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models as m
from . import services
from stores import models as store_m
from customers import models as customer_m
from storages import exceptions as storage_exc


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(source='store', queryset=store_m.Store.objects.all())
    customer_id = serializers.PrimaryKeyRelatedField(source='customer', queryset=customer_m.Customer.objects.all())

    class Meta:
        model = m.Purchase
        fields = ['id', 'store_id', 'item', 'quantity', 'customer_id']

    def create(self, validated_data):
        try:
            return services.create_purchase(validated_data)
        except storage_exc.NotEnoughStock:
            raise ValidationError({'non_field_error': 'Not enough stock'})
