# Generated by Django 5.1 on 2024-09-07 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart',
            table='cartid_table',
        ),
    ]