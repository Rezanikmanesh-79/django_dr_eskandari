from django.db import models
# from django_jalali.db import models as jmodels
from shop.models import Product
# from account.models import ShopUser


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_code = models.CharField(max_length=100, blank=True, null=True)
    # buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.SET_NULL, null=True)

    # total_price = models.DecimalField(default=0)
    # discount = models.DecimalField(default=0)
    # final_price = models.DecimalField(default=0)

    def __str__(self):
        return f"Order {self.id} - {self.first_name}"
    def get_total_cost(self):
        return sum(item.get_total_cost() for item in self.items.all())
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
    def get_cost(self):
        return self.price * self.quantity
    def get_weight(self):
        return self.weight * self.quantity
    
    def get_post_cost(self):
        weight = self.get_weight()
        if weight <= 1000:
            return 30000
        elif weight <= 2000:
            return 35000
        elif weight <= 3000:
            return 40000
        elif weight <= 4000:
            return 45000
        elif weight <= 5000:
            return 50000
        else:
            extra_weight = self.get_weight() - 5000
            extra_cost = (extra_weight // 1000) * 10000
            if extra_weight % 1000 > 0:
                extra_cost += 10000
            return 50000 + extra_cost
        
    def get_total_cost(self):
        return self.get_cost() + self.get_post_cost()   
#     def total_price(self):