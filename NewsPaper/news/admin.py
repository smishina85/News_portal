from django.contrib import admin
# from django.contrib.auth.models import User

from .models import Author, Category, Comment, Post, PostCategory, Subscription


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating.short_description = 'Nullfy the rating'

class PostAdmin(admin.ModelAdmin):
    list_display = ('time_in', 'author', 'title', 'cat_adm', 'rating_post')
    list_filter = ('time_in', 'author', 'rating_post')
    search_fields = ('time_in', 'title')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fio_author', 'rating')
    list_filter = ('user__last_name', 'rating')
    actions = [nullfy_rating]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('user', 'category')

admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscription, SubscriptionAdmin)

# Register your models here.
