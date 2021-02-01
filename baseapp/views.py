from django.shortcuts import render
from cartapp.views import get_cart

def show_index(request):

	context = {
		'cart' : get_cart(request),
	}

	return  render(request, 'baseapp/index.html', context)
