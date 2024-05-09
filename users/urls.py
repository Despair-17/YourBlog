from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

from .views import *

app_name = 'users'

urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register_done/', register_user_done, name='register_done'),
    path('accounts/profile/', ProfileUserView.as_view(), name='profile'),
    path('accounts/password_change/', PasswordChangeUserView.as_view(), name='password_change'),
    path('accounts/password_change_done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done')
]
