# Generated by Django 3.1.4 on 2020-12-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20201223_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.TextField(default='-'),
        ),
    ]
