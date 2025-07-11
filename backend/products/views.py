from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from products.models import Product
from products.serializers import ProductSerializer
from products.filters import UserProductsFilterBackend

# This file handles the logic, e.g. assign user to product

class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [UserProductsFilterBackend, DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'content', 'price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete other user's products.")
        instance.delete()