from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=50)
    time_in = models.DateTimeField()

    def __str__(self):
        return f'{self.name}'

    def wait_time(self):
        return (timezone.now() - self.time_in).seconds // 60


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f'#{self.id} for {self.amount} lbs of {self.product.lower()}'

    def get_total_cost(self):
        return self.price * self.amount
