from django.contrib import admin
from django import forms

from .models import Post, Reply, Category, User

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'category'
        ]


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Category)
