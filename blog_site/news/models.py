from __future__ import unicode_literals
from django.db import models


class News(models.Model):
    author = models.CharField(default="-", max_length=30)
    date = models.CharField(max_length=30)
    picname = models.TextField(default="-")
    picurl = models.TextField(default="-")
    news_title = models.TextField(default="-")
    short_text = models.TextField(default="-")
    news_text = models.TextField(default="-")
    catid = models.TextField(default="0")
    ocatid = models.IntegerField(default=0)
    cat_name = models.TextField(default="-")
    views = models.IntegerField(default=0)
    namedb = "news article"
    tags = models.TextField(default="-")

    def __str__(self):
        return self.namedb + " | " + str(self.pk)