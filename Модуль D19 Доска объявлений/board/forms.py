from string import hexdigits

from allauth.account.forms import SignupForm
from ckeditor.fields import RichTextFormField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.core.mail import send_mail
from django.forms import ModelForm

from NewsBoard import settings
from .admin import PostAdminForm
from .models import User, Post, Reply

import random


class PostForm(ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    form = PostAdminForm

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['text', 'post']
        widgets = {
            'text': RichTextFormField(config_name="default"),
        }


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Activation code',
            message=f'Account activation code: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
