# Generated by Django 3.1.4 on 2020-12-23 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
