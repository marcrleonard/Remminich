import datetime
import os

from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import PasswordResetForm, SetPasswordForm
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Album
from immich.ImmichClient import ImmichClient
from immich.models import BulkUpdateAssetsModel

needs_email_verify = True

def _get_message(request, user):
	r = render_to_string('template_activate_account.html', {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http'
	})
	print(r)
	return r


def activateEmail(request, user, to_email):
	mail_subject = 'Activate your user account.'
	message = _get_message(request, user)
	email = EmailMessage(mail_subject, message, to=[to_email])
	if email.send():
		messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
			received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
	else:
		messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()

		messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
		return redirect('login')
	else:
		messages.error(request, 'Activation link has expired. Please resend.')

	return redirect('/')


# Create your views here.
def register(request):
	# Logged in user can't register a new account
	if request.user.is_authenticated:
		return redirect("/")

	errors = ""
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			if needs_email_verify:
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				# activateEmail(request, user, form.cleaned_data.get('email'))

				send_mail(
					'Activate your Art Stream account.',
					_get_message(request, user),
					'sales@artstreamvideos.com',
					[form.cleaned_data.get('email')],
					fail_silently=False,
				)

				messages.success(request,
								 "Thanks for signing up! Please click the link in your email to finish activating your account!")

			else:
				user = form.save()
				login(request, user)

			return redirect('/')
		else:
			print(form.errors)
	# for error in list(form.errors.values()):
	# 	messages.error(request, error)
	# errors+=str(error)

	else:
		form = UserRegistrationForm()

	return render(
		request=request,
		template_name="register.html",
		context={
			"form": form,
			"errors_html": errors
		}
	)


def logout_view(request):
	messages.info(request, "User logged out.")
	logout(request)
	return redirect("/accounts/login")


def logged_in_home(request):
	return render(request, "templates/dashboard.html", {})


def register_submit(request):
	if request.method == 'POST':

		form = UserRegistrationForm(request.POST)

		if form.is_valid():
			if needs_email_verify:

				from django import forms
				f = forms.EmailField()

				try:
					f.clean(form.instance.email)
				except forms.ValidationError:
					form.add_error('email', 'Invalid email address.')
					return render(request, 'register.html',
								  {'errors': form.errors}
								  )

				user = form.save(commit=False)
				user.save()

				send_mail(
					'Activate your Art Stream account.',
					_get_message(request, user),
					'sales@artstreamvideos.com',
					[form.cleaned_data.get('email')],
					fail_silently=False,
				)

				messages.success(request,
								 "Thanks for signing up! Please click the link in your email to finish activating your account!")

			else:
				user = form.save()
				login(request, user)

			return redirect('/')
		else:
			return render(request, 'register.html', {'form': form, 'errors': form.errors})

	return JsonResponse({"ok": False})


def profile(request):
	expiry_date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
	sub_level = request.user.get_subscription_level_display()

	if request.POST:
		form = UserUpdateForm(data=request.POST, instance=request.user)
		if form.is_valid():
			form.save()

		return render(request, 'templates/profile.html', {
			'form': form,
			'membership_level': sub_level,
			'expiry_date': expiry_date
		})

	else:
		original_form = UserUpdateForm(instance=request.user)

		return render(request, 'templates/profile.html', {
			'form': original_form,
			'membership_level': sub_level,
			'expiry_date': expiry_date
		})


def index(request):
	all_albums = ImmichClient.list_albums()
	first = all_albums[0]
	a = ImmichClient.get_album(first['id'])

	summary_data = _get_summary_data(a)

	thumb = f"/asset/{a['albumThumbnailAssetId']}/thumb"
	return render(request, "index.html",
				  {
					  "albums": [],
					  "album_name": a['albumName'],
					  "album_uuid": a['id'],
					  "album_image_link": thumb,
					  "summary_data":summary_data
				  }
	)

def search_places(request):
	p = request.GET.get('name', '')
	r = ImmichClient.get_place(p)
	return JsonResponse(r, safe=False)

def _get_summary_data(assetResp: dict):
	locations = []
	dates = []
	for asset in assetResp['assets']:
		metadata = asset['exifInfo']
		long = metadata['longitude']
		lat = metadata['longitude']
		city = metadata['city']
		state = metadata['state']
		country = metadata['country']
		if any([long, lat, city, state, country]):
			if any([city, state, country]):
				location_formatted = ""
				if city:
					location_formatted += city
				if state:
					if location_formatted != "":
						location_formatted += f", {state}"
					else:
						location_formatted += state
				if all([
					location_formatted == "",
					country
				]):
					# only add the country if we got nothin else
					location_formatted += f" ({country})"

				locations.append(location_formatted)

			elif any([long, lat]):
				locations.append(f"({long}, {lat})")

		date = metadata['dateTimeOriginal']
		if date:
			dates.append(date)

	dates = [datetime.datetime.fromisoformat(ts[:-6]) for ts in dates]  # Remove timezone offset

	# Sort dates
	dates.sort()

	# Format and display
	formatted_dates = [date.strftime("%B %-d, %Y") for date in dates]

	start_end_dates = ""
	if len(formatted_dates) > 1:
		start_end_dates = f"{formatted_dates[0]} to {formatted_dates[-1]}"
	elif len(formatted_dates) == 1:
		start_end_dates = formatted_dates[0]

	location_str = "No locations."

	locations = list(set(locations))
	if locations:
		location_str = locations[0]
		if len(locations) > 1:
			location_str += f" and {len(locations) - 1} more"

	return {
		'locations': location_str,
		'dates': start_end_dates
	}
def get_album(request, album_uuid):
	# album = get_object_or_404(Album, id=album_uuid)
	a = ImmichClient.get_album(album_uuid)
	thumb = f"/asset/{a['albumThumbnailAssetId']}/thumb"

	summary_data = _get_summary_data(a)

	for asset in a['assets']:
		# enrich the date
		aa = asset['exifInfo']['dateTimeOriginal']
		asd = datetime.datetime.fromisoformat(aa[:-6])
		human  = asd.strftime("%B %-d, %Y")
		asset['dateHuman'] = human

	return render(request, "edit-metadata.html", {
		"immich": a,
		"album_thumbnail": thumb,
		"summary_data": summary_data,

	})


def get_asset_thumbnail(request, asset_uuid):
	r = ImmichClient.get_thumbnail(asset_uuid)
	return HttpResponse(r.content, content_type='image/jpeg')


@csrf_exempt
def update_album(request):
	if request.method == 'POST':

		ImmichClient.update_assets(BulkUpdateAssetsModel(ids=[], ))
		return JsonResponse({"id": str(album.id), "title": album.title})
