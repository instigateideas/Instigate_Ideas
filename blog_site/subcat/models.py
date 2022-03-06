from __future__ import unicode_literals
from django.db import models


class SubCategory(models.Model):
    subcat_name = models.CharField(max_length=30)
    catname = models.CharField(max_length=50)
    catid = models.IntegerField()
    namedb = "Sub-Category Type"

    def __str__(self):
        return self.namedb + " | " + str(self.pk)