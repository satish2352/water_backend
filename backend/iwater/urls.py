from django.urls import path, include
# from . import views  # TODO for views.py
import iwater.views as views

urlpatterns = [
    # login/signup/logout
    path('', views.user_login, name='login'),
    path('otp_login/<uidb64>/', views.otp_login, name='otp_login'),
    path('signup/', views.user_registration, name='create_user'),
    path('update_signup/<int:pk>', views.update_user_registration, name='edit_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('change_password/<uidb64>/<token>/', views.change_password, name='change_password'),
    path('change_pass/<uidb64>/<token>/', views.change_password, name='change_pass'),
    path('get_user_to_verify/<uidb64>/<token>/', views.get_user_to_verify, name='get_user_to_verify'),
    path('user_invite/<uidb64>/<token>/', views.user_invite, name='user_invite'),
    
    # path('user_otp/', views.user_otp, name='user_otp'),
    path('verify_user_otp/<uidb64>/<token>/', views.verify_user_otp, name='verify_user_otp'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.user_logout, name='logout'),
    
    path('block-user/<str:email>/', views.block_user),  # added by Sourabh while adding block unblock functionality
    path('unblock-user/<str:email>/', views.unblock_user), # added by Sourabh while adding block unblock functionality
    path('blocked/', views.blocked_view, name='blocked'), # added by Sourabh while adding block unblock functionality

    # subscription
    path('list_sub/', views.list_sub, name="subs"),
    path('site_in_sub/<int:id>', views.sites_under_subscription, name="site_in_sub"),
    path('unassigned_sites/', views.list_free_or_unassigned_sites, name="unassigned_sites"),
    path('add_sub/', views.add_sub, name='addsub'),
    path('razorpay_callback/', views.razorpay_callback, name='razorpay_callback'),
    path('renew_sub/<int:sub_id>', views.renew_sub, name='renew_sub'),
    #--------------------Under code added by Ajim for show data on 28/06/2023-------------------------------------------
   # path('showdata/', views.showdata, name='showdata'),
    #--------------------Under code added by Ajim for show data on 28/06/2023-------------------------------------------

    # list users
    path('users/', views.list_users),
    path('users/<int:pk>', views.user),

    # modify users
    path('add_user/', views.add_user),
    path('resend_invite/<int:pk>', views.resend_invite, name='resend_invite'),
    path('edit_user/<int:pk>', views.edit_user),
    path('available_users/<int:pk>', views.get_available_users),
    path('delete_user/<int:pk>', views.save_and_delete_user),
    path('delete_account/', views.delete_company_account),

    # list sites
    path('sites/', views.list_sites),
    path('sites/<int:pk>', views.site),

    # modify sites
    path('send_otp/', views.send_otp),
    path('verify_otp/', views.verify_otp),
    path('verify_token/', views.verify_token),
    path('add_site/', views.add_site),
    path('get_device/<int:pk>', views.get_device),
    path('re_auth_device/', views.re_auth_device),
    path('edit_site/<int:pk>', views.edit_site),
    path('sites_to_allocate/<int:pk>', views.get_free_or_expired_trial_sites),
    path('delete_site/<int:pk>', views.delete_site),

    # filter sites TODO
    # path('sites/name/<str:city_or_state>', views.filter_sites_by_name),
    path('sites/filter/<str:name>', views.filter_sites_by_location),

    # list archived sites
    path('archive_sites/', views.list_archive_sites),
    path('archive_sites/<int:pk>', views.list_archive_site),

    path('logs/<int:n>', views.get_log),

    # path('sites/date/<str:created_date>', views.filter_sites_by_date),
]
