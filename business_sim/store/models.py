from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=50)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name}'

    def wait_time_over(self):
        self.time_out = timezone.localtime()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    amount = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)

    PROGRESS = 'PR'
    FULFILLED = 'FU'
    REJECTED = 'RE'
    STATUS_CHOICES = [
        (PROGRESS, 'In progress'),
        (FULFILLED, 'Fulfilled'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default=PROGRESS,
                              )

    def __str__(self):
        return f'#{self.id} for {self.amount} lbs of {self.product.lower()}'

    def get_total_cost(self):
        return self.price * self.amount
