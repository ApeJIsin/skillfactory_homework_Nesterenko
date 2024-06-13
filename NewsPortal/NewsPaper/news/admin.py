from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment

# Register your models here.


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_rating.short_description = 'Обнулить рейтинг'

def rating_boost(modeladmin, request, queryset):
    queryset.update(rating=100)


rating_boost.short_description = 'Рейтинг 100!!!'


class CatInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CatInLine,)
    list_display = ('post_name', 'time_create', 'post_type', 'author', 'post_rating', 'low_rating')
    list_filter = ('post_name', 'post_rating', 'time_create', 'author')
    search_fields = ('post_name', 'author__full_name', 'time_create')
    actions = [nullify_rating, rating_boost]


class CatAdmin(admin.ModelAdmin):
    search_fields = (
        'name_category',
    )
    list_filter = ('name_category', 'subscribers')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'rating', 'user')
    list_filter = ('full_name', 'rating', 'user')
    search_fields = ('full_name', 'rating', 'user__username')
    actions = [nullify_rating, rating_boost]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('comment_rating', 'time_comment', 'post__title', 'user')
    search_fields = ('comment', 'comment_rating', 'time_comment', 'post__title', 'user__username')
    actions = [nullify_rating, rating_boost]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
