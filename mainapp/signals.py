from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from mainapp.models import Cart, CartItem, Order

User = get_user_model()


# create cart when User created!
@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Order)
def recreate_cart(sender, instance, created, **kwargs):
    if created:
        instance.cart = Cart.objects.filter(user=instance.buyer)
        instance.cart.update(is_active=False)
        if instance.cart:
            Cart.objects.create(user=instance.buyer)

#
# @receiver(post_save, sender=CartItem)
# def get_total_price(sender, instance, created, **kwargs):
#     instance_cart = Cart.objects.get(user=instance.cart.user, is_active=True)
#     total = 0
#     if instance_cart.discount_total_price:
#         for item in instance_cart.cart_item.all():
#             total += item.total_price
#             instance_cart.total_price = total
#             instance_cart.discount_total_price = total
#             instance_cart.save()
#         else:
#             for item in instance_cart.cart_item.all():
#                 total += item.total_price
#                 instance_cart.total_price = total
#                 instance_cart.save()

# @receiver(pre_delete, sender=CartItem)
# def get_total_del_price(sender, instance, **kwargs):
#     instance_cart = Cart.objects.get(user=instance.cart.user, is_active=True)
#     if instance_cart.discount_total_price:
#         total1 = instance_cart.total_price - instance.total_price
#         total2 = instance_cart.discount_total_price - instance.total_price
#         instance_cart.total_price = total1
#         instance_cart.discount_total_price = total2
#     elif instance_cart.total_price and instance_cart.discount_total_price == 0:
#         total3 = instance_cart.total_price - instance.total_price
#         instance_cart.total_price = total3
#     instance_cart.save()
