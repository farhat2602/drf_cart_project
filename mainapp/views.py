from decimal import Decimal

from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.models import Cart, Product, CartItem, Order, OrderItem, Coupon
from mainapp.serializers import CartSerializer, OrderSerializer, ProductSerializer
from mainapp.utils import get_total_price


@api_view(['POST'])
def login_view(request):
    username = request.data['username']
    password_data = request.data['password']
    user = authenticate(request, username=username, password=password_data)
    login(request, user)
    return Response(status=status.HTTP_200_OK)



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class CartDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemCreateView(APIView):

    def post(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        product = Product.objects.get(id=request.data['product_id'])
        try:
            item = cart.cart_item.get(product=product)
            item.qty += 1
            if product.discount_price:
                item.total_price = item.qty * product.discount_price
            else:
                item.total_price = item.qty * product.price
            item.save()
            total = 0
            get_total_price(cart)
        except:
            if product.discount_price:
                new_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    qty=1,
                    total_price=product.discount_price
                )
                cart.total_price += new_item.total_price
            else:
                new_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    qty=1,
                    total_price=product.price
                )
                cart.total_price += new_item.total_price
            cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemDeleteView(APIView):

    def delete(self, request, id):
        cart = Cart.objects.get(user=request.user, is_active=True)
        item = cart.cart_item.get(id=id)
        item.delete()
        if cart.discount_total_price:
            total = cart.discount_total_price - item.total_price
            cart.discount_total_price = total
        else:
            total = cart.total_price - item.total_price
            cart.total_price = total
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemQty(APIView):
    # This class for increase and decrease CartItem-Product-Qty!
    def post(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        item = cart.cart_item.get(product=request.data['product_id'])
        qty = request.data['qty']
        if int(qty) > 0:
            if item.product.discount_price:
                price = item.product.discount_price * int(qty)
            else:
                price = item.product.price * int(qty)
            item.qty = qty
            item.total_price = price
            item.save()
            get_total_price(cart)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckoutView(APIView):

    def post(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        order, created = Order.objects.get_or_create(
            buyer=cart.user,
            price=cart.total_price,
        )
        if order:
            for item in cart.cart_item.all():
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=item.product.id),
                    qty=item.qty,
                    total_price=item.total_price
                )
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckCoupon(APIView):
    def post(self, request):
        coupon_data = request.data['coupon']
        if Coupon.objects.filter(coupon=coupon_data, is_active=True, user=request.user.id).exists():
            return Response(status=status.HTTP_423_LOCKED)
        elif Coupon.objects.filter(coupon=coupon_data, is_active=True).exists():
            coupon = Coupon.objects.get(coupon=coupon_data)
            coupon.user.add(request.user)
            cart = Cart.objects.get(user=request.user, is_active=True)
            price = Decimal(cart.total_price * (100 - coupon.discount) / 100)
            cart.discount_info = coupon.discount
            cart.discount_total_price = price
            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

# class CartItemQtyIncreaseView(APIView):
#
#     def post(self, request):
#         cart = Cart.objects.get(user=request.user, is_active=True)
#         try:
#             item = cart.cart_item.get(product=request.data['product_id'])
#             qty = item.qty + 1
#             if item.product.discount_price:
#                 price = item.total_price + item.product.discount_price
#             else:
#                 price = item.total_price + item.product.price
#             item.qty = qty
#             item.total_price = price
#             item.save()
#             total = 0
#             for i in cart.cart_item.all():
#                 total += i.total_price
#                 if cart.discount_total_price and cart.discount_total_price > 0:
#                     cart.discount_total_price = total
#                 else:
#                     cart.total_price = total
#                 cart.save()
#             serializer = CartSerializer(cart)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)


# class CartItemQtyDecreaseView(APIView):
#
#     def post(self, request, id):
#         cart = Cart.objects.get(user=request.user, is_active=True)
#         try:
#             item = cart.cart_item.get(product=request.data['product_id'])
#             if item.qty >= 2:
#                 qty = item.qty - 1
#                 if item.product.discount_price:
#                     price = item.total_price - item.product.discount_price
#                 else:
#                     price = item.total_price - item.product.price
#                 item.qty = qty
#                 item.total_price = price
#                 item.save()
#                 total = 0
#                 for i in cart.cart_item.all():
#                     total += i.total_price
#                     if cart.discount_total_price and cart.discount_total_price > 0:
#                         cart.discount_total_price = total
#                     else:
#                         cart.total_price = total
#                     cart.save()
#                 serializer = CartSerializer(cart)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message_error': 'Item, should be more than 1!'})
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#
# @api_view(['POST'])
# def remove_from_cart(request, id):
#     cart = Cart.objects.get(user=request.user, is_active=True)
#     item = cart.cart_item.get(id=id)
#     if cart.discount_total_price:
#         total1 = cart.total_price - item.total_price
#         total2 = cart.discount_total_price - item.total_price
#         cart.total_price = total1
#         cart.discount_total_price = total2
#         item.delete()
#     elif cart.total_price and cart.discount_total_price == 0:
#         total3 = cart.total_price - item.total_price
#         cart.total_price = total3
#         item.delete()
#     cart.save()
#     return Response(status=status.HTTP_200_OK)

