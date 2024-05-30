from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView, PasswordResetCompleteView,
                                       PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView)
from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/done/', register_user_done, name='register_done'),
    path('accounts/profile/', ProfileUserView.as_view(), name='profile'),
    path('accounts/password_change/', PasswordChangeUserView.as_view(), name='password_change'),
    path(
        'accounts/password-change/done/',
        PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done',
    ),
    path(
        'accounts/password-reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset',
    ),
    path(
        'accounts/password-reset/done',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'accounts/password-reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),
    path(
        'accounts/password-reset/confirm',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete',
    )
]
