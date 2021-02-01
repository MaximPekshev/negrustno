from django.shortcuts import render, redirect
from .models import Cart, Cart_Item
from catalogapp.models import Good
from .models import cart_calculate_summ
from django.db.models import Sum
from decimal import Decimal

def test(request):

	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:
		cart_id 	= request.session.get("cart_id")	
		cart 		= Cart.objects.filter(id = cart_id).last()

	return cart

def get_cart(request):

	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:
		cart_id 	= request.session.get("cart_id")	
		cart 		= Cart.objects.filter(id = cart_id).last()

	return cart

def create_cart(request):

	cart_id 		= request.session.get("cart_id")
	cart 			= Cart()

	if request.user.is_authenticated:
		cart.user = request.user
	else:
		cart.user = None

	cart.save()
	request.session['cart_id'] = cart.id

	return cart


def show_cart(request):

	cart  = get_cart(request)

	context = { 
		'cart': cart,
		}
	
	return render(request, 'cartapp/cart.html', context)


def cart_add_item(request, cpu_slug):

	if request.method == 'POST':

		quantity 		= Decimal(request.POST.get('quantity'))

		cart 			= get_cart(request)

		if cart == None:

			cart = create_cart(request)

		good 				= Good.objects.get(cpu_slug = cpu_slug)
		item 				= Cart_Item.objects.filter(cart=cart, good=good).first()
		if item is None:	
			item 			= Cart_Item(cart = cart, good = good, quantity = quantity, price = good.price)
		else:			
			item.quantity	+= quantity

		item.save()

		current_path = request.META['HTTP_REFERER']
		return redirect(current_path)

def cart_del_item(request, cpu_slug):

	cart 	= get_cart(request)

	if cart != None:

		good 	= Good.objects.get(cpu_slug = cpu_slug)
		item 	= Cart_Item.objects.filter(cart = cart, good = good).first().delete()
		cart_calculate_summ(cart)


	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)

