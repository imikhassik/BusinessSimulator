from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Order, Customer


def index(request):
    customer_list = Customer.objects.all()
    return render(request, 'store/index.html', {'customer_list': customer_list})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/order_detail.html', {'order': order})


def fulfill(request, order_id):
    response = "This is order %s fulfillment page"
    return HttpResponse(response % order_id)


def customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'store/customer.html', {'customer': customer})
