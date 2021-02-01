from django.urls import path
from .views import show_cart, cart_add_item, cart_del_item

urlpatterns = [

	path('', 		show_cart, name='show_cart'),
	path('add/<str:cpu_slug>/', cart_add_item, name='cart_add_item'),
	path('del/<str:cpu_slug>/', cart_del_item, name='cart_del_item'),

]