from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from custom_auth.permissions import (
    IsAdminAuthenticatedAndActivePermission,
    IsConsumerAuthenticatedAndActivePermission,
    IsDispatcherAuthenticatedAndActivePermission,
)
from sales.models import Product
from sales.serializers import (
    ConsumeSerializer,
    ConsumingTokenSerializer,
    NewOrderSerializer,
    OrderSerializer,
    OrderWebhookSerializer,
    ProductQuantitySerializer,
    ProductSerializer,
    TicketSerializer,
)
from sales.services import (
    OrderServices,
    WalletServices,
)

class ProductViewSet(ModelViewSet):
    lookup_field = 'uid'
    lookup_value_converter = 'uuid'

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'update_quantity':
            return ProductQuantitySerializer

        return ProductSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response({ 'products': response.data })
    
    @action(detail=True, methods=['patch'], url_path='quantity')
    def update_quantity(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'list':
            return super().get_permissions()

        return [IsAdminAuthenticatedAndActivePermission()]

class WalletViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='orders')
    def orders_action(self, request):
        serializer = NewOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = WalletServices.process_new_order(
            request.user,
            serializer.validated_data['products']
        )

        return Response({ 'order_uid': str(order.uid) })

    @action(detail=False, methods=['get'], url_path='tickets')
    def tickets(self, request):
        all_tickets = bool(request.query_params.get('all'))

        tickets_qs = WalletServices.get_tickets(request.user, all_tickets)
        serializer = TicketSerializer(tickets_qs, many=True)

        return Response({ 'tickets': serializer.data })

    @action(detail=False, methods=['get'], url_path='consuming-token')
    def generate_consuming_token(self, request):
        ct = WalletServices.get_or_create_consuming_token(request.user)

        return Response(ConsumingTokenSerializer(ct).data)

    @action(detail=False, methods=['get', 'post'], url_path='consume')
    def consume(self, request):
        consuming_token_uid = request.query_params.get('consuming_token_uid')

        consuming_token = WalletServices.get_consuming_token(consuming_token_uid)

        result = {}

        if request.method.lower() == 'get':
            consuming_token_user = consuming_token.wallet.user

            tickets_qs = WalletServices.get_tickets(
                consuming_token_user,
                wallet=consuming_token.wallet
            )
            serializer = TicketSerializer(tickets_qs, many=True)

            result.update({
                'name': consuming_token_user.name,
                'email': consuming_token_user.email,
                'tickets': serializer.data
            })

        else:
            serializer = ConsumeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            tickets_consumed = WalletServices.consume(
                request.user,
                consuming_token,
                serializer.validated_data['tickets']
            )

            result.update({ 'tickets': tickets_consumed })

        return Response(result)

    def get_permissions(self):
        if self.action == 'consume':
            return [IsDispatcherAuthenticatedAndActivePermission()]

        return [IsConsumerAuthenticatedAndActivePermission()]

class OrderViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='webhook')
    def webhook(self, request):
        serializer = OrderWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        OrderServices.webhook_handler(str(data['uid']), data['status'])

        return Response(status=204)
