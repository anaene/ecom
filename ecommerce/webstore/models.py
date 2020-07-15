import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=60, blank=True)
    postcode = models.CharField(max_length=12)

    class Meta:
        unique_together = ('street', 'city', 'postcode')
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '{}, {}, {}'.format(self.street, self.city, self.postcode)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='images', blank=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=1)

    @classmethod
    def limited_items(cls, i):
        return cls.objects.all().order_by('stock')[:i]

    @classmethod
    def sort_by_name_desc(cls):
        return cls.objects.all().order_by('-name')

    @classmethod
    def sort_by_name(cls):
        return cls.objects.all().order_by('name')

    @classmethod
    def sort_by_price_desc(cls):
        return cls.objects.all().order_by('-price')

    @classmethod
    def sort_by_price(cls):
        return cls.objects.all().order_by('price')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    class OrderStatus(models.TextChoices):
        PROCESSING = 'processing',
        COMPLETED = 'completed',
        CANCELLED = 'cancelled',
        FAILED = 'failed',

    order_status = models.CharField(max_length=12, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return 'transaction no: {}'.format(self.transaction_id)

    def get_total(self):
        order_products = OrderProduct.objects.filter(order=self)
        return sum([op.subtotal for op in order_products])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    QUANTITY_OPTIONS = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )

    quantity = models.IntegerField(choices=QUANTITY_OPTIONS, default=1)
    subtotal = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subtotal = self.product.price * self.quantity

    class Meta:
        verbose_name_plural = 'Order Products'

    def __str__(self):
        return 'product: {}, quantity = {}'.format(self.product.__str__(), self.quantity)
