from django.contrib import admin
from .models import (customer,Product,Cart,orderplaced,profile)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','state','zipcode']

@admin.register(Product)
class productModelAdmin(admin.ModelAdmin):
    list_display=['id','titile','product_name','price','dec','category','product_img']

@admin.register(Cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity']

@admin.register(orderplaced)
class orderplacedModelAdmin(admin.ModelAdmin):
    list_display=['user','customer','product','quantity','order_date','status']


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['username']

@admin.register(profile)
class profileadmin(admin.ModelAdmin):
    list_display=['photo']