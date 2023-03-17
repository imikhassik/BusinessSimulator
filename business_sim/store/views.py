from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Order, Customer


def index(request):
    customer_list = Customer.objects.all()
    return render(request, 'store/index.html', {'customer_list': customer_list})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/order_detail.html', {'order': order})


def fulfill(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    try:
        order_status = request.POST['fulfillment']
    except KeyError:
        return render(request, 'store/order_detail.html', {
            'order': order,
            'error_message': "You didn't select an action."
        })
    else:
        order.status = order_status
        order.save()
    return HttpResponseRedirect(reverse('store:index'))


def customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'store/customer.html', {'customer': customer})
