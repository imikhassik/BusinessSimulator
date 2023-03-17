from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),  # displays all customers with orders
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/fulfill/', views.fulfill, name='fulfill'),
    path('customer/<int:customer_id>/', views.customer, name='customer'),
]
