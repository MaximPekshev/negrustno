from django.urls import path
from .views import show_category, show_category_list

urlpatterns = [

	path('', 						show_category_list, name='show_category_list'),
	path('<str:cpu_slug>/', 		show_category, name='show_category'),

]