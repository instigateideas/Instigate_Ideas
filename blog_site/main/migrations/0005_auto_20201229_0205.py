# Generated by Django 3.1.4 on 2020-12-29 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201228_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='picname',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='main',
            name='picurl',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='main',
            name='fb',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='main',
            name='pt',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='main',
            name='tw',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='main',
            name='vm',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='main',
            name='yt',
            field=models.TextField(default=''),
        ),
    ]