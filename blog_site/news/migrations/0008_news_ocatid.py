# Generated by Django 3.1.4 on 2020-12-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_news_catid'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='ocatid',
            field=models.TextField(default='0'),
        ),
    ]