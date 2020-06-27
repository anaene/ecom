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
    path('products/<int:product_id>/', product_details, name='product')
]
