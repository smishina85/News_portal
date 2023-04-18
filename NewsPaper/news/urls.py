from django.urls import path, include
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostDelete, PostUpdate, subscriptions





urlpatterns = [
# path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('', PostsList.as_view(), name='posts'),
# pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view() , name='post_search'),
    path('create/', PostCreate.as_view(), name= 'post_create'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    #path('index/', IndexView.as_view()),
]