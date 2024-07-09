from django_filters import FilterSet

from .models import Reply, Post


class PostFilter(FilterSet):

    class Meta:
        model = Reply
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])
