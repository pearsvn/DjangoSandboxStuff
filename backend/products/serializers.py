from rest_framework import serializers
import json

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
            'sale_price',
            'my_discount',
        ]

    def get_my_discount(self, obj):
        return obj.get_discount()
    
# def print_pretty_json(response):
#     try:
#         response_json = response.json()
#         print(json.dumps(response_json, indent=4))
#     except ValueError:
#         print("Non-JSON response received.")
#         print(response.text)
#     print(f"Status: {response.status_code}")