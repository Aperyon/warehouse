from django.db import models


class Storage(models.Model):
    store_id = models.ForeignKey('stores.Store', on_delete=models.PROTECT)
    item = models.CharField(max_length=255, default='')
    stock = models.IntegerField(default=0)
