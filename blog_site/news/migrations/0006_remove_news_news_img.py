# Generated by Django 3.1.4 on 2020-12-21 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_picurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='news_img',
        ),
    ]
