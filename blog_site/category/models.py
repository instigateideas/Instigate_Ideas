from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=30)
    count = models.IntegerField(default=0)
    namedb = "Category Type"

    def __str__(self):
        return self.namedb + " | " + str(self.pk)