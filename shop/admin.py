from django.contrib import admin


from shop.models import Product
from .models import Contact
from .models import Orders
from .models import Orderupdate
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'desc']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'Address', 'city', 'state', 'Zip_code',)



admin.site.register(Contact, ContactAdmin)
admin.site.register(Product)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Orderupdate)




#
# # "models.py"
#
# from django.db import models
# from django.contrib import admin
#
# class Category(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name
#
#     # Here
#     @admin.display(description='products')
#     def get_products(self):
#         return [product.name for product in self.product_set.all()]
#
# class Product(models.Model):
#     categories = models.ManyToManyField(Category)
#     name = models.CharField(max_length=50)
#     price = models.DecimalField(decimal_places=2, max_digits=5)
#
#     # Here
#     @admin.display(description='categories')
#     def get_categories(self):
#         return [category.name for category in self.categories.all()]
# Then, set them to list_display in Category and Product admins respectively as shown below:
#
# # "admin.py"
#
# ...
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'get_products')
#     ordering = ('id',)            # Here
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):      # Here
#     list_display = ('id', 'name', 'price', 'get_categories')
#     ordering = ('id',)