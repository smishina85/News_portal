from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscription
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscription)

# Register your models here.