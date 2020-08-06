from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


class StoreViews(GenericViewSet):
    @action(detail=True, methods=['get'])
    def purchases(self, request, pk):
        return Response([])
