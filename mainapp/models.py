from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount_info = models.IntegerField(null=True, blank=True)
    discount_total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    PAY_CHOICES = (
        ('Card', ("Card")),
        ('Cash', ("Cash")),
    )
    payment_method = models.CharField(max_length=128, choices=PAY_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    qty = models.IntegerField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2)


class Coupon(models.Model):
    user = models.ManyToManyField(User, null=True, blank=True)
    coupon = models.CharField(max_length=16)
    discount = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
