from django.shortcuts import render

def show_orders(request):
	return render(request, 'orderapp/my_orders.html')
