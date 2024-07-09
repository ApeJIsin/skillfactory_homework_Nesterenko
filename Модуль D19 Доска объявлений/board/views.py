from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm, ReplyForm, BaseRegisterForm
from .models import Post, Reply, Category, User


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='board/invalid_code.html')
        return redirect('account_login')


class PostList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'single_post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reply_object = self.object
        context['post_replies'] = Reply.objects.filter(post=reply_object)
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'create'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "board.change_post"
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Post.objects.get(pk=self.kwargs.get('pk')).author
        return context

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.author != self.request.user:
            return render(self.request, 'post_lock.html', context=context)
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "board.delete_post"
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.author != self.request.user:
            return render(self.request, 'post_delete_lock.html', context=context)
        return super(PostDelete, self).dispatch(request, *args, **kwargs)


# дальше представление для поиска откликов по постам
class IndexView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'board/index.html'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.filter(post__author_id=self.request.user.id)
        self.filterset = PostFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Reply.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ReplyDetail(DetailView):
    model = Reply
    template_name = 'single_reply.html'
    context_object_name = 'reply'
    queryset = Reply.objects.all()
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'reply-{self.kwargs["id"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'reply-{self.kwargs["id"]}', obj)
        return obj


def reply_accept(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.accepted = True
    reply.save()
    message = 'You have accepted this reply'
    return render(request, 'board/reply_accepted.html', {'reply': reply, 'message': message})


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_create.html'
    context_object_name = 'reply_create'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        # reply.post_id = self.kwargs['pk']
        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('single_reply', kwargs={'id': self.object.id})


class ReplyDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'board.delete_reply'
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('post_list')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class CategoryList(ListView):
    model = Category

    template_name = 'all_categories.html'
    context_object_name = 'categories'
    paginate_by = 10


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('category_list')


@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('category_list')
