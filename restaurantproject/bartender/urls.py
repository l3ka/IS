from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.orders_screen, name='bartender-orders'),
    path('orders/', views.orders, name='orders'),
    path('login/', auth_views.LoginView.as_view(template_name='bartender/login.html'), name='bartender-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='guest/home.html'), name='bartender-logout')
]

# TODO: Da li je bolje na neko drugo mjesto ga redirect pri logout?