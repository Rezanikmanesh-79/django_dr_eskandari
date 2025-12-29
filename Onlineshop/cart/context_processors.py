from .cart import Cart


def cart(request):
    cart = Cart(request)
    return {
        'cart_item_count': len(cart),
        'cart_total_price': cart.get_total_price(),
    }
