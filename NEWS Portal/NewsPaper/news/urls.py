from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostEdit, PostDelete, PostSearch

urlpatterns = [
    path('post/', PostsList.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
