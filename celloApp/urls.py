from django.conf.urls import url
from django.urls import path
from celloApp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('order/', views.order, name='order'),
    path('downloads/', views.downloads, name='downloads'),
    path('rawMaterial/', views.rawMaterial, name='rawMaterial'),
    path('allOrders/', views.allOrders, name='allOrders'),
    path('edit_customer/<pk>', views.edit_customer, name='edit_customer'),
]
