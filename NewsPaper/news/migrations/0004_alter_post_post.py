# Generated by Django 4.1.7 on 2023-03-28 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_post_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
    ]
