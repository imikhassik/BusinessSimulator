from django.http import HttpResponse


def index(request):
    return HttpResponse("You're at store's index page.")


def order_detail(request, order_id):
    return HttpResponse("You're viewing order %s detail" % order_id)


def fulfill(request, order_id):
    response = "This is order %s fulfillment page"
    return HttpResponse(response % order_id)


def customer(request, customer_id):
    return HttpResponse("You're viewing customer %s detail" % customer_id)
