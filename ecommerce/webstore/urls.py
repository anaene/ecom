from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('account/', account, name='account'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                template_name='webstore/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset'),
    path('register/', register, name='register'),
    path('products/<int:product_id>/', product_details, name='product'),
    path('add/<int:product_id>/', add_to_cart, name='add'),
    path('checkout/', checkout, name='checkout'),
    path('remove/<int:product_id>', remove_cart_product, name='remove'),
    path('update/order/product/', update_order_product, name='update_product'),
    path('checkout/confirmation', process_checkout, name='confirm_checkout'),
    path('address/', get_customer_address, name='get_address')
]
