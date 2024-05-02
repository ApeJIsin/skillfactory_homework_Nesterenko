from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from NewsPaper import settings
from .models import Post, Category


@shared_task
def inform_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.post_name
    subscribers_email = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        for sub in subscribers:
            subscribers_email.append(sub.email)

    html_content = render_to_string(
        'flatpages/post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_mailing():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'flatpages/weekly_mailing.html',
        {
            'link': 'http://127.0.0.1:8000',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Подборка статей за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
