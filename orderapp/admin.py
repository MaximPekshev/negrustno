from django.contrib import admin

from .models import Order, Order_Item


class Order_ItemInline(admin.TabularInline):
    model = Order_Item

    extra = 0

class OrderAdmin(admin.ModelAdmin):
	list_display = (

					'date',
					'order_number', 
					'first_name',
					'last_name',
					'phone',
					'email',
					'summ',
					)
	
	inlines 	 = [Order_ItemInline]

admin.site.register(Order, OrderAdmin)

