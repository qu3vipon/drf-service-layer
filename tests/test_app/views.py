from drf_service_layer.views import ListAPIView
from tests.test_app.models import Product
from tests.test_app.serializers import ProductSerializer
from tests.test_app.services import ProductService


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    service_class = ProductService
