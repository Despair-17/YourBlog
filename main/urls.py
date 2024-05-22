from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('faq/', views.FAQPageView.as_view(), name='faq'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('captcha/', include('captcha.urls')),

    path('api/v1/health/', views.health, name='health'),
]
