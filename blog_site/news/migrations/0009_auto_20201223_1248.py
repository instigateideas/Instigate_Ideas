# Generated by Django 3.1.4 on 2020-12-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_news_ocatid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='ocatid',
            field=models.IntegerField(default=0),
        ),
    ]
