from django.http import HttpResponse
from django.shortcuts import render

from .models import Order


def index(request):
    latest_order_list = Order.objects.order_by('-customer__time_in')[:5]
    context = {'latest_order_list': latest_order_list}
    return render(request, 'store/index.html', context)


def order_detail(request, order_id):
    return HttpResponse("You're viewing order %s detail" % order_id)


def fulfill(request, order_id):
    response = "This is order %s fulfillment page"
    return HttpResponse(response % order_id)


def customer(request, customer_id):
    return HttpResponse("You're viewing customer %s detail" % customer_id)
