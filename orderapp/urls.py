from django.urls import path
from .views import show_orders

urlpatterns = [

	path('', 		show_orders, name='show_orders'),

]