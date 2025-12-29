from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-list-by-category', args=[self.slug])

    class Meta:
        verbose_name_plural = "دسته‌بندی‌ها"
        verbose_name = "دسته‌بندی"
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug'], name='category_slug_idx'),
        ]


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    off = models.PositiveIntegerField(default=0, verbose_name="درصد تخفیف")
    offer_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='قیمت بعد از تخفیف')
    slug = models.SlugField(unique=True)
    weight = models.PositiveIntegerField(
        verbose_name='وزن کالا (گرم)', default=0)

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name

    # متد جدید: قیمت نمایش (با تخفیف یا بدون تخفیف)
    def get_display_price(self):
        return self.offer_price if self.offer_price is not None else self.price

    # متد جدید: آیا تخفیف دارد؟
    def has_discount(self):
        return self.off > 0

    # متد جدید: درصد تخفیف
    def get_discount_percentage(self):
        return self.off if self.off > 0 else None

    class Meta:
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='product_name_idx'),
            models.Index(fields=['-created'], name='product_created_idx'),
        ]


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, related_name='features', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=255)
    feature_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.feature_name}: {self.feature_value}"

    class Meta:
        verbose_name_plural = "ویژگی‌های محصول"
        verbose_name = "ویژگی محصول"
        ordering = ['feature_name']
        indexes = [
            models.Index(fields=['feature_name'], name='feature_name_idx'),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name_plural = "تصاویر محصول"
        verbose_name = "تصویر محصول"
        ordering = ['product']
        indexes = [
            models.Index(fields=['product'], name='product_image_idx'),
        ]
