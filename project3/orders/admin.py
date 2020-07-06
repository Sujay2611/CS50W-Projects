from django.contrib import admin

# Register your models here.
from .models import RegularPizza, SicilianPizza, Pasta, Salad, DinnerPlatter, Sub, Extra, Topping, Item, Order

admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(Pasta)
admin.site.register(DinnerPlatter)
admin.site.register(Sub)
admin.site.register(Salad)
admin.site.register(Extra)
admin.site.register(Topping)
admin.site.register(Item)
admin.site.register(Order)
