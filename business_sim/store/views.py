from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Order, Customer


class IndexView(generic.ListView):
    model = Customer
    template_name = 'store/index.html'


class OrderDetailView(generic.DetailView):
    model = Order


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'store/customer.html'


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
        all_orders_fulfilled = 0
        for order in order.customer.order_set.all():
            if order.status == 'PR':
                all_orders_fulfilled = 0
                break
            else:
                all_orders_fulfilled = 1
        if all_orders_fulfilled:
            order.customer.wait_time_over()
            order.customer.save()
    return HttpResponseRedirect(reverse('store:index'))
