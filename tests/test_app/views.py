from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf_service_layer import views
from tests.test_app.models import Product
from tests.test_app.serializers import DRFProductSerializer, ProductSerializer
from tests.test_app.services import PriceDTO, ProductService


class ProductRetrieveView(views.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    service_class = ProductService

    @property
    def dto(self):
        currency_param = self.request.query_params.get("currency", "WON")
        currency = self.pre_service.filter_currency_param(currency_param)

        return PriceDTO(
            currency=currency,
        )


class ProductListView(views.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    service_class = ProductService

    @property
    def dto(self):
        currency_param = self.request.query_params.get("currency", "WON")
        currency = self.pre_service.filter_currency_param(currency_param)

        return PriceDTO(
            currency=currency,
        )


# Original way of implementation


class DRFProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DRFProductSerializer

    def retrieve(self, request, *args, **kwargs):
        currency_param = self.request.query_params.get("currency", "WON")
        if currency_param not in ["WON", "EUR"]:
            raise ValidationError("This currency is not supported.")

        currency = currency_param

        exchange_rate = {
            "WON": 1200,
            "EUR": 0.85,
        }

        instance = self.get_object()
        instance.price = instance.price * exchange_rate[currency]

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# Error cases


class ErrorCaseView(views.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
