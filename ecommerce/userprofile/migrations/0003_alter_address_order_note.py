# Generated by Django 4.2.3 on 2023-09-21 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_alter_address_address_alter_address_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='order_note',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
