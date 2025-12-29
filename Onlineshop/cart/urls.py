from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('detail/', views.cart_detail, name='cart_detail'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),

    path('remove_item/', views.remove_item, name='remove_item'),
]
