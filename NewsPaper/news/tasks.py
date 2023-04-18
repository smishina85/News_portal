from celery import shared_task

from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category
from django.contrib.auth.models import User
import datetime


# @shared_task
# def hello():
#     time.sleep(10)
#     print("hello world!")
#
# # Здесь мы использовали функцию sleep() из пакета time, чтобы остановить выполнение процесса на 10 секунд.
# # Это поможет нам убедиться, что Клиент не «встал», пока выполняется эта задача.
#
# @shared_task
# def printer(N):
#     for i in range (N):
#         time.sleep(1)
#         print(i+1)

# Представим, что у нас есть задача, которая зависит от аргументов. Например, сделаем цикл, который раз в секунду
# печатает число от 1 до переданного числа:

@shared_task
#def notification(sender, instance, **kwargs):
def notification(instance_id):
    #if kwargs['action'] == 'post_add':
    instance = Post.objects.get(pk=instance_id)
    categories = list(instance.post.all())

    if categories: # we should check it as creation of the post in admin panel doesn't assign category
        cat_name_list = []
        id_cat_list = []
        for el in categories:
            c = el.name_cat
            i = el.id
            cat_name_list.append(c)
            id_cat_list.append(i)

        emails = list(set(list(User.objects.filter(subscriptions__category__in=id_cat_list).values_list('email', flat=True))))

        if emails:
            cat_str_for_subj = ' '.join(cat_name_list)
            subject = f'This is new post in category: {cat_str_for_subj}'
            text_var = instance.text[:256]
            text_content = (
                f'Post: {text_var}\n'
                f'Ссылка на post: http://127.0.0.1:8000{instance.get_absolute_url()}'
            )
            html_content = (
                f'Post: {text_var}<br>'
                f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
                f'Ссылка на post</a>'
            )
            for email in emails:
                msg = EmailMultiAlternatives(subject, text_content, None, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                pass

# еженедельная рассылка последних новостей

@shared_task
def every_wk_news_mailing():
    date_wk_ago = datetime.datetime.today() - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=date_wk_ago)
    # need posts with assigned category (if post created from admin panel there couldn't be a category assigned
    posts_categorized = posts.filter(post__isnull=False)

    if posts_categorized:  # if there is no any post for the last week no actions required
        # create a dictionary where key is a name of category and value is a list of emails of subscribers
        categories = list(Category.objects.all())

        for el in categories:
            cat_name = el.name_cat
            id_cat = el.id
            emails = list(
                set(list(User.objects.filter(subscriptions__category__exact=id_cat).values_list('email', flat=True))))
            if emails:
                subject = f'Posts published last week in category: {cat_name}'
                text_content = ''
                html_content = ''
                # print(cat_name)
                # need to have the list of id of last week posts assigned to exact category
                postid_exact_cat = list(
                    set(posts_categorized.filter(post__name_cat__exact=cat_name).values_list('id', flat=True)))
                # print(postid_exact_cat)

                for i in postid_exact_cat:
                    post = Post.objects.get(pk=i)
                    text_var = post.title[:128]
                    pub_date = (post.time_in).date()
                    text_content += (
                        f'{pub_date}  |  {text_var}  |   Ссылка на post: http://127.0.0.1:8000{post.get_absolute_url()}\n')
                    html_content += (
                        f'{pub_date}  |  {text_var}  |  <br><a href="http://127.0.0.1:8000{post.get_absolute_url()}"></a>\n')
                # print(html_content)
                # print(emails)
                # print(text_content)

                for email in emails:
                    msg = EmailMultiAlternatives(subject, text_content, None, [email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

