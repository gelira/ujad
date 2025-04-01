from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from custom_auth import permissions
from sales import serializers, models

class ProductViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        products = models.Product.objects.order_by('name').all()
        serializer = serializers.ProductSerializer(products, many=True)

        return Response({ 'products': serializer.data })

    def create(self, request, *args, **kwargs):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
    def partial_update(self, request, *args, **kwargs):
        product = models.Product.find_by_uid_or_404(kwargs['pk'])
        serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], url_path='quantity')
    def update_quantity(self, request, pk=None):
        serializer = serializers.ProductQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = models.Product.find_by_uid_or_404(pk)
        product.update_quantity(serializer.validated_data['quantity'])

        return Response(serializers.ProductSerializer(product).data)
    
    def destroy(self, request, *args, **kwargs):
        product = models.Product.find_by_uid_or_404(kwargs['pk'])
        product.delete()

        return Response(status=204)
    
    def get_permissions(self):
        if self.action == 'list':
            return []

        return [permissions.IsAdminAuthenticatedAndActivePermission()]

class WalletViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='orders')
    def orders_action(self, request):
        serializer = serializers.NewOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = models.Wallet.process_new_order(
            request.user,
            serializer.validated_data['products']
        )

        return Response(serializers.OrderSerializer(order).data)
    
    @action(detail=False, methods=['get'], url_path='tickets')
    def tickets(self, request):
        all = bool(request.query_params.get('all'))

        wallet = models.Wallet.get_or_create_wallet(request.user)
        
        serializer = serializers.TicketSerializer(
            wallet.get_tickets(all),
            many=True
        )

        return Response({ 'tickets': serializer.data })
    
    @action(detail=False, methods=['get'], url_path='consuming-token')
    def generate_consuming_token(self, request):
        wallet = models.Wallet.get_or_create_wallet(request.user)
        
        ct = models.ConsumingToken.get_or_create_consuming_token(wallet)

        return Response({ 'consuming_token_uid': str(ct.uid) })

    @action(detail=False, methods=['get', 'post'], url_path='consume')
    def consume(self, request):
        ct_uid = request.query_params.get('consuming_token_uid')

        ct = models.ConsumingToken.find_by_uid_or_404(ct_uid)

        result = { 'tickets': None }

        if request.method == 'GET':
            result['tickets'] = serializers.TicketSerializer(
                ct.wallet.get_tickets(),
                many=True
            ).data
        
        else:
            serializer = serializers.ConsumeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result['tickets'] = ct.consume(
                request.user,
                serializer.validated_data['tickets']
            )

        return Response(result)
    
    def get_permissions(self):
        if self.action == 'consume':
            return [permissions.IsDispatcherAuthenticatedAndActivePermission()]

        return [permissions.IsConsumerAuthenticatedAndActivePermission()]

class OrderViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='webhook')
    def webhook(self, request):
        serializer = serializers.OrderWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        models.Order.webhook_handler(data['uid'], data['status'])

        return Response(status=204)
