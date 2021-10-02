from django.shortcuts import resolve_url
from rest_framework.test import APIClient
from schema import And, Schema


class TestGenericServiceAPIView:
    def test_product_list(self):
        client = APIClient()
        url = resolve_url("product_list")
        response = client.get(url)

        schema = Schema(
            [
                {
                    "id": int,
                    "name": str,
                    "price": float,
                    "category": And(str, lambda s: len(s) == 1),
                    "description": str,
                }
            ]
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())
