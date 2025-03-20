from rest_framework import serializers

from sales.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uid', 'name', 'description', 'price', 'quantity']
        read_only_fields = ['quantity']

class ListProductsSerializer(serializers.Serializer):
    products = serializers.ListField(child=ProductSerializer())