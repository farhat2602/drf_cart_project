from django.contrib import admin

from mainapp.models import Product, Cart, CartItem, Order, OrderItem, Coupon


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
