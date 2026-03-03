from django.contrib import admin
from .models import Blog, Blogger, Comment

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

@admin.register(Blog)
class BlogModel(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'post_date')
    list_filter = ('post_date', 'author')

    fieldsets = (
        ('Main Info', {
            'fields': ('id', 'title', 'author'),
        }),
        ('Content', {
            'fields': ('description', 'post_date'),
        })
    )

    inlines = [CommentInline]

class BlogInline(admin.StackedInline):
    model = Blog
    extra = 0

class BloggerInline(admin.TabularInline):
    model = Blogger
    extra = 1
    can_delete = False

class UserModel(UserAdmin):
    inlines = [BloggerInline]

@admin.register(Comment)
class CommentModel(admin.ModelAdmin):
    list_display = ('author', 'blog', 'description', 'post_date')
    list_filter = ('post_date', 'author')

    fields = [('author', 'blog'), 'description', 'post_date']

admin.site.unregister(User)
admin.site.register(User, UserModel)