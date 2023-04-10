from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Avg, F, Max, Min
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def update_rating(self):
        postRat = self.post_set.all().aggregate(Sum('rating_post'))
        pRat = 0
        pRat += postRat.get('rating_post__sum')

        cRat = 0
        cpRat = 0
        if self.user.comment_set.all():
            commentRat = self.user.comment_set.all().aggregate(Sum('comm_rating'))
            cRat += commentRat.get('comm_rating__sum')
            commpostRat = Comment.objects.filter(post__in= self.post_set.all()).exclude(user__author__in=[self]).aggregate(Sum('comm_rating'))
            cpRat += commpostRat.get('comm_rating__sum')

        self.rating = pRat * 3 + cRat + cpRat
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Category(models.Model):
    name_cat = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name_cat.title()}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'

    CHARACTER = [
        (NEWS, 'News'), (ARTICLE, 'Article')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    charact = models.CharField("Новость или Статья", max_length=2, choices=CHARACTER, default=NEWS)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Заголовок", max_length=128)
    text = models.TextField("Ваш текст")
    rating_post = models.SmallIntegerField(default=0)
    post = models.ManyToManyField(Category,through='PostCategory', verbose_name="Категория")

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        if self.text:
            return '{} ...'.format(self.text[:125])

    def __str__(self):
        cat_list = list(((self.post).all()).values('name_cat'))
        # if cat_list:
        #     print(cat_list[0]['name_cat'])
        cat_str = ''
        if cat_list:
            for i in range(len(cat_list)):
                cat_str += cat_list[i]['name_cat'] +' '
        else:
            cat_str += 'Assign category'
        #print(cat_str)
        #print(cat_list)
        return f"Date of creation: {self.time_in}\n Author: {self.author.user}\n (Rating: {self.rating_post})\n Title: {self.title} \n( {cat_str})"

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title}  -  Category: {self.category}"

    class Meta:
        verbose_name = 'Postcategory'
        verbose_name_plural = 'Postcategories'


class Comment(models.Model):
    comm = models.TextField()
    comm_time_in = models.DateTimeField(auto_now_add=True)
    comm_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comm_rating += 1
        self.save()

    def dislike(self):
        self.comm_rating -= 1
        self.save()

    def __str__(self):
        return f"Date: {self.comm_time_in}, Created by: {self.user.username}, Rating: {self.comm_rating}, Comment: {self.comm}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscription'
    )


