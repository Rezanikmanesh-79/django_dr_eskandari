from django.shortcuts import render
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    # request.session['phone'] = '1234567890'
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)
    print('cart:', request.session.get('cart', {}))
    return render(request, 'product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    product = Product.objects.get(id=id, slug=slug, available=True)
    
    return render(request, 'product/detail.html', {'product': product, 'phone': request.session.get('phone')})
# Create your views here.
