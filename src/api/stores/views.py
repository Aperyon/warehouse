from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from . import models as m
from purchases import models as purchase_m
from purchases import serializers as purchase_s


class StoreViews(GenericViewSet):
    @action(detail=True, methods=['get'])
    def purchases(self, request, pk):
        store = get_object_or_404(m.Store, pk=pk)
        purchases = purchase_m.Purchase.objects.filter(store=store)
        serializer = purchase_s.PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)
