# Generated by Django 2.0.3 on 2020-07-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]