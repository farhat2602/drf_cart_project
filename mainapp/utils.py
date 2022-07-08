

def get_total_price(cart):
    total = 0
    for i in cart.cart_item.all():
        total += i.total_price
        if cart.discount_total_price and cart.discount_total_price > 0:
            cart.discount_total_price = total
        else:
            cart.total_price = total
        cart.save()