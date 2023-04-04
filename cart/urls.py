from django.urls import path
from cart.views import *


app_name = 'cart'
urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
    path('remove-product/<int:product_id>/', remove_product, name='remove_product'),
    path('checkout/', checkout, name='checkout'),
]
