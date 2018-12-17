from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='guest-home'),
    path('menu/', views.menu, name='guest-menu'),
    path('order/', views.order, name='guest-order'),
    re_path(r'order-status/(?P<order_id>\w{1,50})/$', view=views.order_status, name='guest-order-status')
]