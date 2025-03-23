from rest_framework import serializers

from sales.models import Product, Ticket

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uid', 'name', 'description', 'price', 'quantity']
        read_only_fields = ['quantity']

class ListProductsSerializer(serializers.Serializer):
    products = serializers.ListField(child=ProductSerializer())

class ProductQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

class ProductForPurchaseSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    quantity = serializers.IntegerField()

class PurchaseSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=ProductForPurchaseSerializer(),
        allow_empty=False,
        min_length=1
    )

    def validate_products(self, data):
        products_dict = {}

        for product in data:
            uid = str(product['uid'])

            if uid in products_dict:
                products_dict[uid]['quantity'] += product['quantity']
                
            else:
                products_dict[uid] = product

        return list(filter(lambda x: x['quantity'] > 0, products_dict.values()))
    
    def validate(self, attrs):
        if len(attrs['products']) <= 0:
            raise serializers.ValidationError('Products is empty')

        return attrs
    
class TicketSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        return list(
            map(
                lambda ptk: {
                    'uid': str(ptk.uid),
                    'name': ptk.product.name,
                    'price': ptk.product_price,
                    'consumed': ptk.consumed
                },
                instance.productticket_set.all()
            )
        )

    class Meta:
        model = Ticket
        fields = ['uid', 'status', 'payment_method', 'original_value', 'remaining_value', 'products']

class TicketWebhookSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    status = serializers.ChoiceField(choices=['confirmed', 'canceled'])
