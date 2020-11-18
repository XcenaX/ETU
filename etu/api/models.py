from django.db import models
from django.conf import settings
from django.utils import timezone
import os

class Role(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class User(models.Model):
    email = models.TextField(default='') 
    password = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name

class Item(models.Model):
    item_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(default="")  
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name
    
