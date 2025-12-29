from django.shortcuts import render, get_object_or_404
from shop.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def cart_add(request, product_id):
    # Logic to add the product to the cart
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=1)
        context = {'cart_total_items': len(
            cart), 'cart_total_price': cart.get_total_price()}
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    # return render(request, 'cart/detail.html', context)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')

    print(
        f"Received update_quantity request - item_id: {item_id}, action: {action}")

    if not item_id or not action:
        return JsonResponse({
            'success': False,
            'error': 'Missing item_id or action parameter'
        }, status=400)

    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)

        if action == 'add':
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)
        else:
            return JsonResponse({
                'success': False,
                'error': f'Invalid action: {action}'
            }, status=400)

        context = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            # 'final_price': cart.get_final_price()
        }
        return JsonResponse(context)

    except Exception as e:
        print(f"Error in update_quantity: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

# 14040630


@require_POST
def remove_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'success': False, 'error': 'Missing item_id parameter'}, status=400)

        try:
            product = get_object_or_404(Product, id=item_id)
            cart = Cart(request)
            cart.remove(product)

            context = {
                'success': True,
                'item_count': len(cart),
                'total_price': cart.get_total_price(),
                # 'final_price': cart.get_final_price()
            }
            return JsonResponse(context)

        except Exception as e:
            print(f"Error in remove_item: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
