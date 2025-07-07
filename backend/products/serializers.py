from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'user',
            'sale_price',
            'my_discount',
        ]
        read_only_fields=['user']

    def get_my_discount(self, obj):
        return obj.get_discount()