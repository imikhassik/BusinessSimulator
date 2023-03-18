from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # displays all customers with orders
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:order_id>/fulfill/', views.fulfill, name='fulfill'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer'),
]
