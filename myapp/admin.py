from django.contrib import admin
from myapp.models import Pet, Cart, Order

class petAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'breed', 'type', 'price', 'gender', 'description', 'petimage']
    list_filter = ['type', 'price']

admin.site.register(Pet, petAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['id', 'uid', 'petid', 'quantity']
admin.site.register(Cart, CartAdmin )


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'orderid', 'petid', 'userid', 'quantity']
    list_filter = ['petid', 'userid']

admin.site.register(Order, OrderAdmin)