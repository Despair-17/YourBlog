from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:category_slug>/', views.PostsByCategoryView.as_view(), name='category'),
    path('post/<slug:post_slug>', views.PostView.as_view(), name='post'),
]
