from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=255)
    open = models.TimeField()
    close = models.TimeField()
