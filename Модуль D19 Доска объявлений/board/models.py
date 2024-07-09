from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    tanks = 'Tanks'
    heals = 'Heals'
    damagedealers = 'Damage Dealers'
    merchants = 'Merchants'
    guildmasters = 'Guild Masters'
    questgivers = 'Quest Givers'
    blacksmiths = 'Blacksmiths'
    leathercrafters = 'Leather Crafters'
    potionmakers = 'Potion Makers'
    spellmasters = 'Spell Masters'
    CONTENTS = [
        (tanks, 'Танки'),
        (heals, 'Хилы'),
        (damagedealers, 'ДД'),
        (merchants, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (leathercrafters, 'Кожевники'),
        (potionmakers, 'Зельевары'),
        (spellmasters, 'Мастера заклинаний'),
    ]

    name = models.CharField(max_length=20, choices=CONTENTS)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('single_post', args=[str(self.id)])

    def preview(self):
        return self.text[0:50] + '...'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_author')
    text = RichTextUploadingField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_replies')
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def preview(self):
        return f'{self.text[:20]}...'

    def accept_reply(self):
        self.accepted = True
        self.save()

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'reply-{self.id}')

    def get_absolute_url(self):
        return reverse(f'single_reply', args=[str(self.id)])
