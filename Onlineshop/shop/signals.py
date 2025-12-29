from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product
@receiver(pre_save, sender=Product)
def calculate_offer_price(sender, instance, **kwargs):
    if instance.off > 0:
        discount_amount = (instance.price * instance.off) / 100
        instance.offer_price = instance.price - discount_amount
    else:
        instance.offer_price = None