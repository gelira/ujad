from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from sales import serializers
from sales.models import Product

class ProductViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = serializers.ListProductsSerializer({ 'products': products })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
    def update(self, request, *args, **kwargs):
        product = Product.find_by_uid_or_404(kwargs['pk'])
        serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='quantity')
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
    @action(detail=False, methods=['post'], url_path='purchase')
    def purchase(self, request):
        serializer = serializers.PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

        return Response(status=204)
