from django.forms import DateInput

import django_filters
from django_filters import FilterSet

from .models import Post

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
                'author': ['exact'],
                'title': ['icontains'],
                'post': ['exact'],
            }

    date = django_filters.DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Дата',
        widget=DateInput(attrs={'type': 'date'},
                         )
    )
