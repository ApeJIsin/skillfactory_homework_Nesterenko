from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

# Create your views here.


class PostsList(ListView):
    model = Post
    ordering = '-post_name'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = Post.time_create
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
