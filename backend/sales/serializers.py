from rest_framework import serializers

from sales.models import Product, Order, Ticket

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uid', 'name', 'description', 'price', 'quantity']
        read_only_fields = ['quantity']

class ListProductsSerializer(serializers.Serializer):
    products = serializers.ListField(child=ProductSerializer())

class ProductQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

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
    
class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        return list(
            map(
                lambda po: {
                    'uid': str(po.uid),
                    'name': po.product.name,
                    'price': po.product_price,
                    'consumed': po.consumed
                },
                instance.productorder_set.all()
            )
        )

    class Meta:
        model = Order
        fields = ['uid', 'status', 'payment_method', 'original_value', 'remaining_value', 'products']

class TicketSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, instance):
        return instance.product.name

    class Meta:
        model = Ticket
        fields = ['uid', 'product_name', 'product_price', 'consumed']

class OrderWebhookSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    status = serializers.ChoiceField(choices=[Order.STATUS_CONFIRMED, Order.STATUS_CANCELED])

class ConsumeSerializer(serializers.Serializer):
    productorder_uid_list = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        min_length=1
    )
