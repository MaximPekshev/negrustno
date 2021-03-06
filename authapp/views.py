from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from cartapp.views import get_cart
import django.core.exceptions
from authapp.models import Buyer
from .forms import BuyerSaveForm
from allauth.account.views import PasswordChangeView, PasswordResetView
from allauth.account.views import LoginView, SignupView, PasswordResetDoneView
from allauth.account.views import PasswordResetFromKeyView
from allauth.account.utils import passthrough_next_redirect_url, get_request_param
from django.contrib.sites.shortcuts import get_current_site


def profile_change(request, buyer_id):

	if request.method == 'POST':

		buyer_form = BuyerSaveForm(request.POST)

		if buyer_form.is_valid():

			first_name 	= buyer_form.cleaned_data['input_first_name']
			last_name	= buyer_form.cleaned_data['input_second_name']
			phone 		= buyer_form.cleaned_data['input_phone']

			try:
				buyer = Buyer.objects.get(id=buyer_id)

				buyer.first_name 	= first_name
				buyer.last_name 	= last_name
				buyer.phone 		= phone

				buyer.save()
				
			except Buyer.DoesNotExist:
				pass


		current_path = request.META['HTTP_REFERER']
		return redirect(current_path)

def profile_add(request):

	if request.method == 'POST':

		buyer_form = BuyerSaveForm(request.POST)

		if buyer_form.is_valid():

			first_name 	= buyer_form.cleaned_data['input_first_name']
			last_name	= buyer_form.cleaned_data['input_second_name']
			phone 		= buyer_form.cleaned_data['input_phone']

			buyer = Buyer(
				user = request.user,
				first_name = first_name,
				last_name = last_name, 
				)

			buyer.save()

		current_path = request.META['HTTP_REFERER']
		return redirect(current_path)

def show_profile(request):
	

	context = {

		'cart' : get_cart(request),

	}


	try:

		buyer = Buyer.objects.get(user=request.user)

		context.update({
			'buyer': buyer,
			})

	except Buyer.DoesNotExist:

		 pass


	if request.user.is_authenticated:

		return render(request, 'authapp/profile.html', context)

	else:

		return render(request, 'authapp/non_auth_profile.html', context)


class CustomSignupView(SignupView):


	def get_context_data(self, **kwargs):

		ret = super(SignupView, self).get_context_data(**kwargs)

		form = ret['form']
		email = self.request.session.get('account_verified_email')

		if email:
			email_keys = ['email']
			if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
				email_keys.append('email2')
			for email_key in email_keys:
				form.fields[email_key].initial = email

		login_url = passthrough_next_redirect_url(self.request,reverse("account_login"),self.redirect_field_name)
		redirect_field_name = self.redirect_field_name
		redirect_field_value = get_request_param(self.request,redirect_field_name)

		ret.update({'login_url': login_url,
	                'redirect_field_name': redirect_field_name,
	                'redirect_field_value': redirect_field_value,
	                'cart': get_cart(self.request),
	                })

		return ret

class CustomLoginView(LoginView):

	def get_context_data(self, **kwargs):

		ret = super(LoginView, self).get_context_data(**kwargs)
		signup_url = passthrough_next_redirect_url(self.request,reverse('account_signup'),self.redirect_field_name)

		redirect_field_value = get_request_param(self.request,self.redirect_field_name)
		site = get_current_site(self.request)

		ret.update({'signup_url': signup_url,
                    'site': site,
                    'redirect_field_name': self.redirect_field_name,
                    'redirect_field_value': redirect_field_value,
                    'cart': get_cart(self.request),
        			})

		return ret

class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):

	
	def get_context_data(self, **kwargs):

		ret = super(PasswordResetFromKeyView, self).get_context_data(**kwargs)

		ret.update({

			'cart': get_cart(self.request), 

			})

		ret['action_url'] = reverse('account_reset_password_from_key',kwargs={'uidb36': self.kwargs['uidb36'],'key': self.kwargs['key']})

		return ret



class CustomPasswordResetDoneView(PasswordResetDoneView):
	
	def get_context_data(self, **kwargs):

		ret = super(PasswordResetDoneView, self).get_context_data(**kwargs)

		ret.update({

			'cart': get_cart(self.request),

			})

		return ret
		
class  CustomPasswordResetView(PasswordResetView):

	def get_context_data(self, **kwargs):


		ret = super(PasswordResetView, self).get_context_data(**kwargs)


		login_url = passthrough_next_redirect_url(self.request,reverse("account_login"),self.redirect_field_name)


		ret['password_reset_form'] = ret.get('form')

		ret.update({

			'login_url': login_url,
			'cart': get_cart(self.request),

			})

		return ret

class CustomPasswordChangeView(PasswordChangeView):

    success_url = reverse_lazy('account_password_change_succes')

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        ret['password_change_form'] = ret.get('form')

        ret.update({
        	'cart': get_cart(self.request),
        	})

        return ret

def account_password_change_succes(request):

	context = {

		'cart': get_cart(request),

	}

	return render(request, 'authapp/change_password_succes.html', context)        