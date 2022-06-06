from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


CATEGORY_CHOICES = (("C", "Clothes"), ("F", "Food"), ("B", "Beverage"))

ORDER_STATUS_CHOICES = (
    (-1, "Canceled"),
    (0, "Pending"),
    (1, "Ready for delivery"),
    (2, "Shipped"),
    (3, "Received"),
)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    description = models.TextField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    status = models.SmallIntegerField(choices=CATEGORY_CHOICES)


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
