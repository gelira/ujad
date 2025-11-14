from rest_framework import serializers

from sales.models import Product, Order, Ticket, ConsumingToken
from sales.services import ProductServices

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uid', 'name', 'description', 'price', 'quantity']
        read_only_fields = ['quantity']

class ProductQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

    def save(self):
        ProductServices.update_quantity(
            self.instance,
            self.validated_data['quantity']
        )

        self.instance.refresh_from_db()

        return self.instance

class ProductForNewOrderSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    quantity = serializers.IntegerField()

class NewOrderSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=ProductForNewOrderSerializer(),
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
    product_uid = serializers.UUIDField(source='product.uid')
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Ticket
        fields = [
            'uid',
            'product_uid',
            'product_name',
            'product_price',
            'consumed'
        ]

class TicketOrderSerializer(serializers.ModelSerializer):
    product_uid = serializers.UUIDField(source='product.uid')
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Ticket
        fields = [
            'product_uid',
            'product_name',
            'product_price',
        ]

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'uid',
            'status',
            'description',
            'payment_method',
            'original_value',
            'remaining_value',
            'tickets',
            'created_at'
        ]

class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'uid',
            'status',
            'description',
            'payment_method',
            'original_value',
            'remaining_value',
            'created_at',
        ]

class OrderWebhookSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    status = serializers.ChoiceField(choices=[Order.STATUS_CONFIRMED, Order.STATUS_CANCELED])

class ConsumingTokenSerializer(serializers.ModelSerializer):
    consuming_token_uid = serializers.UUIDField(source='uid')
    
    class Meta:
        model = ConsumingToken
        fields = ['consuming_token_uid', 'expired_at']

class ConsumeSerializer(serializers.Serializer):
    tickets = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        min_length=1
    )
