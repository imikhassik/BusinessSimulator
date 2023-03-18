import datetime

from django.test import TestCase
from django.utils import timezone

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
