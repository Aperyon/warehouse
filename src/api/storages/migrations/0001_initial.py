# Generated by Django 3.1 on 2020-08-06 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('stock', models.IntegerField(default=0)),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stores.store')),
            ],
        ),
    ]
