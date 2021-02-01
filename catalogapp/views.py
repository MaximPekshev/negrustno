from django.shortcuts import render
from django.core.paginator import Paginator
from cartapp.views import get_cart

from .models import Good, Category, Manufacturer, Tag
from wishlistapp.views import get_wishlist

def show_catalog(request):

	goods_count=18

	goods = Good.objects.filter(is_active=True)
	
	page_number = request.GET.get('page', 1)

	paginator = Paginator(goods, goods_count)	

	page = paginator.get_page(page_number)

	last_url = '?page={}'.format(paginator.num_pages)

	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''

	categories = []
	cat_with_no_parents_and_no_childs = []

	for cat in Category.objects.all():
		if not cat.have_a_parent() and cat.have_a_childs():
			categories.append(cat)
		elif not cat.have_a_parent() and not cat.have_a_childs():
			cat_with_no_parents_and_no_childs.append(cat)



	context = {
		'page_object': page,
		'prev_url': prev_url,
		'next_url': next_url,
		'is_paginated': is_paginated,
		'last_page' : paginator.num_pages,
		'last_url' : last_url,
		'goods_count' : len(goods),
		'cart' : get_cart(request),
		'wishlist' : get_wishlist(request),
		'categories' : categories,
		'cat_with_no_parents_and_no_childs' : cat_with_no_parents_and_no_childs,
		'tags' : Tag.objects.all()[:6],
		'manufacturers' : Manufacturer.objects.all()[:6],

	}

	return  render(request, 'catalogapp/catalog.html', context)

def show_good(request, cpu_slug):
	
	good = Good.objects.get(cpu_slug=cpu_slug)

	context = {
		'good' : good,
		'related_goods' : Good.objects.all()[:5],
		'cart' : get_cart(request),
		'wishlist' : get_wishlist(request),
	}

	return render(request, 'catalogapp/good.html', context)
