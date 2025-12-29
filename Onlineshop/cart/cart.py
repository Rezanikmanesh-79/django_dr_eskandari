# cart/cart.py

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        display_price = product.get_display_price()  # همیشه قیمت درست

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(display_price),
                'weight': product.weight
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def decrease(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= quantity
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            item = cart[str(product.id)]
            item['product'] = product
            # همیشه قیمت به‌روز از دیتابیس
            item['price'] = float(product.get_display_price())
            item['total_price'] = item['price'] * item['quantity']

        for item in cart.values():
            if 'product' in item:  # فقط آیتم‌های معتبر
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def post_price(self):
        weight = sum(item['weight'] * item['quantity']
                     for item in self.cart.values())
        if weight == 0:
            return 0
        elif weight <= 1000:
            return 10000
        elif weight <= 5000:
            return 20000
        else:
            return 50000

    def get_total_price(self):
        total_items = sum(float(item['price']) * item['quantity']
                          for item in self.cart.values())
        return total_items + self.post_price()
