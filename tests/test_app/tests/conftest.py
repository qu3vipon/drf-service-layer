import pytest

from tests.test_app.models import Product


@pytest.fixture(autouse=True)
def instance(db):
    yield Product.objects.create(
        name="Long-sleeve T-Shirts",
        price=15.5,
        category="C",
        description="2021 F/W",
    )
