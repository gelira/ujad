from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from sales import serializers
from sales.models import Product, Wallet, Order, Ticket

class ProductViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        products = Product.objects.order_by('name').all()
        serializer = serializers.ListProductsSerializer({ 'products': products })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
    def partial_update(self, request, *args, **kwargs):
        product = Product.find_by_uid_or_404(kwargs['pk'])
        serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], url_path='quantity')
    def update_quantity(self, request, pk=None):
        serializer = serializers.ProductQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = Product.find_by_uid_or_404(pk)
        product.update_quantity(serializer.validated_data['quantity'])

        return Response(serializers.ProductSerializer(product).data)
    
    def destroy(self, request, *args, **kwargs):
        product = Product.find_by_uid_or_404(kwargs['pk'])
        product.delete()

        return Response(status=204)

class WalletViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='orders')
    def orders_action(self, request):
        serializer = serializers.NewOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Wallet.process_new_order(
            request.user,
            serializer.validated_data['products']
        )

        return Response(serializers.OrderSerializer(order).data)
    
    @action(detail=False, methods=['get'], url_path='tickets')
    def tickets(self, request):
        wallet = Wallet.get_or_create_wallet(request.user)
        
        serializer = serializers.TicketSerializer(
            wallet.get_tickets(),
            many=True
        )

        return Response({ 'tickets': serializer.data })
    
    @action(detail=True, methods=['get', 'post'], url_path='consume')
    def consume(self, request, pk=None):
        wallet = Wallet.find_by_uid_or_404(pk)

        result = { 'tickets': None }

        if request.method == 'GET':
            result['tickets'] = \
                serializers.TicketSerializer(wallet.get_tickets(), many=True).data
        
        else:
            serializer = serializers.ConsumeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result['tickets'] = Ticket.consume(wallet, serializer.validated_data['tickets'])

        return Response(result)

class OrderViewSet(ViewSet):
    def list(self, request):
        wallet = request.user.wallet_set.filter(is_active=True).first()

        result = { 'tickets': [] }

        if wallet and wallet.is_active:
            result['tickets'] = serializers.OrderSerializer(wallet.ticket_set.all(), many=True).data
        
        return Response(result)

    @action(detail=False, methods=['post'], url_path='webhook')
    def webhook(self, request):
        serializer = serializers.OrderWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        Order.webhook_handler(data['uid'], data['status'])

        return Response(status=204)
