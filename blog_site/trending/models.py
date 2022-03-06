from __future__ import unicode_literals
from django.db import models


class Trending(models.Model):
    name = "Trending News"
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12)
    txt = models.TextField()

    def __str__(self):
        return self.name + " | " + self.pk
