from __future__ import unicode_literals
from django.db import models


class Main(models.Model):
    name = models.TextField()
    about = models.TextField()
    abouttxt = models.TextField(default="")
    fb = models.TextField(default="")
    yt = models.TextField(default="")
    tw = models.TextField(default="")
    pt = models.TextField(default="")
    vm = models.TextField(default="")

    picurl = models.TextField(default="")
    picname = models.TextField(default="")
    picurl2 = models.TextField(default="")
    picname2 = models.TextField(default="")