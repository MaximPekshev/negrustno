from django.db import models

from django.conf import settings

from catalogapp.models import Good

class Wishlist(models.Model):

	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

	def get_wishlist_items(self):

		return Wishlist_Item.objects.filter(wishlist=self)

	def get_goods_in_wishlist(self):

		goods_list = []

		for item in Wishlist_Item.objects.filter(wishlist=self):

			goods_list.append(item.good)
		
		return goods_list

	def get_wishlist_count(self):
		
		return Wishlist_Item.objects.filter(wishlist=self).count()

	def __str__(self):
		return str(self.id)

class Wishlist_Item(models.Model):

	wishlist 	= models.ForeignKey(Wishlist, on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0, default=0)


	def __str__(self):
		return str(self.id)

