from django.shortcuts import render, redirect
from .models import Wishlist, Wishlist_Item
from catalogapp.models import Good
from cartapp.models import Cart, Cart_Item
from cartapp.views import get_cart

def show_wishlist(request):
	return render(request, 'wishlistapp/wishlist.html')


def get_wishlist(request):

	if request.user.is_authenticated:
		wishlist 	= Wishlist.objects.filter(user = request.user).last()
	else:
		wishlist_id = request.session.get("wishlist_id")	
		wishlist 	= Wishlist.objects.filter(id = wishlist_id).last()

	return wishlist


def create_wishlist(request):

	wishlist_id 	= request.session.get("wishlist_id")
	wishlist		= Wishlist()

	if request.user.is_authenticated:
		wishlist.user = request.user
	else:
		wishlist.user = None

	wishlist.save()
	request.session['wishlist_id'] = wishlist.id

	return wishlist


def show_wishlist(request):


	context = {

		'wishlist': get_wishlist(request),
		'cart': get_cart(request),

	}


	return render(request, 'wishlistapp/wishlist.html', context)



def wishlist_add_item(request, cpu_slug):

	wishlist = get_wishlist(request)

	if wishlist == None:

		wishlist = create_wishlist(request)

	good 	= Good.objects.get(cpu_slug = cpu_slug)
	item 	= Wishlist_Item.objects.filter(wishlist=wishlist, good=good).first()
	if item:
		item.delete()
	else:			
		item 	= Wishlist_Item(wishlist = wishlist, good = good, price = good.price)
		item.save()

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)
