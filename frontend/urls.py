from django.urls import path
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('', views.compare, name='compare'),
    path('foreign-page/', views.foreign, name='foreign'),
    path('nigerian-page/', views.nigerian, name='nigerian'),
    path('filter-data/', views.filter_data, name='filter_data'),
    path('details/<int:car_id>/', views.car_detail, name='car_detail'),
    path('about-page/', views.about, name='about'),
    path('contact-page/', views.contact, name='contact'),
    path('signup/', views.signup_view, name="signup"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]