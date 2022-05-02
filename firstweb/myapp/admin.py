from django.contrib import admin
from .models import *

admin.site.site_header = 'Phenomenal Shop'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'Phenomenal Shop Backend'


class AllproductAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'price', 'detail', 'instock', 'quantity']
	list_editable = ['name', 'price', 'detail', 'instock', 'quantity']


admin.site.register(Allproduct, AllproductAdmin)


class ProfileAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'photo', 'usertype', 'cartquan']


admin.site.register(Profile, ProfileAdmin)


class CartAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'productid',
					'productname', 'price', 'quantity', 'total', 'stamp']


admin.site.register(Cart, CartAdmin)


class CatagoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'catagoryname', 'detail']


admin.site.register(Catagory, CatagoryAdmin)


class OrderListAdmin(admin.ModelAdmin):
	list_display = ['id', 'orderid', 'productid',
					'productname', 'price', 'quantity', 'total']


admin.site.register(OrderList, OrderListAdmin)


class OrderPendingtAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'name', 'tel', 'address', 'shipping',
					'payment', 'stamp', 'paid', 'slip', 'sliptime', 'paymentid']


admin.site.register(OrderPending, OrderPendingtAdmin)
admin.site.register(VerifyEmail)
