from django.shortcuts import render,redirect, get_object_or_404
from frontend.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from backend.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from backend.tokens import *
from django.template.loader import render_to_string
from backend.forms import SignUpForm



# for sending mail import
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def index(request):
    fori = Seller_Product.objects.all().filter(category=1)[:4]
    locl = Seller_Product.objects.all().filter(category=2)[:4]
    query_form = FilterForm(request.GET)
    context = {
        'foreign':fori,
        'local':locl,
        'queryf':query_form
    }
    return render(request, 'frontend/index.html', context)

    

def compare(request):
    return render(request, 'frontend/compare.html')

def car_detail(request, car_id):
    detail = Seller_Product.objects.get(id=car_id)
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('message')
        print(name+' '+email+' '+message)
        subject = 'Client Information Form'
        context = {'name':name, 'email':email, 'message':message }
        html_message =render_to_string('frontend/mail-template1.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <dchiemeka95@gmail.com>'
        send =  mail.send_mail(subject, plain_message, from_email, ['dchiemeka95@gmail.com'], html_message=html_message, fail_silently=True)
        if send:
            messages.success(request, 'Email sent sucessfully')
        else:
            messages.error(request, 'Mail not sent')
    return render(request, 'frontend/car-detail.html',{'det':detail})

def foreign(request):
    gid = Seller_Product.objects.all().filter(category=1)
    paginated_filter = Paginator(gid, 6)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filter.get_page(page_number)
    context = {
        'person_page_obj': gid, 
    }
    context['person_page_obj'] = person_page_obj

    return render(request, 'frontend/grid.html', context)

def nigerian(request):
    lst = Seller_Product.objects.all().filter(category=2)
    paginated_filter = Paginator(lst, 6)
    page_number = request.GET.get('page')
    person_page_obj = paginated_filter.get_page(page_number)
    context = {
        'person_page_obj': lst, 
    }
    context['person_page_obj'] = person_page_obj
    return render(request, 'frontend/list.html', context)

def about(request):
    return render(request, 'frontend/about-us.html')

def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        comment = request.POST.get('comment')
        print(name+' '+email+' '+telephone+' '+comment)
        subject = 'Contact Us Form'
        context = {'name':name, 'email':email,'telephone':telephone, 'comment':comment }
        html_message =render_to_string('frontend/mail-template.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <dchiemeka95@gmail.com>'
        send =  mail.send_mail(subject, plain_message, from_email, ['dchiemeka95@gmail.com'], html_message=html_message, fail_silently=True)
        if send:
            messages.success(request, 'Email sent sucessfully')
        else:
            messages.error(request, 'Mail not sent')
    return render(request, 'frontend/contact-us.html')

def blog(request):
    return render(request, 'frontend/blog.html')

def filter_data(request):
    if request.method == 'GET':
        query_form = FilterForm(request.GET)
        if query_form.is_valid():
            car_name = query_form.cleaned_data.get('car_name')
            car_owner_location = query_form.cleaned_data.get('car_owner_location')
            category = query_form.cleaned_data.get('category')
            car_price = query_form.cleaned_data.get('car_price')
            query = Seller_Product.objects.filter(car_name=car_name, car_owner_location=car_owner_location, category__cat_name=category,car_price=car_price)
            print('Success')
            return render(request, 'frontend/filter.html', {'q': query})
        else:
            print('Not Found')
    return render(request, 'frontend/filter.html')



def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
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
            message = render_to_string('frontend/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('frontend:activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form': form})

def activation_sent_view(request):
    return render(request, 'frontend/activation_sent.html')

def activate(request, uidb64, token):
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
        return render(request, 'frontend/activation_invalid.html')



    


