from django.shortcuts import render
from cartapp.views import get_cart
from wishlistapp.views import get_wishlist
from catalogapp.models import Good, Category, Manufacturer, Tag
from django.core.paginator import Paginator

def show_category(request, cpu_slug):

	category = Category.objects.filter(cpu_slug=cpu_slug).first()

	context = {

		'category' : category,
		'cart' : get_cart(request),
		'wishlist' : get_wishlist(request),

	}

	if not category.have_a_childs():

		goods_count=18

		goods = Good.objects.filter(is_active=True, category=category)
		
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


		context.update({
			'page_object': page,
			'prev_url': prev_url,
			'next_url': next_url,
			'is_paginated': is_paginated,
			'last_page' : paginator.num_pages,
			'last_url' : last_url,
			'goods_count' : len(goods),
			'categories' : categories,
			'cat_with_no_parents_and_no_childs' : cat_with_no_parents_and_no_childs,
			'tags' : Tag.objects.all()[:6],
			'manufacturers' : Manufacturer.objects.all()[:6],
		})
	
	return render(request, 'categoryapp/category.html', context)


def show_category_list(request):

	categories = []
	cat_with_no_parents_and_no_childs = []

	for cat in Category.objects.all():
		if not cat.have_a_parent() and cat.have_a_childs():
			categories.append(cat)
		elif not cat.have_a_parent() and not cat.have_a_childs():
			cat_with_no_parents_and_no_childs.append(cat)
	
	context = {

		'categories' : categories,
		'cat_with_no_parents_and_no_childs' : cat_with_no_parents_and_no_childs,
		'cart' : get_cart(request),
		'wishlist' : get_wishlist(request),

	}

	return render(request, 'categoryapp/category_list.html', context)
