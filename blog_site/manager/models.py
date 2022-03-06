from __future__ import unicode_literals
from django.db import models


class Manager(models.Model):
    dbname = "Manager"
    name = models.TextField(default="")
    uname = models.TextField(default="")
    email = models.TextField(default="")

    def __str__(self):
        return self.dbname + " | " + self.pk
