# Generated by Django 2.0.3 on 2020-07-03 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order', to='orders.Item'),
        ),
    ]