from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from custom_auth import permissions
from sales import serializers, models
from sales.models import Product

class ProductViewSet(ModelViewSet):
    lookup_field = 'uid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'update_quantity':
            return serializers.ProductQuantitySerializer

        return serializers.ProductSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response({ 'products': response.data })
    
    @action(detail=True, methods=['patch'], url_path='quantity')
    def update_quantity(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            return super().get_permissions()

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

        return Response(serializers.ConsumingTokenSerializer(ct).data)

    @action(detail=False, methods=['get', 'post'], url_path='consume')
    def consume(self, request):
        ct_uid = request.query_params.get('consuming_token_uid')

        ct = models.ConsumingToken.find_by_uid_or_404(ct_uid)

        result = {}

        if request.method == 'GET':
            u = ct.wallet.user

            serializer = serializers.TicketSerializer(
                ct.wallet.get_tickets(),
                many=True
            )

            result.update({
                'name': u.name,
                'email': u.email,
                'tickets': serializer.data
            })
        
        else:
            serializer = serializers.ConsumeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tickets_consumed = ct.consume(
                request.user,
                serializer.validated_data['tickets']
            )

            result.update({ 'tickets': tickets_consumed })

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

        models.Order.webhook_handler(str(data['uid']), data['status'])

        return Response(status=204)
