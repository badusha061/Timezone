# Generated by Django 4.2.3 on 2023-09-18 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_range',
        ),
    ]
