# Generated by Django 3.1 on 2020-08-06 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='item_id',
        ),
        migrations.AddField(
            model_name='storage',
            name='item',
            field=models.CharField(default='', max_length=255),
        ),
    ]