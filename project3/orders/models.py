from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.
class RegularPizza(models.Model):
    name = models.CharField(max_length = 20)
    price_small = models.FloatField()
    price_large = models.FloatField()
    no_of_toppings = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price_small} {self.price_large} {self.no_of_toppings}"

class SicilianPizza(models.Model):
    name = models.CharField(max_length = 20)
    price_small = models.FloatField()
    price_large = models.FloatField()
    no_of_toppings = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price_small} {self.price_large} {self.no_of_toppings}"

class Pasta(models.Model):
    name = models.CharField(max_length = 30)
    price = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price}"

class Salad(models.Model):
    name = models.CharField(max_length = 30)
    price = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price}"

class DinnerPlatter(models.Model):
    name = models.CharField(max_length = 20)
    price_small = models.FloatField()
    price_large = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price_small} {self.price_large}"

class Sub(models.Model):
    name = models.CharField(max_length = 30)
    price_small = models.FloatField(blank = True, null = True)
    price_large = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price_small} {self.price_large}"

class Extra(models.Model):
    name = models.CharField(max_length = 20)
    price = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.price}"

class Topping(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.id} - {self.name}"

class SignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    size = models.CharField(max_length = 10,blank = True, null = True)
    price = models.FloatField()
    toppings = models.CharField(max_length = 40,blank = True, null = True)
    extras =models.CharField(max_length = 40,blank = True, null = True)
    quantity=models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.name} {self.size} {self.price} {self.toppings} {self.extras} {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Item,related_name='order')
    subtotal = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.user} {self.items.all()} {self.subtotal}"
