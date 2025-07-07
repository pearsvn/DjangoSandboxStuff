from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet

"""
API app-level URL routing.

Registers API viewsets with URL prefixes. Currently:
- 'products' is routed to ProductViewSet.
"""

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]