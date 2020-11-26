from django.db import models
from django.conf import settings
from django.utils import timezone
import os

DEFAULT_CONDITION_ID = 1

class Role(models.Model):
    name = models.TextField(default='') 

    def __str__(self):
        return self.name

class User(models.Model):
    email = models.TextField(default='') 
    password = models.TextField(default='')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    company_name = models.TextField(default='') 
    def __str__(self):
        return self.email

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
    latitude = models.DecimalField(decimal_places=6, max_digits=9, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=9, blank=True, null=True)

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name

class Item(models.Model):
    image = models.ImageField(upload_to="items_images", blank=True)
    item_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(default="")  
    receive_date = models.DateTimeField(blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    rfid = models.TextField(default="")  
    def __str__(self):
        return self.name

class Document(models.Model):
    image = models.FileField(upload_to="items_documents", blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, default=DEFAULT_CONDITION_ID)

    def __str__(self):
        return str(self.id)

class ItemToBuy(models.Model):
    image = models.ImageField(upload_to="items_to_buy_images", blank=True)
    item_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    name = models.TextField(default="")  
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.name

class Purchased_Item(models.Model):
    item = models.ForeignKey(ItemToBuy, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)
    def get_total_price(self):
        return self.item.price * self.count

    def __str__(self):
        return self.item.name

class Purchase(models.Model):
    purchased_items = models.ManyToManyField(Purchased_Item, blank=True, null=True)
    purchase_start_date = models.DateTimeField(default=timezone.now)
    purchase_end_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def total_price(self):
        price = 0
        for purchased_item in self.purchased_items.all():
            price += purchased_item.get_total_price()

    def __str__(self):
        return self.owner.email

class Bag(models.Model):
    items = models.ManyToManyField(Purchased_Item, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def count_of_items(self):
        count = 0
        for purchased_item in self.items.all():
            count += purchased_item.count
        return count

    def sum_of_items(self):
        sum = 0
        for purchased_item in self.items.all():
            sum += purchased_item.get_total_price()
        return sum

    def __str__(self):
        return self.owner.email


class Driver(models.Model):
    fullname = models.TextField(default="")
    phone = models.TextField(default="")
    car_number = models.TextField(default="")

    def __str__(self):
        return self.fullname


class Order(models.Model):
    status = models.BooleanField(default=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    order_date = models.DateField(blank=True, null=True) 
    city = models.TextField(default="")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    client_name = models.TextField(default="")

    def __str__(self):
        responce = self.city + ", " + self.driver.fullname
        return responce


class Feedback(models.Model):
    image = models.ImageField(upload_to="feedback_images", default="empty.png")
    message = models.TextField(default="")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)






    
