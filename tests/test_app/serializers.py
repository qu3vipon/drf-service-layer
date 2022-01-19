from rest_framework import serializers

from drf_service_layer.services import service_layer
from tests.test_app.models import Product
from tests.test_app.services import PriceDTO, ProductService


@service_layer(ProductService, PriceDTO)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["price"] = self.service.adjust_price(instance)
        return representation


# Original way of implementation


class DRFProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# Error cases


@service_layer(ProductService, PriceDTO)
class ErrorCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
