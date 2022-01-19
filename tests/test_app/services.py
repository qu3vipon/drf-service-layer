from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

from drf_service_layer.services import Service
from tests.test_app.models import Product


@dataclass
class PriceDTO:
    currency: str


class ProductService(Service):
    @staticmethod
    def filter_currency_param(currency_param: str) -> str:
        if currency_param not in ["WON", "EUR"]:
            raise ValidationError("This currency is not supported.")
        return currency_param

    def adjust_price(self, instance: Product) -> float:
        self.dto: PriceDTO

        exchange_rate = {
            "WON": 1200,
            "EUR": 0.85,
        }

        return instance.price * exchange_rate[self.dto.currency]
