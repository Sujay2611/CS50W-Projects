# Generated by Django 2.0.3 on 2020-07-04 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_item_incart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='incart',
        ),
    ]
