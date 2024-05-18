from django.urls import path
from . import views

urlpatterns = [
    path('all-categories/', views.AllCategoriesView.as_view(), name='all_categories'),
    path('category/<slug:category_slug>/', views.PostsByCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostsByTagsView.as_view(), name='tag'),
    path('search/', views.PostsSearchView.as_view(), name='search'),
    path('extended-search/', views.PostsExtendedSearchView.as_view(), name='extended_search'),
    path('user-posts/', views.MyPostsCreateView.as_view(), name='my_posts'),
    path('post/<slug:post_slug>/', views.PostDetailView.as_view(), name='post'),
    path('post/update/<slug:post_slug>', views.MyPostsUpdateView.as_view(), name='update_post'),
    path('post/delete/<slug:post_slug>', views.MyPostsDeleteView.as_view(), name='delete_post'),
]
