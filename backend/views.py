from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from backend.tokens import account_activation_token
from .tokens import account_activation_token

from django.urls import reverse_lazy
from frontend.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView  
from django.views.generic import TemplateView
from backend.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib import messages


# Password Reset
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# signUp
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from backend.tokens import account_activation_token
from .tokens import account_activation_token
from django.template.loader import render_to_string
#end

# Create your views here.

def pass_form(request):
    if request.method == 'POST':
        pass_form = ChangePassword(data=request.POST, user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user) 
            messages.success(request, 'Password changed successfully.')
    else:
        pass_form = ChangePassword(user=request.user)
    return render(request, 'backend/pass-form.html', {'pass_key':pass_form})

def admin_pass_form(request):
    if request.method == 'POST':
        pass_form = ChangePassword(data=request.POST, user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user) 
            messages.success(request, 'Password changed successfully.')
    else:
        pass_form = ChangePassword(user=request.user)
    return render(request, 'chart/pass-form.html', {'pass_key':pass_form})

class ChartView(TemplateView):
    template_name = 'chart/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = Seller_Product.objects.all()

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'backend/password-change.html'
    success_url = reverse_lazy('backend:password-change-done-view')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'backend/password-reset-done.html '

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'chart/password-change.html'
    success_url = reverse_lazy('chart:password-change-done-view')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'chart/password-reset-done.html '

# def register(request):
#     if request.method == 'POST':
#         register = Register(request.POST)
#         if register.is_valid():
#             register.save()
#             messages.success(request, 'User have been registered')
#     else:
#         register = Register()
#     return render(request, 'frontend/register.html',{'reg':register})

def register(request):
    if request.method  == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('backend/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')

            # messages.success(request, 'User Registered')
    else:
        form = Register()
    return render(request, 'frontend/register.html', {'reg':form})

def activation_sent_view(request):
    return render(request, 'backend/activation_sent.html')

def activate (request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('backend:login_view')
    else:
        return render(request, 'backend/activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login[username]')
        password = request.POST.get('login[password]')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('backend:dashboard')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'frontend/login.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login[username]')
        password = request.POST.get('login[password]')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('backend:admin_dashboard')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'chart/login.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "backend/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'dchiemeka95@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="backend/password_reset.html", context={"password_reset_form":password_reset_form})



@login_required(login_url='/dashboard/')
def dashboard(request):
    full_name = "john doe"
    if request.user.is_authenticated:
        full_name = request.user.first_name
    
    return render(request, 'backend/index.html', {'fullname':full_name})

@login_required(login_url='/dashboard/')
def admin_dashboard(request):
    full_name = "john doe"
    if request.user.is_authenticated:
        full_name = request.user.first_name
    
    return render(request, 'chart/base.html', {'fullname':full_name})

@login_required(login_url='/dashboard/')
def list_sellers(request):
    show_seller = User.objects.all().order_by('last_name')
    return render(request, 'chart/view-sellers.html', {'seller':show_seller})


@login_required
def all_cars(request):
    seller_product = Seller_Product.objects.all()
    return render(request, 'chart/all-cars.html', {'cars':seller_product })

def view_cars(request):
    user = request.user
    seller_product = Seller_Product.objects.filter(car_owner = user)
    return render(request, 'backend/view-cars.html', {'user_upload':seller_product })

@login_required(login_url='/dashboard/')
def confirm_logout(request):
    return render(request, 'backend/confirm-logout.html')

@login_required(login_url='/dashboard/')
def logout_view(request):
    logout(request)
    return redirect('backend:login_view')

@login_required(login_url='/dashboard/')
def admin_confirm_logout(request):
    return render(request, 'chart/confirm-logout.html')

@login_required(login_url='/dashboard/')
def admin_logout_view(request):
    logout(request)
    return redirect('backend:admin_login_view')

@login_required(login_url='/dashboard/')
def view_profile(request):
    return render(request, 'backend/view-profile.html')

@login_required(login_url='/dashboard/')
def admin_view_profile(request):
    return render(request, 'chart/view-profile.html')


@login_required(login_url='/dashboard/')
def upload_car(request):
    if request.method == 'POST':
        upload_car = UploadForm(request.POST, request.FILES)
        if upload_car.is_valid():
            instance = upload_car.save(commit=False)
            instance.car_owner = request.user
            instance.save()
            messages.success(request, 'Car Uploaded')
    else:
        upload_car = UploadForm()
    return render(request, 'backend/upload-car.html', {'upload': upload_car})

@login_required(login_url='/dashboard/')
def uploads_car(request):
    if request.method == 'POST':
        upload_car = UploadForm(request.POST, request.FILES)
        if upload_car.is_valid():
            instance = upload_car.save(commit=False)
            instance.car_owner = request.user
            instance.save()
            messages.success(request, 'Car Uploaded')
    else:
        upload_car = UploadForm()
    return render(request, 'chart/upload-car.html', {'upload': upload_car})

    
@login_required(login_url='/dashboard/')
def edit_upload(request, upload_id):
    get_upload =get_object_or_404(Seller_Product, pk=upload_id)
    if request.method == 'POST':
        upload_car = UploadForm(request.POST, request.FILES, instance= get_upload)
        if upload_car.is_valid():
            instance = upload_car.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Upload Edited')
    else:
        upload_car = UploadForm(instance=get_upload)
    return render(request, 'backend/edit-upload.html', {'edit': upload_car})

def admin_edit_upload(request, upload_id):
    get_upload =get_object_or_404(Seller_Product, pk=upload_id)
    if request.method == 'POST':
        upload_car = UploadForm(request.POST, request.FILES, instance= get_upload)
        if upload_car.is_valid():
            instance = upload_car.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Upload Edited')
    else:
        upload_car = UploadForm(instance=get_upload)
    return render(request, 'chart/edit-upload.html', {'edit': upload_car})


def admin_single_view(request, pk):
    post = get_object_or_404(Seller_Product, pk=pk)
    return render(request, 'chart/view-car.html', {'pst':post})

def single_view(request, pk):
    post = get_object_or_404(Seller_Product, pk=pk)
    return render(request, 'chart/view-car.html', {'pst':post})

@login_required(login_url='/dashboard/')
def admin_delete_upload(request, upload_id):
    single_delete = get_object_or_404(Seller_Product, pk=upload_id)
    single_delete.delete()
    return redirect('backend:all_cars')

@login_required(login_url='/dashboard/')
def delete_upload(request, upload_id):
    single_delete = get_object_or_404(Seller_Product, pk=upload_id)
    single_delete.delete()
    return redirect('backend:all_cars')

def click_approve_post(request, pk):
    post = get_object_or_404(Seller_Product, pk=pk)
    post.approve_post()
    messages.success(request, 'Post approved successfully')
    return redirect('backend:all_cars')

def click_disapprove_post(request, pk):
    post = get_object_or_404(Seller_Product, pk=pk)
    post.disapprove_post()
    messages.error(request, 'Post disapproved ')
    return redirect('backend:all_cars')

def edit_profile(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, 'backend/edit-profile.html', {'edit_key':edit_form})

def success_message(request):
    return render(request, 'backend/success.html')

