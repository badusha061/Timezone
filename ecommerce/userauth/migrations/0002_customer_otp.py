# Generated by Django 4.2.3 on 2023-09-14 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='otp',
            field=models.IntegerField(blank=True, default=True, null=True),
        ),
    ]
