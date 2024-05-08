from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

app_name = 'users'

urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register_done/', register_user_done, name='register_done'),
    path('accounts/profile/', ProfileUserView.as_view(), name='profile')
]
