
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [

	path(''		 		, include('baseapp.urls')),
	path('catalog/'		, include('catalogapp.urls')),
	path('accounts/'    , include('authapp.urls')),
	path('cart/'    	, include('cartapp.urls')),
	path('wishlist/'    , include('wishlistapp.urls')),
	path('orders/'    	, include('orderapp.urls')),
    path('admin/', admin.site.urls),
]
