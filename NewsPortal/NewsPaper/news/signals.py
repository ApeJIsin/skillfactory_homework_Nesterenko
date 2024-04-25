from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    for subscriber in subscribers:
        html_content = render_to_string(
            'flatpages/post_created_email.html',
            {
                'username': subscriber.username,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_users = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_users += [s for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_users)
