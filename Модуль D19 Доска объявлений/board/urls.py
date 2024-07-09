from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import PostList, PostDetail, PostCreate, ReplyCreate, PostUpdate, PostDelete, \
    ReplyDelete, ReplyDetail, BaseRegisterView, IndexView, reply_accept, CategoryList, subscribe, \
    unsubscribe, ConfirmUser

urlpatterns = [
    path('post/', PostList.as_view(), name='post_list'),
    path('post/<int:id>', PostDetail.as_view(), name='single_post'),
    path('post/create/', PostCreate.as_view(), name='post_edit'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('reply/create/', ReplyCreate.as_view(), name='reply_create'),
    path('reply/<int:id>', ReplyDetail.as_view(), name='single_reply'),
    path('reply/<int:pk>/accept/', reply_accept, name='reply_accept'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('profile/', IndexView.as_view()),
]
