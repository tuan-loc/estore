from django.urls import path
from customer.views import *


app_name = 'customer'
urlpatterns = [
    path('login/', login_customer, name='login'),
    path('login-2/', login_customer_2, name='login_2'),
    path('logout/', logout_customer, name='logout'),
    path('users/', users, name='users'),
    path('logout-user/', logout_user, name='logout_user'),
    path('my-account/', my_account, name='my_account'),
]
