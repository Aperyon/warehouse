from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from . import serializers as s
from . import models as m


class PurchaseView(CreateModelMixin, GenericViewSet):
    serializer_class = s.PurchaseSerializer
    queryset = m.Purchase.objects.all()
