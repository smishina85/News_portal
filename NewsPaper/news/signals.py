from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from news.tasks import notification

from .models import PostCategory


# @receiver(m2m_changed, sender=PostCategory)
# def notification(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = list(instance.post.all())
#
#         if categories: # we should check it as creation of the post in admin panel doesn't assign category
#             cat_name_list = []
#             id_cat_list = []
#             for el in categories:
#                 c = el.name_cat
#                 i = el.id
#                 cat_name_list.append(c)
#                 id_cat_list.append(i)
#
#             emails = list(set(list(User.objects.filter(subscriptions__category__in=id_cat_list).values_list('email', flat=True))))
#
#             if emails:
#                 cat_str_for_subj = ' '.join(cat_name_list)
#                 subject = f'This is new post in category: {cat_str_for_subj}'
#                 text_var = instance.text[:256]
#                 text_content = (
#                     f'Post: {text_var}\n'
#                     f'Ссылка на post: http://127.0.0.1:8000{instance.get_absolute_url()}'
#                 )
#                 html_content = (
#                     f'Post: {text_var}<br>'
#                     f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#                     f'Ссылка на post</a>'
#                 )
#                 for email in emails:
#                     msg = EmailMultiAlternatives(subject, text_content, None, [email])
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.send()
#                 else:
#                     pass


@receiver(m2m_changed, sender=PostCategory)
def new_post_notification(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        notification.delay(instance.id)


# Просто так сигналы не начнут работать. Нам нужно выполнить этот модуль (файл с Python-кодом).
# Для этого подойдёт автоматически созданный файл apps.py в нашем приложении.
# В этом файле есть единственный класс с настройками нашего приложения.
# Добавим в него метод ready, который выполнится при завершении конфигурации нашего приложения
# simpleapp. В самом методе импортируем сигналы, таким образом зарегистрировав их.
