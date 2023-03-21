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


def create_customer(name: str, time_out: datetime.datetime = None, time_in_offset: int = 0) -> object:
    """
    Create customer. Provide 'name' only to simulate customer with
    active orders.
    Provide 'time_out' to simulate customer with
    inactive orders.
    Set 'time_in_offset' to positive int to offset customer time_in by
    number of minutes into the future, and to negative int to offset
    customer time_in by number of minutes into the past.
    """
    time_in = timezone.localtime() + datetime.timedelta(minutes=time_in_offset)
    customer = Customer.objects.create(name=name, time_in=time_in, time_out=time_out)
    return customer


class CustomerIndexViewTests(TestCase):
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
        customer1 = create_customer("Customer1", time_in_offset=-1)
        customer2 = create_customer("Customer2")
        response = self.client.get(reverse('store:index'))
        self.assertQuerysetEqual(response.context['customer_list'], [customer2, customer1])

    def test_future_customer(self):
        """
        Index page does not display customers with future time_in.
        """
        create_customer("Future customer", time_in_offset=1)
        url = reverse('store:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['customer_list'], [])
        self.assertContains(response, "No orders to display")


class CustomerDetailViewTests(TestCase):
    def test_future_customer(self):
        """
        The detail view of a customer with a time_in in the future
        returns a 404 not found.
        """
        future_customer = create_customer("Future customer", time_in_offset=1)
        url = reverse('store:customer', args=(future_customer.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_customer_with_active_orders(self):
        """
        The detail view of a customer with a time_in in the past
        and active orders displays customer name.
        """
        active_customer = create_customer("Active customer")
        url = reverse('store:customer', args=(active_customer.id,))
        response = self.client.get(url)
        self.assertContains(response, active_customer.name)
