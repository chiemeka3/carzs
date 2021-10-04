from django import forms
from backend.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.core import validators
from frontend.models import Seller_Product,Category
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import(PasswordResetForm, SetPasswordForm, PasswordChangeForm, UserChangeForm, UserCreationForm)


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username*', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    first_name = forms.CharField(max_length=100, help_text='First Name', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Firstname'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Lastname'}))
    email = forms.EmailField(max_length=150, help_text='Email',
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    password1 = forms.CharField(label='Enter Password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2= forms.CharField(label='Confirm Password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exist')
        return email_field

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2', )


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    new_password1 = forms.CharField(label='New password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    new_password2= forms.CharField(label='Confirm Password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
    validators=[validators.MaxLengthValidator(0)])

class Register(UserCreationForm):
    username = forms.CharField(label='Username*', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    email = forms.EmailField(label='Email*',
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Firstname'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Lastname'}))
    password1 = forms.CharField(label='Enter Password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2= forms.CharField(label='Confirm Password*', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
    validators=[validators.MaxLengthValidator(0)])

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exist')
        return email_field

    class meta():
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            return user

class UploadForm(forms.ModelForm):
    car_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Name'})
    )
    car_model = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Model'})
    )
    car_year = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Year'})
    )
    car_speed = forms.CharField(
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Car Speed', })
    )
    car_price = forms.CharField(
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price', })
    )
    car_owner_location = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location'})
    )
    # car_type = forms.CharField(
    #     widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Type'})
    # )
    car_description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}))
    catch_bot = forms.CharField(required=False, 
                widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta():
        exclude = ['date_posted', 'car_owner', 'car_type', ]
        model = Seller_Product

class EditUploadForm(forms.ModelForm):
    car_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Name'})
    )
    car_model = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Model'})
    )
    car_year = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Year'})
    )
    car_speed = forms.CharField(
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Car Speed', })
    )
    car_price = forms.CharField(
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price', })
    )
    car_owner_location = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location'})
    )
    # car_type = forms.CharField(
    #     widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Car Type'})
    # )
    car_description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}))
    catch_bot = forms.CharField(required=False, 
                widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta():
        exclude = ['date_posted', 'car_owner', 'car_type', ]
        model = Seller_Product

class CategoryForm(forms.ModelForm):
    cat_name = forms.CharField(label="Category Name*", 
               widget=forms.TextInput(
               attrs={'class':'form-control', 'placeholder':'Enter Category'}))
    cat_desc = forms.CharField(label='Description', required=False,
              widget=forms.Textarea(
             attrs={'class':'form-control'}
              ))
    catch_bot = forms.CharField(required=False, 
                widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
    # clean_<fieldname> is use to validate for just one field
    def clean_cat_name(self):
        cat = self.cleaned_data.get('cat_name').lower()
        if Category.objects.filter(cat_name=cat).exists():
            raise forms.ValidationError(f'{cat} already exist')
        return cat

    class Meta():
        fields = '__all__'
        model = Category

class FilterForm(forms.ModelForm):
    ONE = "200000"
    TWO = "900000"
    THREE = "1000000"
    FOUR = "1300000"
    FIVE = "2300000"
    SIX = "45000000"
    SEVEN = "11800000"
    EIGHT = "260000000"
    NINE = "15000000"
    TEN = "4000000"
    ONE1 = "23500000"
    TW02 = "26000000"
    THREE3 = "3200000"
    FOUR4 = "24500000"
    FIVE5 = "70000000"
    CHOOSE = ""

    PRICE= [
        (ONE, '200000'),
        (TWO, '900000'),
        (THREE, '1000000'),
        (FOUR, '1300000'),
        (FIVE, '2300000'),
        (SIX, '45000000'),
        (SEVEN, '11800000'),
        (EIGHT, '260000000'),
        (NINE, '15000000'),
        (TEN, '4000000'),
        (ONE1, '23500000'),
        (TW02, '26000000'),
        (THREE3, '3200000'),
        (FOUR4, '24500000'),
        (FIVE5, '70000000'),
        (CHOOSE, 'Price')
    ]

    ONE = "Foreign"
    TWO = "Local"
    CHOOSE = "Car Type"

    CATEGORY= [
        (ONE, 'Foreign'),
        (TWO, 'Local'),
        (CHOOSE, 'Car Type')
    ]

    ONE = "Ikeja"
    TWO = "Oshodi"
    THREE = "Lekki"
    FOUR = "Festac"
    FIVE = "Apapa"
    SIX = "Surulere"
    CHOOSE = ""

    LOCATION= [
        (ONE, 'Ikeja'),
        (TWO, 'Oshodi'),
        (THREE, 'Lekki'),
        (FOUR, 'Festac'),
        (FIVE, 'Apapa'),
        (SIX, 'Surulere'),
        (CHOOSE, 'Car Location')
    ]

    ONE = "Range Rover"
    TWO = "Land Rover Range Rover"
    THREE = "Mercedes Benz"
    FOUR = "Toyota"
    FIVE = "Lexus"
    SIX = "Rolls Royce"
    CHOOSE = ""

    CAR_NAME= [
        (ONE, 'Range Rover'),
        (TWO, 'Land Rover Range Rover'),
        (THREE, 'Mercedes Benz'),
        (FOUR, 'Toyota'),
        (FIVE, 'Lexus'),
        (SIX, 'Rolls Royce'),
        (CHOOSE, 'Car Name')
    ]

    car_name = forms.CharField(required=False, label='Name',widget=forms.Select(choices=CAR_NAME,
        attrs={'class': 'form-control', 'placeholder' : 'Car Name'}))
    car_owner_location = forms.CharField(required=False, label='Location',widget=forms.Select(choices=LOCATION,
        attrs={'class': 'form-control', 'placeholder' : 'Location'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}))
    car_price = forms.CharField(required=False, label='Price',widget=forms.Select(choices=PRICE,
        attrs={'class': 'form-control', 'placeholder' : 'Price'}))
    class Meta():
        fields = ['car_name','car_owner_location','category','car_name']
        model = Seller_Product

class EditUserForm(forms.ModelForm):
        username = forms.CharField(label='Username', widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder': 'Enter Username' }))

        email = forms.EmailField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))

        first_name = forms.CharField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}))

        last_name = forms.CharField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}))

        class Meta():
            model = User
            fields = ['username', 'email', 'first_name', 'last_name']

            widgets = {
                'username': forms.TextInput(attrs={'class':'form-control'}),

                'email':forms.TextInput(attrs={'class':'form-control'}),

                'first_name': forms.TextInput(attrs={'class':'form-control'}),

                'last_name': forms.TextInput(attrs={'class':'form-control'}),
            }

        def save(self, commit=True):
            user = super().save(commit=False)
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']

    
            if commit:
                user.save()
                return user
    
    