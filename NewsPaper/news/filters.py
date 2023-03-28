from django_filters import FilterSet, ModelChoiceFilter
import django_filters
from .models import Post, Category, PostCategory
from django.forms import DateInput, Textarea


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.

class PostFilter(FilterSet):
    class Meta:
# В Meta классе мы должны указать Django модель,
# в которой будем фильтровать записи.
        model = Post
# В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = {
           # поиск по заголовку
           'title': ['icontains'],
        # поиск по категории
           'post': ['exact'],
       }
        #widgets={'title': Textarea(attrs={'cols': 128, 'rows': 2}),
                # 'post': Textarea(attrs={'cols': 50}),}

    date = django_filters.DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Дата',
        widget=DateInput(attrs={'type': 'date'},
                         )
    )