from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post, PostCategory

class Command(BaseCommand):
    help = 'This command deletes all news from some category'
    missing_args_message = 'Not enough arguments'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', nargs=1)

    def handle(self, *args, **options):
        cat = (options['category'][0]).capitalize()
        # print(cat)
        # print(type(cat))
        # print(cat[0])
        try:
            category = Category.objects.get(name_cat = cat )
            # print(type(category))
            news_categorized = Post.objects.filter(post__name_cat=cat)
            # print(type(news_categorized))
            news_quantity = news_categorized.count()
            # print(news_quantity)
            if news_quantity:
                self.stdout.readable()
                self.stdout.write(f'The are {news_quantity} news in category {cat}. Do you really want to delete them ? yes/no')
                answer = input()
                if answer == 'yes':
                    # news_categorized.all().delete()
                    # for news in news_categorized:
                    #     # print(news.id)
                    #     # print((Post.objects.get(id=news.id)).id)
                    #     Post.objects.get(id=news.id).delete()
                        # self.stdout.write(self.style.SUCCESS('Successfully deleted news "%s"' % str(news)))
                    news_categorized.delete()
                    self.stdout.write(self.style.SUCCESS(f'All news of the category {cat} deleted'))
                    return
                self.stdout.write(self.style.ERROR('Access denied'))
        except ObjectDoesNotExist:
            self.stdout.write('Wrong parameter or such category does not exist')

        # self.stdout.write(str(options['category']))





