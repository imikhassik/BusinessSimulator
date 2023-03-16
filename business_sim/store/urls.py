from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),  # displays orders
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/fulfill/', views.fulfill, name='fulfill'),
    path('customer/<int:customer_id>/', views.customer, name='customer'),
]
