from django.db import models


class Purchase(models.Model):
    store = models.ForeignKey('stores.Store', on_delete=models.PROTECT)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT)
    item = models.CharField(max_length=255, default='')
    quantity = models.IntegerField(default=0)