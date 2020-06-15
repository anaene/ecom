from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=12)

    class Meta:
        unique_together = ('street', 'city', 'postcode')
        verbose_name_plural = 'Addresses'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='images', blank=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=1)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class OrderStatus(models.TextChoices):
        PROCESSING = 'processing',
        COMPLETED = 'completed',
        CANCELLED = 'cancelled',
        FAILED = 'failed',

    order_status = models.CharField(max_length=12, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order Products'
