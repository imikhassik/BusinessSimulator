import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Customer


class CustomerModelTests(TestCase):
    def test_waiting_too_long_with_over_one_minute_wait(self):
        """
        waiting_too_long() returns True with customers waiting over 1 minute
        """
        time = timezone.localtime() - datetime.timedelta(minutes=1, seconds=1)
        customer = Customer(time_in=time)
        self.assertIs(customer.waiting_too_long(), True)

    def test_waiting_too_long_with_under_one_minute_wait(self):
        """
        waiting_too_long() returns False with customers waiting under 1 minute
        """
        time = timezone.localtime() - datetime.timedelta(seconds=59)
        customer = Customer(time_in=time)
        self.assertIs(customer.waiting_too_long(), False)


def create_customer(name: str, time_in=timezone.localtime(), time_out: datetime.datetime = None) -> object:
    """
    Create customer. Provide 'name' only to simulate customer with active
    orders. Provide 'time_out' to simulate customer with inactive orders.
    :param name: string
    :param time_in: defaults to timezone.localtime()
    :param time_out: defaults to None
    :return: Customer object
    """
    customer = Customer.objects.create(name=name, time_in=time_in, time_out=time_out)
    return customer


class IndexViewTests(TestCase):
    def test_customer_with_active_orders(self):
        """
        Customer with active orders is displayed on index page.
        """
        customer = create_customer(name='Customer with active orders')
        response = self.client.get(reverse('store:index'))
        self.assertQuerysetEqual(response.context['customer_list'], [customer])

    def test_customer_with_inactive_orders(self):
        """
        Customer with inactive orders is not displayed on index
        page. "No orders to display" is displayed when there are
        no customers with active orders.
        """
        create_customer(name='Customer with inactive orders', time_out=timezone.localtime())
        response = self.client.get(reverse('store:index'))
        self.assertQuerysetEqual(response.context['customer_list'], [])
        self.assertContains(response, "No orders to display")

    def test_customers_with_active_and_inactive_orders(self):
        """
        Even if both customer with active and customer with
        inactive orders exist, only customer with active orders
        is displayed on index page.
        """
        customer_active = create_customer(name='Active')
        create_customer(name='Inactive', time_out=timezone.localtime())
        response = self.client.get(reverse('store:index'))
        self.assertQuerysetEqual(response.context['customer_list'], [customer_active])

    def test_multiple_customers_with_active_orders(self):
        """
        Index page displays all customers with active orders.
        """
        customer1 = create_customer("Customer1")
        customer2 = create_customer("Customer2", time_in=timezone.localtime()+datetime.timedelta(seconds=1))
        response = self.client.get(reverse('store:index'))
        self.assertQuerysetEqual(response.context['customer_list'], [customer2, customer1])
