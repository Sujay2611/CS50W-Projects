# Generated by Django 2.0.3 on 2020-07-02 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_item_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
    ]
