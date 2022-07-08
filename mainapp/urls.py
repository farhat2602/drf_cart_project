from django.urls import path
from mainapp.views import (CartItemCreateView, login_view, CartDetailView, ProductListView,
                           CartItemDeleteView, CartItemQty, CheckoutView, CheckCoupon)


urlpatterns = [
    path('cart/<pk>/', CartDetailView.as_view()),
    path('product_list/', ProductListView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('check_coupon/', CheckCoupon.as_view()),
    path('add_to_cart/', CartItemCreateView.as_view()),
    path('remove_from_cart/<int:id>/', CartItemDeleteView.as_view()),
    path('cart_item_qty/', CartItemQty.as_view()),
    path('login/', login_view),
]