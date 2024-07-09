from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Reply
from django.conf import settings


def send_notifications(preview, pk, title, subscribers_list, author):
    for s in subscribers_list:
        sub_name = s.username
        if sub_name != author.username:
            sub_email = [s.email]
            html_content = render_to_string(
                'post_created_email.html',
                {
                    'title': title,
                    'text': preview,
                    'link': f'{settings.SITE_URL}/post/{pk}',
                }
            )

            msg = EmailMultiAlternatives(
                subject='New post!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=sub_email,
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, **kwargs):
    category = instance.category
    author = instance.author
    subscribers_list = []

    subscribers = category.subscribers.all()
    subscribers_list += [s for s in subscribers]

    send_notifications(instance.preview, instance.pk, instance.title, subscribers_list, author)


def send_new_reply(reply_author, reply_text, reply_post):

    html_content = render_to_string(
        template_name='reply_created_email.html',
        context={
            'post_author': reply_post.author,
            'reply_author': reply_author,
            'text': reply_text,
            'link': f'{settings.SITE_URL}/post/{reply_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='New reply to your post!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reply_post.author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Reply)
def notify_about_new_reply(sender, instance, **kwargs):
    reply_author = instance.author
    reply_text = instance.text
    reply_post = instance.post

    send_new_reply(reply_author, reply_text, reply_post)


def send_accept_reply(reply_author, reply_post):
    html_content = render_to_string(
        template_name='accept_reply_email.html',
        context={
            'reply_author': reply_author,
            'link': f'{settings.SITE_URL}/post/{reply_post.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your reply has been accepted!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reply_author.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Reply)
def notify_about_accepted_reply(sender, instance, **kwargs):
    reply_author = instance.author
    reply_post = instance.post
    if instance.accepted:
        send_accept_reply(reply_author, reply_post)
