from django.urls import path
from .views import (PostsList, PostDetail, PostCreate, PostEdit, PostDelete, PostSearch, upgrade_me, IndexView,
                    ProfileUpdate, CategoryListView, subscribe)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('post/', cache_page(15)(PostsList.as_view()), name='post_list'),
    path('post/<int:pk>', cache_page(30)(PostDetail.as_view()), name='post_detail'),
    path('post/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('profile/', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('profile/<int:pk>/update/', ProfileUpdate.as_view(), name='profile_update'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
