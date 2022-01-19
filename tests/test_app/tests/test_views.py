import pytest
from django.shortcuts import resolve_url
from rest_framework.test import APIClient
from schema import And, Schema

from drf_service_layer.services import Service
from tests.test_app.serializers import ErrorCaseSerializer
from tests.test_app.services import ProductService


class TestServiceAPIView:
    @pytest.mark.parametrize(
        "currency, adjusted_price",
        [
            ("WON", 15.5 * 1200),
            ("EUR", 15.5 * 0.85),
        ],
    )
    def test_product_retrieve(self, currency, adjusted_price):
        client = APIClient()
        url = resolve_url("product_retrieve_service", pk=1)

        query_param = {"currency": currency}
        response = client.get(url, query_param)

        schema = Schema(
            {
                "id": 1,
                "name": str,
                "price": adjusted_price,
                "category": And(str, lambda s: len(s) == 1),
                "description": str,
            }
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())

    @pytest.mark.parametrize(
        "currency, adjusted_price",
        [
            ("WON", 15.5 * 1200),
            ("EUR", 15.5 * 0.85),
        ],
    )
    def test_product_list(self, currency, adjusted_price):
        client = APIClient()
        url = resolve_url("product_list_service")

        query_param = {"currency": currency}
        response = client.get(url, query_param)

        schema = Schema(
            [
                {
                    "id": int,
                    "name": str,
                    "price": adjusted_price,  # return 1 instance
                    "category": And(str, lambda s: len(s) == 1),
                    "description": str,
                }
            ]
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())


# Original way of implementation


class TestDRFAPIView:
    @pytest.mark.parametrize(
        "currency, adjusted_price",
        [
            ("WON", 15.5 * 1200),
            ("EUR", 15.5 * 0.85),
        ],
    )
    def test_product_retrieve(self, currency, adjusted_price):
        client = APIClient()
        url = resolve_url("product_retrieve_original", pk=1)

        query_param = {"currency": currency}
        response = client.get(url, query_param)

        schema = Schema(
            {
                "id": 1,
                "name": str,
                "price": adjusted_price,
                "category": And(str, lambda s: len(s) == 1),
                "description": str,
            }
        )

        schema.validate(response.json())

        assert response.status_code == 200
        assert schema.is_valid(response.json())


# Error cases


class TestViewErrors:
    def test_service_class_not_defined(self):
        client = APIClient()
        url = resolve_url("product_retrieve_errors", pk=1)

        with pytest.raises(
            AssertionError,
            match=r".+ should either include a `service_class` attribute.",
        ):
            client.get(url)


class TestDecoratorErrors:
    def test_serializer_context(self, instance):
        with pytest.raises(
            AssertionError, match=r".+ should retrieve service context from view."
        ):
            ErrorCaseSerializer(instance)

    def test_service_class_match(self, instance):
        context = {"service": Service(None)}
        with pytest.raises(
            AssertionError,
            match=r".+ - The service injected from view and the service declared in the decorator are not the same..+",
        ):
            ErrorCaseSerializer(instance, context=context)

    def test_dto_match(self, instance):
        context = {"service": ProductService(None)}
        with pytest.raises(
            AssertionError,
            match=r".+ - The dto injected from view and the dto declared in the decorator are not matched..+",
        ):
            ErrorCaseSerializer(instance, context=context)
