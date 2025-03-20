from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from sales.serializers import ListProductsSerializer, ProductSerializer
from sales.models import Product

class ProductViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ListProductsSerializer({ 'products': products })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)
    
    def update(self, request, *args, **kwargs):
        product = Product.find_by_uid_or_404(kwargs['pk'])
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='quantity')
    def update_quantity(self, request, pk=None):
        product = Product.find_by_uid_or_404(pk)
        
