import json
from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from products.serializers import ProductSerializer

@api_view(['GET', 'POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API VIEW that handles both GET and POST
    """
    if request.method == 'GET':
        title=request.GET.get('title')
        if title:
            products=Product.objects.filter(title__icontains=title)
        else:
            products=Product.objects.all()
        serializer=ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)