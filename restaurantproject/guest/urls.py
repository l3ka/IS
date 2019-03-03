from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='guest-home'),
    re_path(r'menu/$', views.menu, name='guest-menu'),
    path('sw.js', views.serviceworker, name='serviceworker'),
    path('manifest.json', views.appmanifest, name='appmanifest'),
    path('localforage.min.js', views.localforage, name='localforage'),
    re_path(r'menu/additions/(?P<menu_item_id>\w{1,50})/$', view=views.menu_item_additions, name='guest-order-status'),
    re_path(r'order/$', views.add_order, name='guest-order'),
    re_path(r'order/(?P<order_id>\w{1,50})/$', view=views.order, name='guest-order'),
    re_path(r'order-status/(?P<order_id>\w{1,50})/$', view=views.order_status, name='guest-order-status'),
    path('promotions/', views.promotions, name='guest-promotions'),
    path('call-bartender/', views.call_bartender, name='call-bartender'),
    path('logout/', views.logout_view, name='logout')
]