from django.urls import path
from . import views

urlpatterns = [
    path('post/<slug:post_slug>/', views.PostView.as_view(), name='post'),
    path('all-categories/', views.AllCategoriesView.as_view(), name='all_categories'),
    path('category/<slug:category_slug>/', views.PostsByCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostsByTagsView.as_view(), name='tag'),
    path('search/', views.PostsSearchView.as_view(), name='search'),
]
