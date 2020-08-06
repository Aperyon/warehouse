from django.db import models


class Storage(models.Model):
    store_id = models.ForeignKey('stores.Store', on_delete=models.PROTECT)
    item_id = models.IntegerField()
    stock = models.IntegerField(default=0)
