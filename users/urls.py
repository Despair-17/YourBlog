from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

app_name = 'users'

urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register_done/', RegisterUserDoneView.as_view(), name='register_done'),
]
