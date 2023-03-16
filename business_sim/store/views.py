from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Order, Customer


def index(request):
    latest_order_list = Order.objects.order_by('customer__time_in')
    context = {'latest_order_list': latest_order_list}
    return render(request, 'store/index.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/order_detail.html', {'order': order})


def fulfill(request, order_id):
    response = "This is order %s fulfillment page"
    return HttpResponse(response % order_id)


def customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'store/customer.html', {'customer': customer})
