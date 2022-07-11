# urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
	path('', Home, name='home-page'),
	path('about/', About, name='about-page'),
	path('contact/', Contact, name='contact-page'),
	path('addproduct/', AddProduct, name='addproduct-page'),
	path('allproduct/', Product, name='allproduct-page'),
	path('register/', Register, name='register-page'),
	path('addtocart/<int:pid>/', AddtoCart, name='addtocart-page'),
	path('mycart/', MyCart, name='mycart-page'),
	path('mycartedit/', MyCartEdit, name='mycartedit-page'),
	path('checkout/', Checkout, name='checkout-page'),
	path('orderlist/', OrderlistPage, name='orderlist-page'),
	path('allorderlist/', AllOrderlistPage, name='allorderlist-page'),
	path('uploadslip/<str:orderid>/', UploadSlip, name='uploadslip-page'),
	path('updatestatus/<str:orderid>/<str:status>/',UpdatePaid, name='updatestatus'),
	path('updatetracking/<str:orderid>/',UpdateTracking, name='updatetracking'),
	path('myorder/<str:orderid>/', MyOrder, name='myorder-page'),
	path('confirm/<str:token>/', Confirm, name='confirm-email'),
	path('catagory/<int:code>/', ProductCatagory, name='catagory-page'),
	path('testmd/', TestMd, name='testmd-page'),
	path('product/<int:productid>/', ProductDetail, name='detail-page'),
	path('editproduct/<int:productid>/', EditProduct, name='editproduct-page'),
	path('api/product/', AllproductAPI, name='api-product'),
	# path('api/product/<int:pid>/', ProductDetailAPI, name='api-product-detail'),
	path('api/product/<int:pid>/', api_get_product, name='api-product-detail'),
	path('api/product/create', api_post_product, name='api-product-post'),
	path('api/product/update/<int:pid>', api_update_product, name='api-product-update'),
	path('api/product/delete/<int:pid>', api_delete_product, name='api-product-delete'),


]
