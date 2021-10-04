from django.urls import path
from backend import views 
from .views import MyPasswordChangeView, MyPasswordResetDoneView,ChartView


app_name='backend'

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('admin-login-view/', views.admin_login_view, name='admin_login_view'),
    path('logout-page/', views.logout_view, name='logout_view'),
    path('admin-logout-page/', views.admin_logout_view, name='admin_logout_view'),
    path('pass_form_page/', views.pass_form, name='pass_form'),
    path('admin_pass_form_page/', views.admin_pass_form, name='admin_pass_form'),
    path('success-message/', views.success_message, name='success_message'),
    path('change-password/', MyPasswordChangeView.as_view(), name='password-change-view'),
    path('admin-change-password/', MyPasswordChangeView.as_view(), name='password-change-view'),
    path('change-password/done/', MyPasswordResetDoneView.as_view(), name='password-change-done-view'),
    path('admin-change-password/done/', MyPasswordResetDoneView.as_view(), name='password-change-done-view'),
    path('chartview-page/', ChartView.as_view(), name='chartview'),
    path('confirm-page/', views.confirm_logout, name='confirm_logout'),
    path('admin-confirm-page/', views.admin_confirm_logout, name='admin_confirm_logout'),
    path('list-sellers/', views.list_sellers, name='list_sellers'),
    path('all-cars/', views.all_cars, name='all_cars'),
    path('view-cars/', views.view_cars, name='view_cars'),
    path('upload-car/', views.upload_car, name='upload_car'),
    path('uploads-car/', views.uploads_car, name='uploads_car'),
    path('edit-upload/<int:upload_id>/', views.edit_upload, name='edit_upload'),
    path('admin-edit-upload/<int:upload_id>/', views.admin_edit_upload, name='admin_edit_upload'),
    path('single-view/<int:pk>/', views.single_view, name='single_view'),
    path('admin-single-view/<int:pk>/', views.admin_single_view, name='admin_single_view'),
    path('delete-upload/<int:upload_id>/', views.delete_upload, name='delete_upload'),
    path('admin-delete-upload/<int:upload_id>/', views.admin_delete_upload, name='admin_delete_upload'),
    path('backoffice/', views.dashboard, name='dashboard'),
    path('approve-post/<int:pk>/', views.click_approve_post, name='click_approve_post'),
    path('disapprove-post/<int:pk>/', views.click_disapprove_post, name='click_disapprove_post'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view-profile/', views.view_profile, name='view_profile'),
    path('admin-view-profile/', views.admin_view_profile, name='admin_view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
]