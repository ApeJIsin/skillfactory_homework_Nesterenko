from django import forms
from .models import Post, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'category', 'post_name', 'post_text')


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('rating', 'user')
