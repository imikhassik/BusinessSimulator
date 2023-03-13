from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)


class Baskets(models.Model):
    cost = models.FloatField(default=0.0)
    products = models.ManyToManyField(Products, related_name='baskets')


class Customers(models.Model):
    name = models.CharField(max_length=255)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True)
    basket = models.ForeignKey(Baskets, on_delete=models.CASCADE)
