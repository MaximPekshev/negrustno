from django.urls import path
from .views import show_catalog, show_good
from django.urls import include

urlpatterns = [

	path('', 						show_catalog, name='show_catalog'),
	path('category/', 				include('categoryapp.urls')),
	path('<str:cpu_slug>/', 		show_good, name='show_good'),

]