from django.contrib.auth.mixins import PermissionRequiredMixin   # D5.6
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from pprint import pprint


class PostsList(ListView):
         # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 8

         # Переопределяем функцию получения списка товаров
    def get_queryset(self):
             # Получаем обычный запрос
        queryset = super().get_queryset()
             # Используем наш класс фильтрации.
             # self.request.GET содержит объект QueryDict, который мы рассматривали
             # в этом юните ранее.
             # Сохраняем нашу фильтрацию в объекте класса,
             # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)

             # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

# Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
# С помощью super() мы обращаемся к родительским классам
# и вызываем у них метод get_context_data с теми же аргументами,
# что и были переданы нам.
# В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
# К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
     model = Post
#     # Используем другой шаблон — post.html
     template_name = 'post.html'
#     # Название объекта, в котором будет выбранная пользователем новость
     context_object_name = 'post'


class PostSearch(ListView):
# # Указываем модель, объекты которой мы будем выводить
    model = Post
# # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
# # Указываем имя шаблона, в котором будут все инструкции о том,
# # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_search.html'
# # Это имя списка, в котором будут лежать все объекты.
# # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_search'
    paginate_by = 4
#
# # Переопределяем функцию получения списка товаров
    def get_queryset(self):
#     # Получаем обычный запрос
        queryset = super().get_queryset()
#     # Используем наш класс фильтрации.
    # self.request.GET содержит объект QueryDict, который мы рассматривали
#     # в этом юните ранее.
#     # Сохраняем нашу фильтрацию в объекте класса,
#     # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)

        if not self.request.GET:
            return queryset.none()
#
#     # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
#
#
# # Метод get_context_data позволяет нам изменить набор данных,
# # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
#     # С помощью super() мы обращаемся к родительским классам
#     # и вызываем у них метод get_context_data с теми же аргументами,
#     # что и были переданы нам.
#     # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
#     # К словарю добавим текущую дату в ключ 'time_now'.
#         context['time_now'] = datetime.utcnow()
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

