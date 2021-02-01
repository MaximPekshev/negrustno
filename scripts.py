import json

from catalogapp.models import Category, Good
from decimal import Decimal

def upload_category():
	with open('group1.json', 'r', encoding='utf-8') as f:
		data = json.load(f)
		for item in data['data']:
			try:
				cat = Category.objects.get(uid=str(item['id']))
			except:
				cat = Category(
					title=item['name'],
					uid=item['id'],
					)
				cat.save()

			try:
				parent = Category.objects.get(uid=str(item['group']))
				cat.parent_category = parent
				cat.save()
			except:
				pass

def upload_goods():
	with open('goods.json', 'r', encoding='utf-8') as f:
		data = json.load(f)
		for item in data['data']:

			try:
				price = Decimal(item['price'])
			except:
				price= 1
			
			good = Good(
				title=item['name'],
				good_uid=item['id'],
				art=item['art'],
				fullname=item['fullname'],
				description=item['description'],
				price= price,
				old_price=None,
				discount_per=None,
				quantity=1,
				weight=1,
				is_active=True
				)
			good.save()

			try:
				cat = Category.objects.get(uid=str(item['group']))
				good.category = cat
				good.save()
			except:
				pass


def update_brands():

	with open('goods.json', 'r', encoding='utf-8') as f:
		data = json.load(f)
		for item in data['data']:

			try:
				good = Good.objects.filter(good_uid=item['id']).first()
				try:
					properties = item.get('propertyes')
					for i in propertyes:
						if i.key == 'Бренд':
							print(i.value)
				except:
					pass
			except:
				pass
