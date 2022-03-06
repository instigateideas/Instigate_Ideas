from __future__ import unicode_literals
from django.db import models


class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=80)
    msg = models.CharField(max_length=600)
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12)
    namedb = "Contact Info"

    def __str__(self):
        return self.namedb + " | " + str(self.pk)