from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']*3
        author_comment_rating = Comment.object.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        sum_com_to_post = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = author_post_rating + author_comment_rating + sum_com_to_post
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    POST = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_name = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.CharField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
