import pytest

from tests.test_app.models import Product


@pytest.fixture(autouse=True)
def products(db):
    Product.objects.create(
        name="Long-sleeve T-Shirts",
        price=15.5,
        category="C",
        description="2021 F/W",
    )
    Product.objects.create(
        name="Pizza",
        price=10.9,
        category="F",
        description="Pepperoni",
    )
    Product.objects.create(
        name="Coke",
        price=1.9,
        category="B",
        description="Zero Sugar",
    )
