from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.

class Category(models.Model):
    cat_name = models.CharField(max_length=100, verbose_name='Category Name')
    cat_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.cat_name

    class Meta():
        verbose_name_plural='Category'

class Car(models.Model):
    car_type = models.CharField(max_length=60)

    def __str__(self):
        return self.car_type

class Plan(models.Model):
    plan_name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.plan_name

class User_plan(models.Model):
    user_plan_name =  models.ForeignKey(Plan,on_delete=models.CASCADE,blank=True,null=True)
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True) 

    def __str__(self):
        return f'{self.user_name} is on a {self.user_plan_name} Plan'      

class Seller_Product(models.Model):
    FEATURE = 'Feature'
    NO_FEATURE = 'No Feature'
    CHOOSE = ''
    APPEAR_HOME_FIELD=[
        (FEATURE,'Appear on home'),
        (NO_FEATURE,"Don't show on home"),
        (CHOOSE, 'Please Choose')
    ]

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
    CHOOSE = ""

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

    car_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_id')
    car_name = models.CharField(max_length=80, choices=CAR_NAME, default=CHOOSE)
    car_model = models.CharField(max_length=80)
    car_year = models.CharField(max_length=80)
    # car_type = models.ForeignKey(Car,on_delete=models.CASCADE)
    car_speed = models.DecimalField(max_digits=7,decimal_places=2)
    car_owner_location = models.CharField(max_length=80,choices=LOCATION, default=CHOOSE)
    car_image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    car_price = models.DecimalField(max_digits=12,decimal_places=2, choices=PRICE, default=CHOOSE)
    car_description = models.TextField(default='',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.car_model

    @property
    def img_url(self):
        if self.car_image:
            return self.car_image.url

    class Meta():
        verbose_name_plural='Seller_Product'

    def approve_post(self):
        self.approve = True
        self.save()

    def disapprove_post(self):
        self.approve = False
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


