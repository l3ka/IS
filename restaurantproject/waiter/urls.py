from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.waiter_view, name='waiter-view'),
    path('calls', views.calls, name='waiter-calls'),
    path('login', auth_views.LoginView.as_view(template_name='bartender/login.html'), name='bartender-login'),
    path('logout', auth_views.LogoutView.as_view(template_name='guest/home.html'), name='bartender-logout')
]