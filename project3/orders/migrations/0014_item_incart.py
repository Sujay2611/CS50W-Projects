# Generated by Django 2.0.3 on 2020-07-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20200703_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='incart',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
