# Generated by Django 3.1.4 on 2020-12-31 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=12)),
                ('time', models.CharField(max_length=12)),
                ('txt', models.TextField()),
            ],
        ),
    ]
